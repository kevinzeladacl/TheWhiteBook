from django import forms
from apps.users.models import *
from apps.projects.models import *

class LoginForm(forms.Form):
    email = forms.CharField(max_length=30,
       widget=forms.TextInput(attrs={
           'class': 'form-control',
           'placeholder':"Ingresa tu Correo",
           'required': 'true',
       }))
    password = forms.CharField(max_length=30,
       widget=forms.TextInput(attrs={
           'type': 'password',
           'class': 'form-control',
           'placeholder':"Ingresa tu Clave",
           'required': 'true'
       }))

class RegisterForm(forms.Form):
    email = forms.CharField(max_length=30,
       widget=forms.TextInput(attrs={
           'class': 'form-control',
           'placeholder':"Ingresa tu Correo",
           'required': 'true',
       }))
    password = forms.CharField(max_length=30,
       widget=forms.TextInput(attrs={
           'type': 'password',
           'class': 'form-control',
           'placeholder':"Ingresa tu Clave",
           'required': 'true'
       }))


class updateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email','type_user')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
             'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),

             'type_user': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
 
        }



class createProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'required': 'true',
                'placeholder': 'Nombre del proyecto...'
            }),
     
        }

class createChapterForm(forms.ModelForm):
    
    class Meta:
        model = Chapter
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'required': 'true',
                'placeholder': 'Nombre del proyecto...'
            }),
     
        }



class writeChapterForm(forms.ModelForm):
    
    class Meta:
        model = Chapter
        fields = ('body',)
 