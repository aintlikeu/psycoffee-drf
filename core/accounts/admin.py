from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Customer
from accounts.forms import CustomerChangeForm, CustomerCreationForm


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ('id', 'first_name', 'last_name', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'phone')
    ordering = ('id', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone', 'password1', 'password2', 'is_active'),
        }),
    )


admin.site.register(Customer, CustomerAdmin)
