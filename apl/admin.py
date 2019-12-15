from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class MyAdminSite(admin.AdminSite):
    site_header = _('Lendarium administration')
