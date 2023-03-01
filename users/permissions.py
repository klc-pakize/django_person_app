from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user.is_staff or (obj.user == request.user))  # obj.user == request.user = Are the owner of the profile object and the user who made the request the same user ? If true, it can perform the update