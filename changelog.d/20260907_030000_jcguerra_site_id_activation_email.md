<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Bugfix] The account-activation email no longer links to ``example.com``. ACE
  transactional emails render in a request-less Celery worker and build URLs from the
  ``Site`` at ``SITE_ID``; that row was still Django's default ``example.com``. New
  ``INDIGO_SITE_ID`` setting (default ``3``) points ``SITE_ID`` at the ``udesst.com``
  ``Site``, and ``tasks/init.sh`` now canonicalises the ``SITE_ID`` row instead of only
  creating extra rows via ``get_or_create``. (by @Epp-Seguridad-Industrial-S-A-S)
