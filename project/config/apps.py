from django.contrib.admin.apps import AdminConfig


class ProjectAdminConfig(AdminConfig):
    default_site = "config.admin.ProjectAdmin"
