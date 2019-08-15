# -*- coding: utf-8 -*-
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import Matcher
from collective.transmogrifier.utils import defaultKeys
from Products.CMFPlone.utils import safe_unicode
from zope.interface import provider
from zope.interface import implementer


@provider(ISectionBlueprint)
@implementer(ISection)
class PathFixer(object):
    """Changes the start of the path.
    """

    def __init__(self, transmogrifier, name, options, previous):
        """
        :param options['path-key']: The key, under the path can be found in
                                    the item.
        :param options['stripstring']: A string to strip from the beginning of
                                       the path.
        :param options['prependstring']: A string to prepend on the beginning
                                         of the path.
        """
        self.previous = previous
        self.context = transmogrifier.context

        if 'path-key' in options:
            pathkeys = options['path-key'].splitlines()
        else:
            pathkeys = defaultKeys(options['blueprint'], name, 'path')
        self.pathkey = Matcher(*pathkeys)

        self.stripstring = None
        if 'stripstring' in options and options['stripstring']:
            self.stripstring = options['stripstring'].splitlines()[0]

        self.prependstring = None
        if 'prependstring' in options and options['prependstring']:
            self.prependstring = options['prependstring'].splitlines()[0]

    def __iter__(self):

        for item in self.previous:

            pathkey = self.pathkey(*list(item.keys()))[0]
            stripstring = self.stripstring
            prependstring = self.prependstring

            if not pathkey or not (stripstring or prependstring):
                # not enough info or nothing to do
                yield item
                continue

            path = item[pathkey]

            if stripstring and path.startswith(stripstring):
                path = path[len(stripstring):]
            if prependstring:
                path = '%s%s' % (prependstring, path)

            item[pathkey] = safe_unicode(path)

            yield item
