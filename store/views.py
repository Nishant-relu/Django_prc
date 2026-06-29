from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from store.pagination import DefaultPagination
from .filters import ProductFilter
from .models import Collection, Product, OrderItem, Review, Cart
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer, CartSerializer

# ================================Product==========================================
class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):

        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is linked to an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        
        return super().destroy(request, *args, **kwargs)

# ===============================Collection==================================================
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.product.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it contains products.'}, status=status.HTTP_403_FORBIDDEN)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ================================Review====================================================
class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_id'] = self.kwargs['product_pk']
        return context

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_pk'])

# ================================Cart====================================================

class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    