<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Improvement] The account-activation email no longer has an empty "use our web form
  at ___" link or Tutor's ``{platform name} - https://{host}`` placeholder in the footer.
  New ``INDIGO_ACTIVATION_EMAIL_SUPPORT_URL`` (sets ``ACTIVATION_EMAIL_SUPPORT_LINK``) and
  ``INDIGO_CONTACT_MAILING_ADDRESS`` (sets ``CONTACT_MAILING_ADDRESS``); an empty value
  falls back to the upstream default. (by @Epp-Seguridad-Industrial-S-A-S)
