from django.db import models
from decimal import Decimal

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('social', 'Социальные'),
        ('medical', 'Медицинские'),
        ('other', 'Тоже важно'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    collected = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='social')
    collected_all = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class HelpRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.email}"
