from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.

    Этот сериализатор преобразует данные модели Order в JSON и обратно.
    """
    
    class Meta:
        model = Order
        fields = '__all__'

    def validate_total_price(self, value):
        """
        Проверка, что общая стоимость не отрицательная.

        :param value: Общая стоимость заказа.
        :raises serializers.ValidationError: Если стоимость отрицательная.
        :return: Проверенное значение.
        """
        if value < 0:
            raise serializers.ValidationError("Общая стоимость не может быть отрицательной.")
        return value