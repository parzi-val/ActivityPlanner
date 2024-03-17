from rest_framework import serializers

from rest_framework import serializers
from .models import OrderEnlisting

class OrderEnlistingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEnlisting
        fields = '__all__'  # You can specify the fields you want to include here if needed
