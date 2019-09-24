from setuptools import find_packages
from setuptools import setup
import os


version = '1.4.2'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = ('\n'.join((
    read('README.rst'), ''
    'Detailed Documentation',
    '======================', '',
    read('src', 'plone', 'app', 'transmogrifier', 'atschemaupdater.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'browserdefault.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'criteria.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'datesupdater.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'mimeencapsulator.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'pathfixer.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'portaltransforms.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'redirector.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'reindexobject.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'uidupdater.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'urlnormalizer.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'versioning.rst'), '',
    read('src', 'plone', 'app', 'transmogrifier', 'workflowupdater.rst'), '',

    read('CHANGES.rst'), '',
)))
open('compiled-doc.rst', 'w').write(long_description)

name = 'plone.app.transmogrifier'
setup(
    name=name,
    version=version,
    description="Plone blueprints for collective.transmogrifier pipelines",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='content import filtering plone',
    author='Jarn',
    author_email='info@jarn.com',
    url='http://pypi.python.org/pypi/plone.app.transmogrifier',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.transmogrifier>=1.1',
        'plone.uuid',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
