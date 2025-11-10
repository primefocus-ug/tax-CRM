from django.db import models
from customers.models import Customer
from django.utils import timezone

class Debtor(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} owes {self.amount_owed} UGX"

class Creditor(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=50, blank=True)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Creditor: {self.name} - {self.amount_to_pay} UGX"

class Expense(models.Model):
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_by = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.date} - {self.category}: {self.amount} UGX"