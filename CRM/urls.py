"""
URL configuration for CRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),

    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('myaccount/', views.myaccount, name='myaccount'),

    path('log-in/', views.user_login, name='login'),
    path('sign-up/', views.signup, name='signup'),
    path('log-out/', views.user_logout, name='logout'),

    path('add-lead/', views.add_lead, name='addlead'),
    path('leads_list/', views.leads_list, name='leads_list'),
    path('leads_detail/<int:id>/', views.leads_detail, name='leads_detail'),
    path('leads_delete/<int:id>', views.leads_delete, name='leads_delete'),
    path('leads_edit/<int:id>/', views.edit_lead, name='leads_edit'),

    path('convert_lead/<int:id>/', views.convert_to_client, name='convert_lead'),

    path('clients_list', views.clients_list, name='clients_list'),
    path('add-client/', views.add_client, name='addclient'),
    path('clients_detail<int:id>', views.clients_detail, name='clients_detail'),
    path('clients_delete/<int:id>', views.clients_delete, name='clients_delete'),
    path('clients_edit/<int:id>/', views.edit_client, name='clients_edit'),
]
