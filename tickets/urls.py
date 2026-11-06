from django.urls import path
from .views import CategoryListView, TicketViewSet, CommentViewSet

ticket_list = TicketViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

ticket_detail = TicketViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('tickets/', ticket_list, name='ticket-list'),
    path('tickets/<int:pk>/', ticket_detail, name='ticket-detail'),
    path('tickets/<int:ticket_id>/comments/', comment_list, name='comment-list'),
]