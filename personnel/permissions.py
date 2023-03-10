from rest_framework import permissions

class IsStaffOrReadOnly(permissions.IsAdminUser):

    message = "You do not have permission perform this action"

#! Departments can only do get after users log in, and post can only be done if they are user staff.
#! Departmanları ancak kullanıcı girişi yaptıktan görüntüleyebilir ve post, delete, patch ve put işlemlerini ancak kullanıcı user ise yapılabilir.

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)



#! Each registered user will be able to view the detailed information of the personnel, but only the user who created the personnel can delete and put.
#! Kayıtlı her kullanıcı personele ait detaylı bilgileri görebilecek ancak sadece personeli oluşturan staff user delete, put ve patch işlemlerini yapabilir.
class IsOwnerAndStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.is_staff and (obj.create_user == request.user))