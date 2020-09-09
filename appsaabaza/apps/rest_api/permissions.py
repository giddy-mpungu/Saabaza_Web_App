from django.core.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission

from appsaabaza.apps.acls.models import AccessControlList
from appsaabaza.apps.permissions import Permission


class AppsaabazaPermission(BasePermission):
    def has_permission(self, request, view):
        required_permissions = getattr(
            view, 'appsaabaza_view_permissions', {}
        ).get(request.method, None)

        if required_permissions:
            try:
                Permission.check_user_permissions(
                    permissions=required_permissions, user=request.user
                )
            except PermissionDenied:
                return False
            else:
                return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        required_permissions = getattr(
            view, 'appsaabaza_object_permissions', {}
        ).get(request.method, None)

        if required_permissions:
            try:
                AccessControlList.objects.check_access(
                    obj=obj, permissions=required_permissions,
                    user=request.user
                )
            except PermissionDenied:
                return False
            else:
                return True
        else:
            return True