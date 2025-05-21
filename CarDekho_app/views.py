from asyncio import mixins
from django.shortcuts import render
from django.http import JsonResponse
from .models import Carlist, Showroomlist
from django.http import HttpResponse
from rest_framework import status 
from rest_framework import mixins
from rest_framework import generics as Generic
from .models import Review
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .api_file.serializers import CarSerializer, ReviewSerializer, ShowroomSerializer
import json
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

# -------------------------------------> Not using serializers <--------------------------------




# def car_list_view(request):
#     cars = Carlist.objects.all()
#     data = {
#         'cars':list(cars.values()),

#     }
#     return JsonResponse(data)



# def car_detail_view(request, pk):
#     car = Carlist.objects.get(pk=pk)
#     data = {
#         'name':car.name,
#         'description':car.description,
#         'active':car.active,
#     }

#     return JsonResponse(data)


# def car_list_view(request):
#     cars = Carlist.objects.all()
#     data = {
#         'cars': list(cars.values()),
#     }

#     data_json = json.dumps(data)
#     return HttpResponse(data_json, content_type='application/json')




#-------------------------------------> Using serializers <--------------------------------


# @api_view()
# def car_list_view(request):
#     car = Carlist.objects.all()
#     serializer = CarSerializer(car,many=True)
#     return Response(serializer.data)

# @api_view()
# def car_detail_view(request,pk):
#     car = Carlist.objects.get(pk=pk)
#     serializer = CarSerializer(car)
#     return Response(serializer.data)

# --------------------------------------->class based view <--------------------------------


class ReviewDetails(mixins.RetrieveModelMixin,Generic.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

class Reviewlist(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                Generic.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)





class Showroom_View(APIView):

    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated] 
    #permission_classes = [AllowAny] #--> it allows all the users to access this view
    #permission_classes = [IsAdminUser] #--> it allows only admin users to access this view

    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser] #--> it allows all the users to access this view
    def get(self,request):
        showroom = Showroomlist.objects.all()
        serializer = ShowroomSerializer(showroom,many=True,context={'request':request})
        return Response(serializer.data)
    

    def post(self,request):
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        


class Showroom_details(APIView):
    def get(self,request,pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'error':'Showroom not found'},status=status.HTTP_404_NOT_FOUND)
        

        serializer = ShowroomSerializer(showroom)
        return Response(serializer.data)
    

    def put(self,request,pk):
        showroom = Showroomlist.objects.get(pk=pk)
        serializer = ShowroomSerializer(showroom,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self,request,pk):
        showroom = Showroomlist.objects.get(pk=pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        
# -------------------------------------> Using serializers GET and POST <--------------------------------


@api_view(['GET', 'POST'])
def car_list_view(request):
    if request.method == 'GET':
        car = Carlist.objects.all()
        serializer = CarSerializer(car,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors) 
        

@api_view(['GET', 'PUT', 'DELETE'])
def car_detail_view(request, pk):
    if request.method == 'GET':
        try:
            car = Carlist.objects.get(pk=pk)
        except:
            return Response({'error':'Car not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        car = Carlist.objects.get(pk=pk)
        serializer = CarSerializer(car,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        car = Carlist.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
