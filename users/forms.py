
from django.contrib.auth.forms import UserCreationForm
from .models import UserBookings
from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'input-box'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'input-box'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'input-box'}), label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'input-box'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-box'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'input-box'}), label='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email




# class UserBookingsForm(forms.ModelForm):

#     full_name = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'id': "full-name", 'placeholder': 'Full Name'}),
#         required=True
#     )
#     phone_number = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'id': "phone-number", 'placeholder': 'Phone Number'}),
#         required=True
#     )
#     number_of_adults = forms.IntegerField(
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'id': "number-of-adults", 'placeholder': 'Number of Adults'}),
#         required=True
#     )
#     number_of_children = forms.IntegerField(
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'id': "number-of-children", 'placeholder': 'Number of Children (Optional)'}),
#         required=False
#     )
#     number_of_rooms = forms.IntegerField(
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'id': "number-of-rooms", 'placeholder': 'Number of Rooms'}),
#         required=True
#     )
#     travel_date = forms.DateField(
#         widget=forms.DateInput(attrs={'class': 'form-control', 'id': "travel-date", 'placeholder': 'Travel Date'}),
#         required=True
#     )
#     include_travelling = forms.BooleanField(
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': "include-travelling"}),
#         required=False
#     )
#     special_requests = forms.CharField(
#         widget=forms.Textarea(attrs={'class': 'form-control', 'id': "special-requests", 'placeholder': 'Any special requests'}),
#         required=False
#     )
    
#     class Meta:
#         model = UserBookings
#         fields = ['full_name', 'phone_number', 'number_of_adults', 'number_of_children', 'number_of_rooms', 'travel_date', 'include_travelling', 'special_requests']



class UserBookingsForm(forms.ModelForm):
    class Meta:
        model = UserBookings
        fields = [
            'full_name',
            'phone_number',
            'number_of_adults',
            'number_of_children',
            'number_of_rooms',
            'include_travelling',
            'special_requests',
            'paid'
        ]