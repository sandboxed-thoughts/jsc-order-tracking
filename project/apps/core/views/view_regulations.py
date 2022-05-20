def group_check(user, check_groups=None):
    if not user.is_active:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=check_groups).exists()
