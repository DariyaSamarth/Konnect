from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import json

from rest_framework.views import APIView

# Create your views here.

class register(APIView):
    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(type(e).__name__,status =status.HTTP_204_NO_CONTENT)