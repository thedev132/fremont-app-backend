from django.contrib.admin.apps import AdminConfig


class CoreAdminConfig(AdminConfig):
    default_site = "fremont_app.admin.CoreAdmin"