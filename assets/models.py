from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from simple_history.models import HistoricalRecords

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Department(TimeStampedModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    # is_manager = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='departments')
    ROLE_CHOICES = (
                ('ADMIN', 'Administrator'),
                ('MANAGER','Manager'),
                ('EMPLOYEE','Employee'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    @property
    def is_manager_or_admin(self):
        return self.role in ['ADMIN', 'MANAGER'] or self.is_superuser




class Asset(TimeStampedModel):
    ASSET_TYPES = (
                ('LAPTOP', 'Laptop'),
                ('MONITOR','Monitor'),
                ('PHONE','Phone'),
                ('FURNITURE', 'Furniture'))
    
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"
    
class MaintenanceLog(TimeStampedModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_logs')
    description = models.TextField(max_length=100)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    date_repaired = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.asset} ({self.date_repaired})"


