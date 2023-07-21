from rest_framework import serializers
from .models import AfiliadosModel

class AfiliadosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfiliadosModel
        fields = '__all__'