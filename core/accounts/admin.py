from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Customer, Patient
from accounts.forms import CustomerChangeForm, CustomerCreationForm, PatientCreationForm, PatientChangeForm


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active'),
        }),
    )


class PatientAdmin(UserAdmin):
    add_form = PatientCreationForm
    form = PatientChangeForm
    model = Patient
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active'),
        }),
    )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Patient, PatientAdmin)
