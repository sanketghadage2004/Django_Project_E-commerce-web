from rest_framework import permissions

class GetRequestOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.mothod == 'GET':
            return True
        return False