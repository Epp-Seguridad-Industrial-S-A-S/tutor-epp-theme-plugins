<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Bugfix] Set `LANGUAGE_CODE = "es-419"` for the LMS (production and development). Anonymous
  visitors without an explicit language cookie or browser preference (e.g. hitting
  `/authn/register` directly) were falling back to English because the platform never declared
  a default language. Visitors whose browser or cookie already request another language are
  unaffected. (by @Epp-Seguridad-Industrial-S-A-S)
