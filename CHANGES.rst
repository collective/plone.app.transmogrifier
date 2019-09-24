Changelog
=========

1.4.2 (2019-09-24)
------------------

- ``plone.app.transmogrifier.atschemaupdater`` updates fields in fixed order
  (field names) for bette debuggability.
  [gotcha]

- ``plone.app.transmogrifier.pathfixer`` now also converts a path into ``str`` and removes any invalid characters from it;
  this avoids ``UnicodeEncodeError`` in many blueprint sections.
  [hvelarde]


1.4.1 (2018-02-27)
------------------

- Avoid failures on redirector section when there is no object in referenced path.
  [hvelarde]

- Fix ``plone.app.transmogrifier.browserdefault`` blueprint section:
  ``default_page`` and ``layout`` properties should be string, not unicode.
  [sunew]


1.4 (2015-10-23)
----------------

- Support updating effective and expiration dates on ``plone.app.transmogrifier.datesupdater`` blueprint.
  Fix field discovering logic to avoid skipping the ones set as ``None``.
  Fix documentation.
  [hvelarde]

- Support indexing of individual indexes for the
  ``plone.app.transmogrifier.reindexobject`` blueprint.
  [thet]


1.3 (2015-01-22)
----------------

- Ignore if workflow_history is not available on objects when running the
  workflowupdater blueprint.
  [thet]

- Add datesupdater section to set creation_date and modification_date on
  objects.
  [thet]

- Add pathfixer section to remove/prepend parts of the path.
  [thet]

- PEP 8.
  [thet]

- Fix uidsection for dexterity.
  [shylux]

- Allow to import transition date in the worflow history
  [ebrehault]

- Fix field accessor and mutator for updating schemaextended field values
  with schemaupdater.
  In some cases when using fields extended by schemaextender it defines
  an accessor attribute which is not accessable. To cover all fields, its
  better to access and mutate over the getAccessor and getMutator methods on
  archetype fields.
  [elioschmutz]

- Add a section to manage `plone.app.redirector` and to use it to
  update paths.
  [rpatterson]

- Support field accessor and mutator for updating field values with
  schemaupdater.
  [phgross]


1.2 (2011-05-23)
----------------

- Sections to disable and enable versioning within the pipeline.
  [elro]

- Convert paths to strings.
  [elro]

- Add a 'verbose' option to reindexobject blueprint
  that logs the object currently reindexed and number of objects reindexed.
  [thomasdesvenain]

- Check for CatalogAware base class when reindexing an object instead of
  CMFCatalogAware because in Plone 4 folders do not inherit from
  CMFCatalogAware.
  [buchi]


1.1 (2010-03-30)
----------------

- Added Indexing section. See reindexobject.rst.
  [sylvainb]

- Added UID updated section. See uidupdater.rst.
  [optilude]

- Fixed tests for Plone 4, in the same way that they were fixed in
  collective.transmogrifier.
  [optilude]


1.0 (2009-08-09)
----------------

- Initial package.
  [mj]
