from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import Customer


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('phone',)


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('phone',)
