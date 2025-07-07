from django.shortcuts import render
from django.urls import path
from .views import login, logout
from . import views
from .views import request_food , success_page, food, viewfood, offerfood
from django.conf import settings
from django.conf.urls.static import static
from .views import volunteer , delete_financial_request
from .views import financial_requests, donate_money
from .views import submit_medical_request
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('volunteer/', volunteer, name='volunteer'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path("submit-feedback/", views.submit_feedback, name="submit_feedback"),
    path("thank-you/", views.thank_you, name="thank_you"),  # Add this!
    path("request_food/", request_food, name="request_food"),
    path ("success/", lambda request: render(request, "success.html"), name="success"),
    path ("food/", food, name="food"),
    path ("viewfood/", views.viewfood, name="viewfood"),
    path ("offerfood/", views.offerfood, name="offerfood"),
    path('relief-fund/',views.relief_fund, name='relief_fund'),
    path ('financial/', views.financial, name='financial'),
    path('financial/requests/', financial_requests, name='financial_requests'),
    path('donate/<int:request_id>/', donate_money, name='donate'),
    path('financial/requests/delete/<int:request_id>/', delete_financial_request, name='delete_financial_request'),
    path('shelter/', views.shelter, name='shelter'),
    path('request_shelter/', views.request_shelter, name='request_shelter'),
    path('offer_shelter/', views.offer_shelter, name='offer_shelter'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('disaster_reports/',views.disaster_reports, name='disaster_reports'),
    path('disasterreport/', views.disasterreport, name='disasterreport'),
    path('medical-assistance',views.medical_assistance, name='medical_assistance'),
    path ("request-medical-help/", views.submit_medical_request, name="submit_medical_request"),
    path ("medical-success/", views.medical_request_success, name="medical_request_success"),
    path ("doctors-dashboard/", views.doctors_dashboard, name="doctors_dashboard"),
    path("mark-as-resolved/<int:request_id>/", views.mark_as_resolved, name="mark_as_resolved"),
  path('logout/',logout, name='logout' )
    ]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
