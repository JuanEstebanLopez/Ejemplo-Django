from rest_framework import serializers
from .models import Category, Task

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'color', 'icon')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        category = CategorySerializer()
        fields = ('id', 'category', 'title', 'description', 'date', 'complete')