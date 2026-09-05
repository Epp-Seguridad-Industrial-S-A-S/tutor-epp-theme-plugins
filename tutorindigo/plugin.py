from __future__ import annotations

import os
from glob import glob
import typing as t

import importlib_resources
from tutor import hooks
from tutormfe.hooks import MFE_APPS, PLUGIN_SLOTS
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__


################# Configuration
config: t.Dict[str, t.Dict[str, t.Any]] = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "WELCOME_MESSAGE": "The place for all your online learning",
        "PRIMARY_COLOR": "#073784",  # Indigo
        "ENABLE_DARK_TOGGLE": True,
        # Footer links are dictionaries with a "title" and "url"
        # To remove all links, run:
        # tutor config save --set INDIGO_FOOTER_NAV_LINKS=[]
        "FOOTER_NAV_LINKS": [
            {"title": "About Us", "url": "/about"},
            {"title": "Blog", "url": "/blog"},
            {"title": "Donate", "url": "/donate"},
            {"title": "Terms of Service", "url": "/tos"},
            {"title": "Privacy Policy", "url": "/privacy"},
            {"title": "Help", "url": "/help"},
            {"title": "Contact Us", "url": "/contact"},
        ],
        # --- Self-registration ("autoregistro") reCAPTCHA ---
        # Google reCAPTCHA v2 "I'm not a robot" checkbox keys. Set both via
        #   tutor config save --set INDIGO_RECAPTCHA_SITE_KEY=... --set INDIGO_RECAPTCHA_SECRET_KEY=...
        # Leaving them blank + ENABLE_REGISTRATION_RECAPTCHA=false keeps registration unchanged.
        "RECAPTCHA_SITE_KEY": "",
        "RECAPTCHA_SECRET_KEY": "",
        "ENABLE_REGISTRATION_RECAPTCHA": True,
        # Only relevant if you switch the keys to reCAPTCHA v3 (score based). Keep null for v2.
        "RECAPTCHA_MIN_SCORE": None,
        # pip requirement baked into the openedx image; pin to a tag for reproducible builds.
        "REGISTRATION_CAPTCHA_PACKAGE": (
            "git+https://github.com/Epp-Seguridad-Industrial-S-A-S/"
            "epp-registration-captcha.git@v0.2.0"
        ),
        # "Confirm email" double-entry field on the registration form (catches values
        # that don't match; does NOT check the domain -- see ENABLE_EMAIL_DOMAIN_CHECK).
        "REQUIRE_CONFIRM_EMAIL": True,
        # Reject registration if the email's domain has no MX/A record (fails open on
        # DNS errors -- see epp_registration_captcha.forms.domain_can_receive_mail).
        "ENABLE_EMAIL_DOMAIN_CHECK": True,
    },
    "unique": {},
    "overrides": {},
}

# Theme templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutorindigo") / "templates")
)
# This is where the theme is rendered in the openedx build directory
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("indigo", "build/openedx/themes"),
        ("indigo/env.config.jsx", "plugins/mfe/build/mfe"),
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_items(
    [
        r"indigo/lms/static/sass/partials/lms/theme/",
        r"indigo/cms/static/sass/partials/cms/theme/",
    ]
)


# init script: set theme automatically
with open(
    os.path.join(
        str(importlib_resources.files("tutorindigo") / "templates"),
        "indigo",
        "tasks",
        "init.sh",
    ),
    encoding="utf-8",
) as task_file:
    hooks.Filters.CLI_DO_INIT_TASKS.add_item(("lms", task_file.read()))


# Override openedx & mfe docker image names
@hooks.Filters.CONFIG_DEFAULTS.add(priority=hooks.priorities.LOW)
def _override_openedx_docker_image(
    items: list[tuple[str, t.Any]]
) -> list[tuple[str, t.Any]]:
    openedx_image = ""
    mfe_image = ""
    for k, v in items:
        if k == "DOCKER_IMAGE_OPENEDX":
            openedx_image = v
        elif k == "MFE_DOCKER_IMAGE":
            mfe_image = v
    if openedx_image:
        items.append(("DOCKER_IMAGE_OPENEDX", f"{openedx_image}-indigo"))
    if mfe_image:
        items.append(("MFE_DOCKER_IMAGE", f"{mfe_image}-indigo"))
    return items


# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"INDIGO_{key}", value) for key, value in config["defaults"].items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"INDIGO_{key}", value) for key, value in config["unique"].items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))


#  MFEs that are styled using Indigo
indigo_styled_mfes = [
    "learning",
    "learner-dashboard",
    "profile",
    "account",
    "discussions",
]

hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            f"mfe-dockerfile-post-npm-install-{mfe}",
            """
           
RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
RUN npm install '@edx/frontend-component-header@npm:@edly-io/indigo-frontend-component-header@^3.2.2'
RUN npm install '@edx/brand@git+https://github.com/Epp-Seguridad-Industrial-S-A-S/epp-brand.git'

""",
        )
        for mfe in indigo_styled_mfes
    ]
)


hooks.Filters.ENV_PATCHES.add_item(
    (
        "mfe-dockerfile-post-npm-install-authn",
        "RUN npm install '@edx/brand@git+https://github.com/Epp-Seguridad-Industrial-S-A-S/epp-brand.git'",
    )
)


# Build the authn (logistration) MFE from the EPP fork instead of upstream. The fork adds
# the Google reCAPTCHA widget to the registration form; the token is verified server-side
# by the epp-registration-captcha package (see the openedx settings patches below).
EPP_AUTHN_MFE_REPOSITORY = (
    "https://github.com/Epp-Seguridad-Industrial-S-A-S/frontend-app-authn.git"
)
EPP_AUTHN_MFE_VERSION = "epp/recaptcha-sumac"  # branched off open-release/sumac.master


@MFE_APPS.add()
def _epp_override_authn_mfe(mfes: dict) -> dict:
    mfes["authn"] = {
        "repository": EPP_AUTHN_MFE_REPOSITORY,
        "port": 1999,  # authn's port in tutor-mfe CORE_MFE_APPS
        "version": EPP_AUTHN_MFE_VERSION,
    }
    return mfes


# Install the server-side reCAPTCHA verifier (registration extension form) into the
# openedx image. One patch covers the production and development image stages.
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-dockerfile-post-python-requirements",
        "RUN pip install '{{ INDIGO_REGISTRATION_CAPTCHA_PACKAGE }}'",
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "mfe-dockerfile-post-npm-install-authoring",
        "RUN npm install '@edx/brand@git+https://github.com/Epp-Seguridad-Industrial-S-A-S/epp-brand.git'",
    )
)

# Include js file in lms main.html, main_django.html, and certificate.html

