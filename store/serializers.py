from decimal import Decimal
from pyexpat import model
from rest_framework import serializers
from .models import Cart, Product, Collection, Review, CartItem

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:   
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description', 'product']
        read_only_fields = ['product']

class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']
