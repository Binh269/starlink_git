from django.urls import path
from .views import *
 
urlpatterns = [
	path('', index),
    
	path('technology', technology, name='technology'),
    path('help_center', help_center, name='help_center'),
    path('map', map, name='map'),
    path('order', order, name='order'),
    path('residential', residential, name='residential'),
    path('roam', roam, name='roam')
]