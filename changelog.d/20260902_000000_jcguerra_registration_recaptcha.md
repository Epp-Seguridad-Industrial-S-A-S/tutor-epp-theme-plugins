<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Feature] Add Google reCAPTCHA to the self-registration flow. The `authn` MFE is now
  built from the EPP fork (which renders the reCAPTCHA widget) and the token is verified
  server-side by the `epp-registration-captcha` package, installed into the openedx image.
  Configure with `INDIGO_RECAPTCHA_SITE_KEY`, `INDIGO_RECAPTCHA_SECRET_KEY` and
  `INDIGO_ENABLE_REGISTRATION_RECAPTCHA` (set the last to `false` to disable). (by @Epp-Seguridad-Industrial-S-A-S)
