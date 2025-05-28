from asyncio import mixins
from django.shortcuts import render
from django.http import JsonResponse
from .models import Carlist, Showroomlist
from django.http import HttpResponse
from rest_framework import status 
# from rest_framework import mixins
from rest_framework import generics as Generic
from rest_framework import viewsets
from .api_file.permissions import AdminReadOnlyPermission,ReviewUserorReadOnlyPermission
from .models import Review
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from .api_file.serializers import CarSerializer, ReviewSerializer, ShowroomSerializer
import json
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .api_file.throtting import ReviewDetailThrottle, Reviewlistthrottle
from .api_file.pagination import Reviewlistpagination,Reviewlistlimitoffpag,Reviewlistcursorpag


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


# class ReviewDetails(mixins.RetrieveModelMixin,Generic.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [DjangoModelPermissions]


#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

# class Reviewlist(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 Generic.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)




class ReviewCreate(Generic.CreateAPIView):
    serializer_class = ReviewSerializer


    def get_queryset(self):
        return Review.objects.all()
    

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        cars = Carlist.objects.get(pk=pk)
        useredit = self.request.user
        Review.queryset = Review.objects.filter(car=cars,apiuser=useredit)
        if Review.queryset.exists():
            raise ValidationError("You have already submitted a review for this car")
        serializer.save(car=cars,apiuser=useredit)



# class Reviewlist(Generic.ListAPIView):
#     #queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     authentication_classes = [TokenAuthentication]
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Review.objects.filter(car=pk)
from rest_framework.permissions import AllowAny

class Reviewlist(Generic.ListAPIView):
    serializer_class = ReviewSerializer
    #authentication_classes = [JWTAuthentication]


    #authentication_classes = [TokenAuthentication]


    #before creating a file thorough API, we need to authenticate the user like this
    #throttle_classes = [UserRateThrottle, AnonRateThrottle]

    #after creating a throttling file we need to add it here
    #throttle_classes = [Reviewlistthrottle, AnonRateThrottle]  # <-- Throttling for this view

    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'review_list_scope'  # <-- Scoped throttling for this view

    # pagination_class = Reviewlistlimitoffpag

    pagination_class = Reviewlistcursorpag
    
    #pagination_class = Reviewlistpagination
    #permission_classes = [AllowAny]  # <- Makes the endpoint public

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)





#
# class ReviewDetails(Generic.retrieveAPIView):
# class ReviewDetails(Generic.RetrieveAPIView):
# class ReviewDetails(Generic.RetrieveUpdateAPIView):
# class ReviewDetails(Generic.destroyAPIView):
# class ReviewDetails(Generic.DestroyAPIView):
class ReviewDetails(Generic.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [AdminReadOnlyPermission]      # permission for admin
    # throttle_classes = [UserRateThrottle,AnonRateThrottle]  # <-- Throttling for this view
    #throttlintg_classes = [ReviewDetailThrottle, AnonRateThrottle]  # <-- Throttling for this view
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review_list_scope'  # <-- Scoped throttling for this view
    permission_classes = [ReviewUserorReadOnlyPermission]   # permission for which user created the review


# class Showroom_Viewset(viewsets.ModelViewSet):
#     queryset = Showroomlist.objects.all()
#     serializer_class = ShowroomSerializer 

#     def list(self, request):
#         queryset = Showroomlist.objects.all()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = Showroomlist.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = self.get_serializer(user)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = ShowroomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class Showroom_Viewset(viewsets.ModelViewSet):
class Showroom_Viewset(viewsets.ReadOnlyModelViewSet):
     queryset = Showroomlist.objects.all()
     serializer_class = ShowroomSerializer
     


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
@permission_classes([AllowAny])  # <--- Add this
def car_list_view(request):
    if request.method == 'GET':
        car = Carlist.objects.all()
        serializer = CarSerializer(car, many=True)
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
    
 