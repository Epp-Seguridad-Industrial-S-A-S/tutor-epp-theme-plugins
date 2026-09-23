<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Bugfix] Restored full `epp-theme` (`lms/` + `cms/`, branding included) vendoring into the
  `indigo` theme image, after a prior fragment briefly narrowed it to just
  `lms/templates/shoppingcart/`. The site-wide crash that prompted that narrowing
  (`NoReverseMatch: session_language`) was traced to host-side contamination from an unrelated
  package mixup, not to `epp-theme` itself, which renders cleanly on this install. Deployments
  that already picked up the narrow fragment will regain their logo/colors/header/footer on the
  next rebuild. (by @Epp-Seguridad-Industrial-S-A-S)
