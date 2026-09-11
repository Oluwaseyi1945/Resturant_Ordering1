from django.urls import path
from .views import MenuItemListView, OrderCreateView, OrderDetailView, OrderAddItemView, OrderItemDeleteView, OrderStatusUpdateView


urlpatterns = [
    path('menuitem/', MenuItemListView.as_view(), name='menuitem-list'),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
       path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
       path('orders/<int:pk>/add-item/', OrderAddItemView.as_view(), name='order-add-item'),
       path('orders/<int:pk>/items/<int:item_id>/',OrderItemDeleteView.as_view(),name='order-item-delete'),
       path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]