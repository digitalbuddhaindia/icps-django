from rest_framework.permissions import BasePermission


class IsDistrictUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_district_user