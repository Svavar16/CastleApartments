from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="apartment-index"),
    path('all_listing', views.all_listing, name="apartment_all_listing"),
    path('all_listing/<int:id>', views.get_apartment_by_id, name='apartment_details'),
    path('<int:id>', views.get_apartment_by_id, name='apartment_details'),
    path('create_apartment', views.create_apartment, name='create_apartment'),
    path('delete_apartment/<int:id>', views.delete_apartment, name='delete_apartment'),
    path('<int:id>/change_price', views.change_price, name='change_price'),
    path('get_three_random_apartments/', views.get_three_random_apartments, name="get_three_random_apartments"),
    path('get_newest_apartment/', views.get_newest_apartment, name="get_newest_apartment"),
    path('get_all_apartment_images/<int:id>', views.get_all_apartment_images, name="get_all_apartment_images")
]


