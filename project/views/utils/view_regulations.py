def group_check(self, check_groups=None):
    if not self.request.user.is_active:
        return False
    if self.request.user.is_superuser:
        return True
    return self.request.user.groups.filter(name__in=check_groups).exists()
