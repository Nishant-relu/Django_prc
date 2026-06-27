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

class CollectionDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(Collection.objects.annotate(products_count=Count('product')),pk=pk)

    def get(self, request, pk):
        collection = self.get_object(pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    def put(self, request, pk):
        collection = self.get_object(pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        collection = self.get_object(pk=pk)
        if collection.product.count() > 0:
            return Response({'error': ' Collection cannot be deleted'}, status=status.HTTP_403_FORBIDDEN)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(
#         products_count=Count('product')
#     ), pk=pk)

#     if request.method == "GET":
#         serialize = CollectionSerializer(collection)
#         return Response(serialize.data)
    
#     elif request.method == "PUT":
#         deserialize = CollectionSerializer(collection, request.data)
#         deserialize.is_valid(raise_exception=True)
#         deserialize.save()
#         return Response(deserialize.data)
    
#     elif request.method == "DELETE":
#         if collection.product.count() > 0:
#             return Response({'error': ' Collection cannot be deleted'}, status=status.HTTP_403_FORBIDDEN)
        
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(products_count=Count('product')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == "POST":
#         serializer = CollectionSerializer(data=request.data)  # deserialize the data
#         serializer.is_valid(raise_exception=True)    # validate the data
#         serializer.save() # then save the data 
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
