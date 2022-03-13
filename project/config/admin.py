from django.contrib import admin


class ProjectAdmin(admin.AdminSite):
    site_header = 'JSC Order Tracking'
    site_title = 'JSC Order Tracker'
    index_title = site_header
    enable_nav_sidebar = True