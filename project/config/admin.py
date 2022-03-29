from email.policy import default
from django.contrib import admin
from decouple import config


class ProjectAdmin(admin.AdminSite):
    site_header = config("SITE_HEADER", default="JSC Order Tracking")
    site_title = config("SITE_TITLE", default="JSC Order Tracker")
    index_title = config("INDEX_TITLE", default=site_title)
    enable_nav_sidebar = config("ENABLE_ADMIN_SIDEBAR", default=True)
