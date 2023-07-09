from django.shortcuts import render
from rest_framework import generics
from .models import Thing
from .serializer import ThingSerializer
# Create your views here.

# view//get
# class ThingList(generics.ListAPIView):
#     queryset =Thing.objects.all()
#     serializer_class=ThingSerializer

# create a new thing
class ThingList(generics.ListCreateAPIView):
    queryset =Thing.objects.all()
    serializer_class=ThingSerializer

# class ThingDetail(generics.RetrieveAPIView):
#     queryset =Thing.objects.all()
#     serializer_class=ThingSerializer

# update
# class ThingDetail(generics.RetrieveUpdateAPIView):
#     queryset =Thing.objects.all()
#     serializer_class=ThingSerializer

# delete
class ThingDetail(generics.RetrieveDestroyAPIView):
    queryset =Thing.objects.all()
    serializer_class=ThingSerializer