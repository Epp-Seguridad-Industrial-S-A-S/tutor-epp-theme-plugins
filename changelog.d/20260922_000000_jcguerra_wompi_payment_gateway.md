<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- 💥[Feature] Replaced the Mercado Pago shopping-cart payment processor with Wompi.
  New ``INDIGO_WOMPI_PUBLIC_KEY``, ``INDIGO_WOMPI_INTEGRITY_SECRET``, ``INDIGO_WOMPI_EVENTS_SECRET``
  and ``INDIGO_WOMPI_CHECKOUT_URL`` settings configure the ``Wompi`` ``CC_PROCESSOR``; the
  Eventos webhook URL to register in the Wompi dashboard is
  ``<LMS root>/shoppingcart/wompi/webhook/``. Deployments still on Mercado Pago must set
  these before upgrading, since the Mercado Pago processor code was removed.
  (by @Epp-Seguridad-Industrial-S-A-S)
