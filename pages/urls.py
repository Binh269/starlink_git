from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video-guides/', views.video_guides, name='video_guides'),
    path('update/', views.update, name='update'),
    path('technology/', views.technology, name='technology'),
    path('specifications/', views.specifications, name='specifications'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('service-plans/', views.service_plans, name='service_plans'),
    path('service-plans-business/', views.service_plans_business, name='service_plans_business'),
    path('roam/', views.roam, name='roam'),
    path('residential/', views.residential, name='residential'),
    path('order/', views.order, name='order'),
    path('map/', views.map, name='map'),
    path('help-center/', views.help_center, name='help_center'),
    path('business/', views.business, name='business'),
    path('business/mobility/', views.business_mobility, name='business_mobility'),
    path('business/maritime/', views.business_maritime, name='business_maritime'),
    path('business/fixed-site/', views.business_fixed_site, name='business_fixed_site'),
    path('business/direct-to-cell/', views.business_direct_to_cell, name='business_direct_to_cell'),
    path('business/aviation/', views.business_aviation, name='business_aviation'),
] 