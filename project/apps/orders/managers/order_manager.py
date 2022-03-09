from django.db import models

class NonCompleteOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_complete=False)
    
class CompleteOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_complete=True)