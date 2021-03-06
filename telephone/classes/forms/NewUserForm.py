from django import forms


class NewUserForm(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    uid = forms.CharField(max_length=50)
    token = forms.CharField(max_length=50)
    userKey = forms.CharField(max_length=50)
    secretKey = forms.CharField(max_length=50)
    userEmail = forms.EmailField(max_length=30)
    userPassword = forms.CharField(max_length=30)
    profilePhoneNumber = forms.CharField(max_length=20)
    userName = forms.CharField(max_length=30)
    customerNumber = forms.CharField(max_length=10)
