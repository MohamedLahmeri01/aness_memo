from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('client/', views.MyClientPaymentsView.as_view(), name='client-payments'),
    path('freelancer/', views.MyFreelancerPaymentsView.as_view(), name='freelancer-payments'),
    path('admin/', views.AdminPaymentListView.as_view(), name='admin-payments'),
    path('<uuid:payment_id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('<uuid:payment_id>/update-status/', views.UpdatePaymentStatusView.as_view(), name='update-payment-status'),
]
