<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Bugfix] Confirm-email field: drop the ``REGISTRATION_EXTRA_FIELDS`` /
  ``ENABLE_DYNAMIC_REGISTRATION_FIELDS`` approach (it can't deliver ``confirm_email`` to the
  authn MFE, and it side-effected optional demographic fields onto the registration form).
  The authn fork now renders the second email input directly; the only wiring is
  ``MFE_CONFIG['EPP_ENABLE_CONFIRM_EMAIL']``, driven by ``INDIGO_ENABLE_CONFIRM_EMAIL``
  (was ``INDIGO_REQUIRE_CONFIRM_EMAIL``). (by @Epp-Seguridad-Industrial-S-A-S)
