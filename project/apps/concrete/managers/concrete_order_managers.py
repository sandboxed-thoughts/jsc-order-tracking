from django.db import models


class WallManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_wall=True)


class FootingsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_footings=True)


class FlatworkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_flatwork=True)
