from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product-detail'),
    path('collections/', views.CollectionViewSet.as_view({'get': 'list', 'post': 'create'}), name='collection-list'),
    path('collections/<int:pk>/', views.CollectionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='collection-detail'),
]
