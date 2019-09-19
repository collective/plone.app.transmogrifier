# -*- coding: utf-8 -*-
from Products.Archetypes.event import ObjectEditedEvent
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.interfaces import IBaseObject
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import Matcher
from collective.transmogrifier.utils import defaultKeys
from collective.transmogrifier.utils import traverse
from zope import event
from zope.interface import classProvides, implements


def _compare(fieldval, itemval):
    """Compare a AT Field value with an item value

    Because AT fields return utf8 instead of unicode and item values may be
    unicode, we need to special-case this comparison. In case of fieldval
    being a str and itemval being a unicode value, we'll decode fieldval and
    assume utf8 for the comparison.

    """
    if isinstance(fieldval, str) and isinstance(itemval, unicode):
        return fieldval.decode('utf8', 'replace') == itemval
    return fieldval == itemval


def get(field, obj):
    if getattr(field, 'getAccessor', False):
        return field.getAccessor(obj)()
    elif field.accessor is not None:
        return getattr(obj, field.accessor)()
    return field.get(obj)


def set(field, obj, val):
    if getattr(field, 'getMutator', False):
        field.getMutator(obj)(val)
    elif field.mutator is not None:
        getattr(obj, field.mutator)(val)
    else:
        field.set(obj, val)


class ATSchemaUpdaterSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        if 'path-key' in options:
            pathkeys = options['path-key'].splitlines()
        else:
            pathkeys = defaultKeys(options['blueprint'], name, 'path')
        self.pathkey = Matcher(*pathkeys)

    def __iter__(self):  # noqa: C901
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]

            if not pathkey:         # not enough info
                yield item
                continue

            path = item[pathkey]

            obj = traverse(self.context, str(path).lstrip('/'), None)
            if obj is None:         # path doesn't exist
                yield item
                continue

            if IBaseObject.providedBy(obj):
                changed = False
                is_new_object = obj.checkCreationFlag()
                keys = item.keys()
                keys.sort()
                for k in keys:
                    if k.startswith('_'):
                        continue
                    field = obj.getField(k)
                    if field is None:
                        continue
                    v = item[k]
                    if not _compare(get(field, obj), v):
                        set(field, obj, v)
                        changed = True
                obj.unmarkCreationFlag()

                if is_new_object:
                    event.notify(ObjectInitializedEvent(obj))
                    obj.at_post_create_script()
                elif changed:
                    event.notify(ObjectEditedEvent(obj))
                    obj.at_post_edit_script()

            yield item
