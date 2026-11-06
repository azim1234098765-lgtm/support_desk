from rest_framework import serializers
from .models import Category, Ticket, Comment
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'ticket', 'author', 'text', 'created_at')
        read_only_fields = ('author', 'ticket')

class TicketSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'category', 'category_name', 'status', 'status_display', 'author', 'created_at', 'updated_at')
        read_only_fields = ('status', 'author')

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'category', 'status')
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'category': {'required': False},
            'status': {'required': False},
        }