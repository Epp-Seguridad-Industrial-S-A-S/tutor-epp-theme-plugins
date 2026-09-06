<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Bugfix] Also set the Django-level ``ENABLE_DYNAMIC_REGISTRATION_FIELDS = True`` (not just
  the ``MFE_CONFIG`` flag) when ``INDIGO_REQUIRE_CONFIRM_EMAIL`` is on. Without it,
  ``/api/mfe_context`` returns no extra registration fields and the "Confirm email" field
  never reaches the authn MFE. (by @Epp-Seguridad-Industrial-S-A-S)
