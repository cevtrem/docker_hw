from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # Извлекаем данные о позициях продуктов
        positions = validated_data.pop('positions')

        # Создаём склад
        stock = super().create(validated_data)

        # Создаём позиции продуктов на складе
        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )

        return stock

    def update(self, instance, validated_data):
        # Извлекаем данные о позициях продуктов
        positions = validated_data.pop('positions')

        # Обновляем данные склада
        stock = super().update(instance, validated_data)

        # Удаляем все старые позиции
        stock.positions.all().delete()

        # Создаём новые позиции
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={
                    'quantity': position['quantity'],
                    'price': position['price']
                }
            )

        return stock