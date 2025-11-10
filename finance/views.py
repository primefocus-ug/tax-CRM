from django.shortcuts import render
from .models import Debtor, Creditor, Expense
from django.shortcuts import redirect
from django.urls import reverse
from .forms import ExpenseForm

def finance_dashboard(request):
    debtors = Debtor.objects.all()
    creditors = Creditor.objects.all()
    expenses = Expense.objects.all()



    total_debt = sum(d.amount_owed for d in debtors if not d.is_paid)
    total_credit = sum(c.amount_to_pay for c in creditors if not c.is_paid)
    total_expense = sum(e.amount for e in expenses)

    context = {
        'debtors': debtors,
        'creditors': creditors,
        'expenses': expenses,
        'total_debt': total_debt,
        'total_credit': total_credit,
        'total_expense': total_expense,
    }
    return render(request, 'finance/dashboard.html', context)

def expenses_list_view(request):
    expenses = Expense.objects.all()
    context = {
        'expenses': expenses,
        'active_icon': 'expenses',
    }
    return render(request, 'finance/expenses_list.html', context)

def expense_create_view(request):
    from .forms import ExpenseForm
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance:expenses_list')
    else:
        form = ExpenseForm()
    
    context = {
        'form': form,
        'active_icon': 'expenses',
    }
    return render(request, 'finance/expense_form.html', context)

def add_expense(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Save the new object instance to the database
            form.save()
            # Redirect to a success page or the expense list
            return redirect('expense_list') # Replace 'expense_list' with a real URL name
    else:
        # If it's a GET request, create an empty form
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

def expense_update_view(request, pk):
    from .forms import ExpenseForm
    expense = Expense.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('finance:expenses_list')
    else:
        form = ExpenseForm(instance=expense)
    
    context = {
        'form': form,
        'active_icon': 'expenses',
    }
    return render(request, 'finance/expense_form.html', context)


def expense_delete_view(request, pk):
    expense = Expense.objects.get(pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('finance:expenses_list')
    
    context = {
        'expense': expense,
        'active_icon': 'expenses',
    }
    return render(request, 'finance/expense_confirm_delete.html', context)
       