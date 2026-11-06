from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Ticket, Comment
from .serializers import CategorySerializer, TicketSerializer, TicketUpdateSerializer, CommentSerializer
from .permissions import IsSupportManagerOrOwner


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSupportManagerOrOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'support_manager':
            return Ticket.objects.all()
        return Ticket.objects.filter(author=user)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'support_manager' and instance.status != 'new':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Можно удалять обращения только со статусом «новое».")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        return Comment.objects.filter(ticket_id=ticket_id)

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = Ticket.objects.get(id=ticket_id)

        user = self.request.user
        if user.role != 'support_manager' and ticket.author != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Нет доступа к этому обращению.")

        serializer.save(author=user, ticket=ticket)