from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('accountant', 'Accountant'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # For accountants
    clients = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='accountants',
        blank=True,
        limit_choices_to={'role': 'client'}
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_client(self):
        return self.role == 'client'

    @property
    def is_accountant(self):
        return self.role == 'accountant' 