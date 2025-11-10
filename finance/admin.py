
from django.contrib import admin
from .models import Debtor, Creditor, Expense

admin.site.register(Debtor)
admin.site.register(Creditor)
admin.site.register(Expense)
