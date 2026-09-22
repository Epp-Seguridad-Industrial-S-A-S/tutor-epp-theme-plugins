<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Bugfix] The `indigo` theme baked into the openedx image was missing all of its `lms`/`cms`
  templates and static assets (only `tasks/init.sh` survived a March 2025 cleanup) -- any
  template with no upstream edx-platform fallback, such as a shoppingcart payment processor's
  checkout form, crashed with `TemplateDoesNotExist`. The image now clones `epp-theme` and
  vendors its `lms/`/`cms/` directories into `/openedx/themes/indigo/` at build time.
  (by @Epp-Seguridad-Industrial-S-A-S)
