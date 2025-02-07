from django.shortcuts import get_object_or_404, render, redirect
from .models import Order
from .forms import OrderForm
from django.db.models import Q
from rest_framework import viewsets
from .serializers import OrderSerializer
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.db import models
from .filters import OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами.

    Этот ViewSet предоставляет стандартные действия CRUD для модели Order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = OrderFilter
    search_fields = ['table_number', 'status']

    def list(self, request: HttpRequest) -> HttpResponse:
        """
        Получить список всех заказов.

        :param request: HTTP запрос.
        :return: Ответ с сериализованными данными заказов.
        """
        try:
            query: str = request.GET.get('q', '')
            status_filter: str = request.GET.get('status', '')
            orders = Order.objects.all()

            if query:
                orders = orders.filter(Q(table_number__icontains=query) | Q(status__icontains=query))

            if status_filter:
                orders = orders.filter(status=status_filter)

            return render(request, 'orders/order_list.html', {'orders': orders, 'query': query, 'status_filter': status_filter})
        except Exception as e:
            messages.error(request, f"Ошибка при получении списка заказов: {e}")
            return render(request, 'orders/order_list.html', {'orders': [], 'query': '', 'status_filter': ''})

    def create(self, request: HttpRequest) -> HttpResponse:
        """
        Создать новый заказ.

        :param request: HTTP запрос с данными заказа.
        :return: Ответ с созданным заказом.
        """
        if request.method == 'POST':
            try:
                table_number: str = request.POST.get('table_number')
                items: list = []
                for i in range(len(request.POST.getlist('item_name'))):
                    item_name: str = request.POST.getlist('item_name')[i]
                    item_price: str = request.POST.getlist('item_price')[i]
                    if item_name and item_price:
                        items.append({'name': item_name, 'price': float(item_price)})

                order = Order(table_number=table_number, items=items)
                order.save()
                messages.success(request, "Заказ успешно добавлен.")
                return redirect('order_list')
            except Exception as e:
                messages.error(request, f"Ошибка при добавлении заказа: {e}")
        return render(request, 'orders/order_form.html')

    def retrieve(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Получить детали конкретного заказа.

        :param request: HTTP запрос.
        :param pk: ID заказа.
        :return: Ответ с деталями заказа.
        """
        try:
            order = get_object_or_404(Order, id=pk)
            return render(request, 'orders/order_detail.html', {'order': order})
        except Exception as e:
            messages.error(request, f"Ошибка при получении деталей заказа: {e}")
            return redirect('order_list')

    def update(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Обновить существующий заказ.

        :param request: HTTP запрос с обновленными данными заказа.
        :param pk: ID заказа.
        :return: Ответ с обновленным заказом.
        """
        try:
            order = get_object_or_404(Order, id=pk)
            
            if request.method == 'POST':
                try:
                    table_number: str = request.POST.get('table_number')
                    items: list = []
                    for i in range(len(request.POST.getlist('item_name'))):
                        item_name: str = request.POST.getlist('item_name')[i]
                        item_price: str = request.POST.getlist('item_price')[i]
                        if item_name and item_price:
                            items.append({'name': item_name, 'price': float(item_price)})

                    order.table_number = table_number
                    order.items = items
                    order.status = request.POST.get('status') 
                    order.save()
                    messages.success(request, "Заказ успешно обновлен.")
                    return redirect('order_list')
                except Exception as e:
                    messages.error(request, f"Ошибка при обновлении заказа: {e}")
            
            return render(request, 'orders/order_form.html', {'order': order})
        except Exception as e:
            messages.error(request, f"Ошибка: {e}")
            return redirect('order_list')

    def destroy(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Удалить заказ.

        :param request: HTTP запрос.
        :param pk: ID заказа.
        :return: Ответ с подтверждением удаления.
        """
        try:
            order = get_object_or_404(Order, id=pk)
            order.delete()
            messages.success(request, "Заказ успешно удален.")
        except Exception as e:
            messages.error(request, f"Ошибка при удалении заказа: {e}")
        return redirect('order_list')

def order_list(request: HttpRequest) -> HttpResponse:
    """
    Отображение списка всех заказов.

    :param request: HTTP запрос.
    :return: Ответ с HTML-шаблоном списка заказов.
    """
    try:
        query: str = request.GET.get('q', '')
        status_filter: str = request.GET.get('status', '')
        orders = Order.objects.all()

        if query:
            orders = orders.filter(Q(table_number__icontains=query) | Q(status__icontains=query))

        if status_filter:
            orders = orders.filter(status=status_filter)

        return render(request, 'orders/order_list.html', {'orders': orders, 'query': query, 'status_filter': status_filter})
    except Exception as e:
        messages.error(request, f"Ошибка при получении списка заказов: {e}")
        return render(request, 'orders/order_list.html', {'orders': [], 'query': '', 'status_filter': ''})

def order_create(request: HttpRequest) -> HttpResponse:
    """
    Создание нового заказа.

    :param request: HTTP запрос с данными нового заказа.
    :return: Ответ с перенаправлением на список заказов.
    """
    if request.method == 'POST':
        try:
            table_number: str = request.POST.get('table_number')
            items: list = []
            for i in range(len(request.POST.getlist('item_name'))):
                item_name: str = request.POST.getlist('item_name')[i]
                item_price: str = request.POST.getlist('item_price')[i]
                if item_name and item_price:
                    items.append({'name': item_name, 'price': float(item_price)})

            order = Order(table_number=table_number, items=items)
            order.save()
            messages.success(request, "Заказ успешно добавлен.")
            return redirect('order_list')
        except Exception as e:
            messages.error(request, f"Ошибка при добавлении заказа: {e}")
    return render(request, 'orders/order_form.html')

def order_delete(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Удаление заказа.

    :param request: HTTP запрос.
    :param order_id: ID заказа для удаления.
    :return: Ответ с перенаправлением на список заказов.
    """
    try:
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, "Заказ успешно удален.")
    except Exception as e:
        messages.error(request, f"Ошибка при удалении заказа: {e}")
    return redirect('order_list')

def order_update(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Обновление существующего заказа.

    :param request: HTTP запрос с обновленными данными заказа.
    :param order_id: ID заказа для обновления.
    :return: Ответ с перенаправлением на список заказов.
    """
    try:
        order = get_object_or_404(Order, id=order_id)
        
        if request.method == 'POST':
            try:
                table_number: str = request.POST.get('table_number')
                items: list = []
                for i in range(len(request.POST.getlist('item_name'))):
                    item_name: str = request.POST.getlist('item_name')[i]
                    item_price: str = request.POST.getlist('item_price')[i]
                    if item_name and item_price:
                        items.append({'name': item_name, 'price': float(item_price)})

                order.table_number = table_number
                order.items = items
                order.status = request.POST.get('status') 
                order.save()
                messages.success(request, "Заказ успешно обновлен.")
                return redirect('order_list')
            except Exception as e:
                messages.error(request, f"Ошибка при обновлении заказа: {e}")
        
        return render(request, 'orders/order_form.html', {'order': order})
    except Exception as e:
        messages.error(request, f"Ошибка: {e}")
        return redirect('order_list')

def revenue_report(request: HttpRequest) -> HttpResponse:
    try:
        total_revenue: float = Order.objects.filter(status='paid').aggregate(total=models.Sum('total_price'))['total'] or 0
        return render(request, 'orders/revenue_report.html', {'total_revenue': total_revenue})
    except Exception as e:
        messages.error(request, f"Ошибка при расчете выручки: {e}")
        return render(request, 'orders/revenue_report.html', {'total_revenue': 0})
