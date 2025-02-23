from django.views.generic import TemplateView, ListView, UpdateView, FormView, CreateView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Transaction, Purchase, Company
from .forms import TransactionForm, PurchaseForm, PaymentForm, CompanyForm
from django.urls import reverse_lazy
from customers.models import Profile, Payment
from django.utils import timezone 
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from products.models import Product
from django.contrib.auth.models import User
from dashboards.models import Notification
from django.contrib import messages
from products.forms import ProductForm




@method_decorator(never_cache, name='dispatch')
class UserDashboardView(LoginRequiredMixin, CreateView):
    template_name = 'dashboards/user_dashboard.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = get_object_or_404(Profile.objects.select_related('user'), user=user)
        context['profile'] = profile
        context['user_payments'] = Payment.objects.select_related('profile').filter(profile=profile)
    
        return context
    
    
    def form_valid(self, form):
        # Automatically set the current user as the product owner
        form.instance.user = self.request.user

        # Save the form data
        response = super().form_valid(form)

        # Create a notification for all users about the new product
        users = User.objects.exclude(id=self.request.user.id)  # Exclude the current user (product creator)
        for user in users:
            Notification.objects.create(
                user=user,
                product=form.instance,
                message=f"New product added: {form.instance.name}",
            )

        # Add success message for the notification
        messages.success(self.request, 'Product added and notifications sent to customers!')

        return response
        

@method_decorator(never_cache, name='dispatch')
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView, FormView):
    template_name = 'dashboards/admin_dashboard.html'
    form_class = PaymentForm
    success_url = reverse_lazy('admin_dashboard')
    
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.first() 
        customer = Profile.objects.count()
        customers_profiles = Profile.objects.all()
        product = Product.objects.count()
        
            
        context['company_total'] = company.total
        context['company_balance'] = company.balance
        context['company_profit'] = company.profit            
        context['total_customers'] = customer
        context['customers_profiles'] = customers_profiles
        context['company_funds_out'] = company.funds_out
        context['total_products'] = product
        # context['total_purchases'] = purchase
        return context
    
    
    def form_valid(self, form):
        payment = form.save(commit=False)
        
        # تعيين تاريخ الدفع إذا لم يكن محددًا
        if not payment.payment_date:
            payment.payment_date = timezone.now()
        
        payment.save()
        
        # تحديث بيانات الملف الشخصي
        profile = payment.profile
        profile.ballance = F('ballance') + payment.amount
        profile.total_payment = F('total_payment') + payment.amount
        profile.save()

        # إعادة التوجيه إلى لوحة تحكم المستخدم
        return HttpResponseRedirect(reverse_lazy('admin_dashboard'))



def sidebar_counts(request):
    purchase = Purchase.objects.count()
    transaction = Transaction.objects.count()
    return {'purchase': purchase, 'transaction': transaction}






@method_decorator(never_cache, name='dispatch')
class PurchaseProductView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Purchase  
    template_name = 'operations/purchase.html'
    context_object_name = 'purchases'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_queryset(self):
        return Purchase.objects.select_related()




    
@method_decorator(never_cache, name='dispatch')
class PurchachesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'operations/edit_purchase.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_success_url(self):
        return reverse_lazy ('purchase_list')
    
    
    
    
@method_decorator(never_cache, name='dispatch')
class TransactionDetailView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'operations/transaction.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_queryset(self):
        return Transaction.objects.select_related()




@method_decorator(never_cache, name='dispatch')
class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'operations/transaction_confirm.html'
    
    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('transaction_list')