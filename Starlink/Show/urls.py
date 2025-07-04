from django.urls import path
from .views import *
 
urlpatterns = [
	path('', index, name='index'),
    
	path('technology', technology, name='technology'),
    path('help_center', help_center, name='help_center'),
    path('map', map, name='map'),
    path('order', order, name='order'),
    path('residential', residential, name='residential'),
    path('roam', roam, name='roam'),
    path('service_plans', service_plans, name='service_plans'),
    path('service_plans_business', service_plans_business, name='service_plans_business'),
    path('sign_in', sign_in, name='sign_in'),
    path('specifications', specifications, name='specifications'),
    path('update', update, name='update'),
    path('video_guides', video_guides, name='video_guides'),
    path('index_business', index_business, name='index_business'),
    path('business_aviation', business_aviation, name='business_aviation'),
    path('business_direct_to_cell', business_direct_to_cell, name='business_direct_to_cell'),
    path('business_fixed_site', business_fixed_site, name='business_fixed_site'),
    path('business_maritime', business_maritime, name='business_maritime'),
    path('business_mobility', business_mobility, name='business_mobility'),
]