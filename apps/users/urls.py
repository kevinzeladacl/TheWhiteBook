from django.urls import path,include
from django.contrib import admin
from . import views

 


urlpatterns = [
    
	#custom dapi
	path(r'^resetpassword$', views.resetPasswordView, name='resetPasswordView'),
]
	
 