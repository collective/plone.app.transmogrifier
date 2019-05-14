# -*- coding: utf-8 -*-
from OFS.Image import File
from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.utils import Condition
from collective.transmogrifier.utils import Expression
from collective.transmogrifier.utils import defaultMatcher
from zope.interface import provider, implementer


@provider(ISectionBlueprint)
@implementer(ISection)
class MimeEncapsulatorSection(object):

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.datakey = defaultMatcher(options, 'data-key', name, 'data')
        self.mimetype = Expression(options['mimetype'],
                                   transmogrifier, name, options)
        self.field = Expression(options['field'],
                                transmogrifier, name, options)
        self.condition = Condition(options.get('condition', 'python:True'),
                                   transmogrifier, name, options)

    def __iter__(self):
        for item in self.previous:
            key, match = self.datakey(*list(item.keys()))
            if not key:
                yield item
                continue

            field = self.field(item, key=key, match=match)
            mimetype = self.mimetype(item, key=key, match=match, field=field)
            if self.condition(item, key=key, match=match,
                              field=field, mimetype=mimetype):
                item[field] = File(field, field, item[key], mimetype)

            yield item
