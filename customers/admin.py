from django.contrib import admin
from . models import Profile, Payment




# PaymentInline
class PaymentInline(admin.TabularInline):
    model = Payment
    fields = ('payment_date', 'amount')  # إظهار هذه الحقول فقط
    readonly_fields = ('payment_date', 'amount')  # جعل الحقول غير قابلة للتعديل
    extra = 0  # إضافة سطر فارغ لإضافة دفعة جديدة (زر "Add another Payment" سيظل يعمل)

# Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'total_payment', 'total_profit')
    inlines = [PaymentInline]  # إضافة الـ PaymentInline إلى ProfileAdmin

    def save_model(self, request, obj, form, change):
        # حفظ الـ Profile أولاً
        super().save_model(request, obj, form, change)
        
        # إعادة حساب total_payment بناءً على الدفعات
        total_payment = sum(payment.amount for payment in obj.payments.all())
        obj.total_payment = total_payment
        obj.save()

admin.site.register(Profile, ProfileAdmin)

# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # حفظ الـ Payment أولاً
        super().save_model(request, obj, form, change)
        
        # التأكد من وجود Profile مرتبط بالـ Payment
        profile = obj.profile
        
        # التأكد من أن المبلغ في Payment ليس صفرًا
        if obj.amount > 0:
            # إضافة المبلغ إلى total_payment في الـ Profile
            profile.total_payment += obj.amount
            profile.save()


admin.site.register(Payment, PaymentAdmin)