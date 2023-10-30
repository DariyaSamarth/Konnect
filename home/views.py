from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView

# Create your views here.

class register(APIView):
    def post(self,request):
        try:
            data = request.data
            data['password']=make_password(data['password'])
            serializer = UserSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(type(e).__name__,status =status.HTTP_204_NO_CONTENT)