from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce
import json
from django.contrib import messages

from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill, SaleItem, Supplier
from .forms import SuperUserRegistrationForm


# Use login_required for class-based views
@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = "home.html"

    def get(self, request):        
        labels = []
        data = []        

        # Get stock items, excluding deleted ones
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')

        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)

        # Get 3 most recent sales and purchases
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        
        # Get supplier count for dashboard
        supplier_count = Supplier.objects.filter(is_deleted=False).count()
        
        # Get top selling products
        top_selling_products = SaleItem.objects.values(
            'stock__id', 
            'stock__name', 
            'stock__price'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_sales=Sum('totalprice'),
            # Calculate percentage change (for demo - random calculation)
            # In a real app, you'd compare with previous period
            sales_growth=ExpressionWrapper(
                (F('total_quantity') * 0.01), 
                output_field=FloatField()
            )
        ).order_by('-total_quantity')[:7]  # Get top 7 products
        
        # Process the data for the template
        for product in top_selling_products:
            # Determine if growth is positive or negative (demo logic)
            if product['sales_growth'] > 0:
                product['growth_class'] = 'text-success'
                product['growth_icon'] = 'bi-arrow-up'
            else:
                product['growth_class'] = 'text-danger'
                product['growth_icon'] = 'bi-arrow-down'
            
            # Convert the growth to percentage and absolute value
            product['sales_growth_pct'] = abs(round(product['sales_growth'] * 100, 1))

        context = {
            'labels': labels,
            'data': data,
            'labels_json': json.dumps(labels),
            'data_json': json.dumps(data),
            'sales': sales,
            'purchases': purchases,
            'supplier_count': supplier_count,
            'top_selling_products': top_selling_products
        }

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class AboutView(TemplateView):
    template_name = "about.html"


def register_superuser(request):
    if request.method == 'POST':
        form = SuperUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = form.cleaned_data['is_superuser']
            user.is_staff = form.cleaned_data['is_staff']
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = SuperUserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
