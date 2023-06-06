from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import Customer, Patient


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('email',)


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('email',)


class PatientChangeForm(UserChangeForm):
    class Meta:
        model = Patient
        fields = ('email',)


class PatientCreationForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ('email',)