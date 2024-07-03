from rest_framework import permissions
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')



# to allow read-only access for all users and full access only for admin users.
class AdminOrReadOnly(permissions.IsAdminUser):
    message = ' ADMIN or read only. '
    # has_permission used for listing only(usally actions are not taken considerations  )
    def has_permission(self, request, view):
        # return super  ().has_permission(request=request,view=view)
        
        # will tell if i m admin or not(readonly)
        admin_permission = super().has_permission(request=request, view=view)
        
        if request.method == 'GET' or admin_permission:
            return True
        return False
    

class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )



# allow edit if loggedin user posted that review
class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request/ safe_method means get request
            return True  #get request means readonly  i.e. true
        else: #if post request i.e. check if review_user is same as user who is logged in
            if obj.review_user == request.user:
                return True
            else:
                return False