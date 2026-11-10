from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class RoleRequiredMixin(AccessMixin):
    """Verify that the current user has an allowed role."""
    allowed_roles = []
    def dispatch(self, request, *args, **kwargs):
        # 1. Check if user is logged in
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # 2. Check if user role is in the allowed list
        role = getattr(request.user, 'role', None)
        if role not in self.allowed_roles:
            # Redirect to their correct home base if they don't match
            if role == 'customer':
                return redirect('customer_index')
            elif role == 'driver':
                return redirect('driver_index')
            elif role == 'admin':
                return redirect('administrator_index')
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        """Redirect unauthenticated users to login with a next parameter."""
        return redirect(f'/auth/login/?next={self.request.path}')
