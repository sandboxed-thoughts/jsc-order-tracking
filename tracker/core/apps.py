from django.contrib.admin.apps import AdminConfig


class JSCAdminConfig(AdminConfig):
    default_site = "core.admin.JSCAdmin"
