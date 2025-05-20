from rest_framework import serializers
from ..models import Carlist

def alphanumeric(value):
    if not str(value).isalnum():
        raise serializers.ValidationError("Chassis number must be alphanumeric")
    
    
class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 100)
    description = serializers.CharField()
    active = serializers.BooleanField(read_only = True)
    chassinumber = serializers.CharField(validators = [alphanumeric])
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


    def create(self, validated_data):
        return Carlist.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.active = validated_data.get('active',instance.active)
        instance.chassinumber = validated_data.get('chassinumber',instance.chassinumber)
        instance.prince = validated_data.get('price',instance.price)
        instance.save()
        return instance
    
    def validate_price(self,value):
        if value <= 200000:
            raise serializers.ValidationError("price must be greater than 200000")
        return value
    
    def validate(self,data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("name and description should not be same")
        return data
    

    