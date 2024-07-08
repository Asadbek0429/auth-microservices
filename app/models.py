from uuid import uuid4
from django.db import models


class Services(models.Model):
    secret_key = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SSOToken(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)

    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service.name
