from django.urls import path

from . import views

urlpatterns = [
    path('news/', views.news, name='news'),
    path('people/', views.people, name='people'),
    path('publications/', views.publications, name='publications'),
    path('software/<int:software_id>/', views.software, name='software'),
    path('software/<int:software_id>/authors', views.authors_of_software, name='software_authors'),
    path('software/', views.software_list, name='software_list'),

]