hooks.Filters.ENV_PATCHES.add_items(
    [
        # for production
        (
            "openedx-common-assets-settings",
            """
javascript_files = ['base_application', 'application', 'certificates_wv']
dark_theme_filepath = ['indigo/js/dark-theme.js']

for filename in javascript_files:
    if filename in PIPELINE['JAVASCRIPT']:
        PIPELINE['JAVASCRIPT'][filename]['source_filenames'] += dark_theme_filepath
""",
        ),
        # for development
        (
            "openedx-lms-development-settings",
            """
javascript_files = ['base_application', 'application', 'certificates_wv']
dark_theme_filepath = ['indigo/js/dark-theme.js']

for filename in javascript_files:
    if filename in PIPELINE['JAVASCRIPT']:
        PIPELINE['JAVASCRIPT'][filename]['source_filenames'] += dark_theme_filepath

MFE_CONFIG['INDIGO_ENABLE_DARK_TOGGLE'] = {{ INDIGO_ENABLE_DARK_TOGGLE }}

# Self-registration reCAPTCHA (verified server-side by epp-registration-captcha)
REGISTRATION_EXTENSION_FORM = "epp_registration_captcha.forms.RegistrationCaptchaForm"
EPP_ENABLE_REGISTRATION_RECAPTCHA = {{ INDIGO_ENABLE_REGISTRATION_RECAPTCHA }}
RECAPTCHA_PUBLIC_KEY = "{{ INDIGO_RECAPTCHA_SITE_KEY }}"
RECAPTCHA_PRIVATE_KEY = "{{ INDIGO_RECAPTCHA_SECRET_KEY }}"
{% if INDIGO_RECAPTCHA_MIN_SCORE is not none %}RECAPTCHA_MIN_SCORE = {{ INDIGO_RECAPTCHA_MIN_SCORE }}{% endif %}
MFE_CONFIG['RECAPTCHA_PUBLIC_KEY'] = "{{ INDIGO_RECAPTCHA_SITE_KEY }}"
MFE_CONFIG['ENABLE_REGISTRATION_RECAPTCHA'] = {{ INDIGO_ENABLE_REGISTRATION_RECAPTCHA }}

# Reject registrations whose email domain has no MX/A record (fails open on DNS errors)
EPP_ENABLE_EMAIL_DOMAIN_CHECK = {{ INDIGO_ENABLE_EMAIL_DOMAIN_CHECK }}

# "Confirm email" field on the registration form (catches values that don't match)
REGISTRATION_EXTRA_FIELDS = REGISTRATION_EXTRA_FIELDS if "REGISTRATION_EXTRA_FIELDS" in dir() else {}
REGISTRATION_EXTRA_FIELDS["confirm_email"] = "{{ 'required' if INDIGO_REQUIRE_CONFIRM_EMAIL else 'hidden' }}"
MFE_CONFIG['ENABLE_DYNAMIC_REGISTRATION_FIELDS'] = {{ INDIGO_REQUIRE_CONFIRM_EMAIL }}
""",
        ),
        (
            "openedx-lms-production-settings",
            """
MFE_CONFIG['INDIGO_ENABLE_DARK_TOGGLE'] = {{ INDIGO_ENABLE_DARK_TOGGLE }}

# Self-registration reCAPTCHA (verified server-side by epp-registration-captcha)
REGISTRATION_EXTENSION_FORM = "epp_registration_captcha.forms.RegistrationCaptchaForm"
EPP_ENABLE_REGISTRATION_RECAPTCHA = {{ INDIGO_ENABLE_REGISTRATION_RECAPTCHA }}
RECAPTCHA_PUBLIC_KEY = "{{ INDIGO_RECAPTCHA_SITE_KEY }}"
RECAPTCHA_PRIVATE_KEY = "{{ INDIGO_RECAPTCHA_SECRET_KEY }}"
{% if INDIGO_RECAPTCHA_MIN_SCORE is not none %}RECAPTCHA_MIN_SCORE = {{ INDIGO_RECAPTCHA_MIN_SCORE }}{% endif %}
MFE_CONFIG['RECAPTCHA_PUBLIC_KEY'] = "{{ INDIGO_RECAPTCHA_SITE_KEY }}"
MFE_CONFIG['ENABLE_REGISTRATION_RECAPTCHA'] = {{ INDIGO_ENABLE_REGISTRATION_RECAPTCHA }}

# Reject registrations whose email domain has no MX/A record (fails open on DNS errors)
EPP_ENABLE_EMAIL_DOMAIN_CHECK = {{ INDIGO_ENABLE_EMAIL_DOMAIN_CHECK }}

# "Confirm email" field on the registration form (catches values that don't match)
REGISTRATION_EXTRA_FIELDS = REGISTRATION_EXTRA_FIELDS if "REGISTRATION_EXTRA_FIELDS" in dir() else {}
REGISTRATION_EXTRA_FIELDS["confirm_email"] = "{{ 'required' if INDIGO_REQUIRE_CONFIRM_EMAIL else 'hidden' }}"
MFE_CONFIG['ENABLE_DYNAMIC_REGISTRATION_FIELDS'] = {{ INDIGO_REQUIRE_CONFIRM_EMAIL }}
""",
        ),
    ]
)


# Apply patches from tutor-indigo
for path in glob(
    os.path.join(
        str(importlib_resources.files("tutorindigo") / "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


for mfe in indigo_styled_mfes:
    PLUGIN_SLOTS.add_item(
        (
            mfe,
            "footer_slot",
            """ 
            {
                op: PLUGIN_OPERATIONS.Hide,
                widgetId: 'default_contents',
            },
            {
                op: PLUGIN_OPERATIONS.Insert,
                widget: {
                    id: 'default_contents',
                    type: DIRECT_PLUGIN,
                    priority: 1,
                    RenderWidget: <IndigoFooter />,
                },
            },
            {
                op: PLUGIN_OPERATIONS.Insert,
                widget: {
                    id: 'read_theme_cookie',
                    type: DIRECT_PLUGIN,
                    priority: 2,
                    RenderWidget: AddDarkTheme,
                },
            },
  """,
        ),
    )
