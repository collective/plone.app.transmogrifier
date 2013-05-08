import posixpath
import logging

from xml.etree.ElementTree import Element
try:
    from lxml.etree import ElementBase
except ImportError:
    ElementBase  # pyflakes
    ElementBase = Element

from zope.interface import classProvides, implements
from zope.component import queryUtility

from plone.app.redirector.interfaces import IRedirectionStorage

from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher, Matcher, Condition


class RedirectorSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.logger = logging.getLogger(name)

        self.condition = Condition(options.get(
            'condition',
            'python:"remoteUrl" not in item and "_is_defaultpage" not in item'
            ), transmogrifier, name, options)

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.oldpathskey = defaultMatcher(
            options, 'old-paths-key', name, 'old_paths')

        self.updatepathkeys = Matcher(*options.get(
            'update-path-keys',
            "_content_element\nremoteUrl\nrelatedItems").splitlines())

        self.elementattribs = options.get('element-attributes',
                                          ('href', 'src'))

    def __iter__(self):
        storage = queryUtility(IRedirectionStorage)
        for item in self.previous:
            if storage is None:
                self.logger.warn(
                    'Could not find plone.app.redirector storage utility')
                yield item
                continue

            keys = item.keys()

            old_paths = set()
            oldpathskey = self.oldpathskey(*keys)[0]
            if oldpathskey and oldpathskey in item:
                paths = item[oldpathskey]
                if isinstance(paths, (str, unicode)):
                    paths = [paths]
                old_paths.update(paths)

            pathkey = self.pathkey(*keys)[0]
            if pathkey:
                path = item[pathkey]
                for old_path in old_paths:
                    if old_path and old_path != path:
                        storage.add(str(old_path).lstrip('/'),
                                    str(path).lstrip('/'))

            for key in keys:
                if not self.updatepathkeys(key)[1]:
                    continue

                multiple = True
                paths = item[key]
                if not isinstance(paths, (tuple, list)):
                    multiple = False
                    paths = [paths]

                for idx, obj in enumerate(paths):
                    path = obj
                    is_element = isinstance(obj, (Element, ElementBase))
                    if is_element:
                        for attrib in self.elementattribs:
                            if attrib in obj.attrib:
                                path = obj.attrib[attrib]
                                break
                        else:
                            # No attribute in this element
                            continue

                    path = str(path).lstrip('/')

                    new_path = old_path = ''
                    for elem in pathsplit(path):
                        old_path = posixpath.join(old_path, elem)
                        new_path = storage.get(old_path, new_path)

                    if is_element:
                        obj.attrib[attrib] = new_path
                        new_path = obj
                    paths[idx] = new_path

                if not multiple:
                    paths = paths[0]
                item[key] = paths

            yield item


def pathsplit(path):
    if path:
        dirname, basename = posixpath.split(path)
        for elem in pathsplit(dirname):
            yield elem
        yield basename
