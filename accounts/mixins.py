from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return self.request.user.role in self.allowed_roles
    
    def handle_no_permission(self):
        return HttpResponse("You don't have permission to access this page.")