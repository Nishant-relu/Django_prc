from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count

class ProductList(ListCreateAPIView):

    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer(self, *args, **kwargs):
    #     return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetail(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = self.get_object(id)
        if product.orderitems.count() > 0:
            return Response({'error': "Product cannot be deleted because linked to the order item"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# =================================================Collection======================================================#

class CollectionList(ListCreateAPIView):

    queryset = Collection.objects.annotate(product_count=Count('product')).all()
    serializer_class = CollectionSerializer

class CollectionDetail(RetrieveUpdateDestroyAPIView):

    queryset = Collection.objects.annotate(products_count=Count('product'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = self.get_object(pk=pk)
        if collection.product.count() > 0:
            return Response({'error': ' Collection cannot be deleted'}, status=status.HTTP_403_FORBIDDEN)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)