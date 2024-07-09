from django.contrib.admin.sites import AdminSite


class CoreAdmin(AdminSite):
    site_header = "Fremont ASB"

    def has_permission(self, request):
        return request.user.is_active