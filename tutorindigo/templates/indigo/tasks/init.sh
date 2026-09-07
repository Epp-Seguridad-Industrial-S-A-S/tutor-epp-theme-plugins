# Assign themes only if no other theme exists yet
./manage.py lms shell -c "
import sys
from django.conf import settings
from django.contrib.sites.models import Site

# Make the Site at SITE_ID canonical: its domain must be LMS_HOST, because request-less
# ACE emails (activation) build absolute URLs from Site.objects.get_current(). Left alone,
# it stays Django's default 'example.com' and leaks broken/phishy links into those emails.
canonical = '{{ LMS_HOST }}'
current = Site.objects.filter(pk=settings.SITE_ID).first()
if current and current.domain != canonical:
    clash = Site.objects.filter(domain=canonical).exclude(pk=current.pk).first()
    if clash:
        clash.domain = 'legacy-%d.%s' % (clash.pk, canonical)
        clash.name = clash.domain
        clash.save()
    current.domain = canonical
    current.name = canonical
    current.save()
if current and not current.themes.exists():
    current.themes.create(theme_dir_name='indigo')

def assign_theme(domain):
    site, _ = Site.objects.get_or_create(domain=domain)
    if not site.themes.exists():
        site.themes.create(theme_dir_name='indigo')

assign_theme('{{ LMS_HOST }}')
assign_theme('{{ LMS_HOST }}')
assign_theme('{{ LMS_HOST }}:8000')
assign_theme('{{ CMS_HOST }}')
assign_theme('{{ CMS_HOST }}:8001')
assign_theme('{{ PREVIEW_LMS_HOST }}')
assign_theme('{{ PREVIEW_LMS_HOST }}:8000')
"
