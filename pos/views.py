import json
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, FloatField, F, DecimalField 
from django.db.models.functions import Coalesce
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
# Import all necessary models
from products.models import Product, Category
from sales.models import Sale
from finance.models import Debtor, Creditor, Expense 
from django.core.paginator import Paginator # Ensure this is imported for any list views


@login_required(login_url="/accounts/login/")
def index(request):
    """
    Renders the Combined Dashboard with Sales/POS and Financial statistics.
    """
    today = date.today()
    year = today.year
    
    # ----------------------------------------------------
    # 1. SALES/POS CALCULATIONS (Your original index logic)
    # ----------------------------------------------------
    monthly_earnings = []
    for month in range(1, 13):
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum('grand_total'), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
        Sum('grand_total'), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    if monthly_earnings:
        avg_month = format(sum(monthly_earnings) / 12, '.2f')
    else:
        avg_month = format(0.00, '.2f')

    top_products = Product.objects.annotate(quantity_sum=Coalesce(Sum(
        'saledetail__quantity'), 0)).order_by('-quantity_sum')[:3]

    top_products_names = [p.name for p in top_products]
    top_products_quantity = [p.quantity_sum for p in top_products]
    
    # ----------------------------------------------------
    # 2. FINANCE CALCULATIONS (Logic from finance_dashboard)
    # ----------------------------------------------------
    
    # Total Outstanding Debt (Owed TO the company)
    total_debt = Debtor.objects.filter(is_paid=False).aggregate(
        sum_owed=Coalesce(Sum('amount_owed'), 0.0, output_field=DecimalField())
    )['sum_owed']

    # Total Outstanding Credit
    total_credit = Creditor.objects.filter(is_paid=False).aggregate(
        sum_to_pay=Coalesce(Sum('amount_to_pay'), 0.0, output_field=DecimalField())
    )['sum_to_pay']

    # Total Expenses
    total_expense = Expense.objects.filter(date__year=year).aggregate(
        sum_expense=Coalesce(Sum('amount'), 0.0, output_field=DecimalField())
    )['sum_expense']
    
    # Net Position (format now)
    net_profit = total_credit - total_debt - total_expense
    
    # DETERMINE THE PROFIT CARD COLOR IN PYTHON
    if net_profit < 0:
        profit_card_class = "danger"
    else:
        profit_card_class = "success"

    # Recent Expenses (for the dashboard table)
    recent_expenses = Expense.objects.all().order_by('-date')[:5]

    # ----------------------------------------------------
    # 3. CONTEXT DICTIONARY
    # ----------------------------------------------------
    context = {
        # ... (other context items) ...
        
        # Finance Context (formatted for display)
        'total_debt': format(total_debt, '.2f'),
        'total_credit': format(total_credit, '.2f'),
        'total_expense': format(total_expense, '.2f'),
        'net_profit': format(net_profit, '.2f'),
        # NEW CONTEXT VARIABLE
        'profit_card_class': profit_card_class, 
        'recent_expenses': recent_expenses,
    }
    

    # 3. CONTEXT DICTIONARY
    # ----------------------------------------------------
    context = {
        # POS Context
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
        
        # Finance Context (formatted for display)
        'total_debt': format(total_debt, '.2f'),
        'total_credit': format(total_credit, '.2f'),
        'total_expense': format(total_expense, '.2f'),
        'net_profit': format(net_profit, '.2f'),
        'recent_expenses': recent_expenses,
    }
    
    return render(request, 'pos/index.html', context)


# NOTE: The 'finance_dashboard' view is now redundant if you map the main 
# dashboard URL to the 'index' view, you can delete it or rename it 
# if you want a separate finance view. 
# I recommend DELETING this if you are using 'index' as the main dashboard.
#
# @login_required(login_url="/accounts/login/")
# def finance_dashboard(request):
#     # ... (redundant logic)
#     return render(request, 'pos/index.html', context)

# ----------------------------------------------------
# 4. Expense List View (The list page that was broken)
# ----------------------------------------------------

def expenses_list_view(request):
    """
    Lists all recorded expenses with basic pagination.
    """
    # Fetch ALL expenses, ordered by newest first
    expenses = Expense.objects.all().order_by('-date') 
    
    # Pagination
    paginator = Paginator(expenses, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    # IMPORTANT: Ensure this renders the correct template!
    return render(request, 'finance/expenses_list.html', context)