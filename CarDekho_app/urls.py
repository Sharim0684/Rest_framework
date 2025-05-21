from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.car_list_view,name='car_list'),
    path('<int:pk>/',views.car_detail_view,name='car_detail'),
    path('showroom',views.Showroom_View.as_view(),name='showroom_View'),
    path('showroom/<int:pk>/',views.Showroom_details.as_view(),name='showroom_details'),
    path('review/',views.Reviewlist.as_view(),name='review_View'),
    path('review/<int:pk>/',views.ReviewDetails.as_view(),name='review_details'),
]