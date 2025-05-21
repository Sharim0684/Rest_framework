from rest_framework import serializers
from ..models import Carlist,Showroomlist,Review

# def alphanumeric(value):
#     if not str(value).isalnum():
#         raise serializers.ValidationError("Chassis number must be alphanumeric")
    

    
# class CarSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField(max_length = 100)
#     description = serializers.CharField()
#     active = serializers.BooleanField(read_only = True)
#     chassinumber = serializers.CharField(validators = [alphanumeric])
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)


#     def create(self, validated_data):
#         return Carlist.objects.create(**validated_data)
    

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.chassinumber = validated_data.get('chassinumber',instance.chassinumber)
#         instance.prince = validated_data.get('price',instance.price)
#         instance.save()
#         return instance





class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True,read_only=True)
    def get_discounted_price(self,obj):
        # discountprice = object.price - 5000
        # return discountprice
        if obj.price:
            return obj.price - 5000
        return None
    
    class Meta:
        model = Carlist
        # fields = ['id','name','description','active','chassinumber','price']
        #or
        # fields = '__all__'
        #OR
        #fields = ['id','name','description']   #--> it show only these fields in the response 8000/car/list/
        #OR
        exclude = ['id','name']



    def validate_price(self,value):
        if value <= 200000:
            raise serializers.ValidationError("price must be greater than 200000")
        return value
    
    def validate(self,data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("name and description should not be same")
        return data
    


class ShowroomSerializer(serializers.ModelSerializer): 
    #showrooms = CarSerializer(many=True,read_only=True) 
    # showrooms = serializers.StringRelatedField(many=True)
    # showrooms = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    #showrooms = CarSerializer.HyperlinkedRelatedField(many=True,read_only=True,view_name='car_detail')
    showrooms = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='car_detail')
    class Meta:
        model = Showroomlist
        fields = "__all__"


