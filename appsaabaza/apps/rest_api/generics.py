from rest_framework import generics

from .filters import AppsaabazaObjectPermissionsFilter
from .permissions import AppsaabazaPermission


class GenericAPIView(generics.GenericAPIView):
    filter_backends = (AppsaabazaObjectPermissionsFilter,)
    permission_classes = (AppsaabazaPermission,)


class ListAPIView(generics.ListAPIView):
    """
    requires:
        object_permission = {'GET': ...}
    """
    filter_backends = (AppsaabazaObjectPermissionsFilter,)
    # permission_classes is required for the EventListAPIView
    # when Actions objects support ACLs then this can be removed
    # as was intented.
    permission_classes = (AppsaabazaPermission,)


class ListCreateAPIView(generics.ListCreateAPIView):
    """
    requires:
        object_permission = {'GET': ...}
        view_permission = {'POST': ...}
    """
    filter_backends = (AppsaabazaObjectPermissionsFilter,)
    permission_classes = (AppsaabazaPermission,)


class RetrieveAPIView(generics.RetrieveAPIView):
    """
    requires:
        object_permission = {
            'GET': ...,
        }
    """
    filter_backends = (AppsaabazaObjectPermissionsFilter,)


class RetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    requires:
        object_permission = {
            'DELETE': ...,
            'GET': ...,
        }
    """
    filter_backends = (AppsaabazaObjectPermissionsFilter,)


class RetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    requires:
        object_permission = {
            'GET': ...,
            'PATCH': ...,
            'PUT': ...
        }
    """
    filter_backends = (AppsaabazaObjectPermissionsFilter,)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    requires:
        object_permission = {
            'DELETE': ...,
            'GET': ...,
            'PATCH': ...,
            'PUT': ...
        }
    """
    filter_backends = (AppsaabazaObjectPermissionsFilter,)
