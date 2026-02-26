from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('query/<int:query_id>/', views.query_view, name='query_view'),
]