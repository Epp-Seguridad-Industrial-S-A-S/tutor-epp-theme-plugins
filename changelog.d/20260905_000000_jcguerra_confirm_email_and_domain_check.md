<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Feature] Add a "confirm email" field to self-registration (fixes an upstream authn bug
  where `field_type="email"` was never rendered) and reject registrations whose email
  domain has no MX/A record (fails open on DNS errors). Configure with
  `INDIGO_REQUIRE_CONFIRM_EMAIL` and `INDIGO_ENABLE_EMAIL_DOMAIN_CHECK` (both default
  `true`; set to `false` to disable). (by @Epp-Seguridad-Industrial-S-A-S)
