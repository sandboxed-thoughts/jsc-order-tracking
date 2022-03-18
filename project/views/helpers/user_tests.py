from operator import contains
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminGroupTest(UserPassesTestMixin):
    def _test_func(self):
        return self.user.groups(contains="Administrators")