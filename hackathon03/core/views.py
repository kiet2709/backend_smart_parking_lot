import base64
import datetime as dt
import os
import cv2
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Camera, MotoInfo
from core.serializer import CameraSerializer, UserSerializer
from park_smarter import settings
from Detect_License_Plate import Detect
from core.models import ObjectResponse
from core.serializer import ObjectResponseSerializer

class CameraView(ListCreateAPIView):

   model = Camera
   serializer_class = ObjectResponseSerializer


   def get(self, request, *args, **kwargs):
      baseDir = settings.BASE_DIR
      cameraList = Camera.objects.all()

      card_number = self.kwargs.get('card_number')
      moto_info = MotoInfo.objects.get(card_number=card_number)
      for camera in cameraList:
         (lps, img) = Detect.detect(cv2.imread(str(baseDir) + camera.image_url))
         print(lps)
         if moto_info.licence_plate in lps:
            timeStamp = str(dt.datetime.now().timestamp())
            cv2.imwrite(str(baseDir) + '/media/detect/' + timeStamp +'.jpg' ,img)
            url = 'http://172.22.224.1:8000/media/detect/' + timeStamp +'.jpg'

            objectResponse = ObjectResponse()
            objectResponse.licencePlate = moto_info.licence_plate
            objectResponse.image_url = url
            objectResponse.locate = camera.locate
            
            print(objectResponse.licencePlate)
            serializer = self.serializer_class(objectResponse)

            return Response(serializer.data)

      return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


class UserRegistrationView(ListCreateAPIView):
   serializer_class = UserSerializer

   def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(data=request.data)

      if serializer.is_valid():
         # create user with student ID as username and password
         User.objects.create_user(
            username=request.data.get('username'),
            password=request.data.get('password'),
         )
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
   serializer_class = UserSerializer

   def post(self, request, *args, **kwargs):
      username = request.data.get('username')
      password = request.data.get('password')

      # authenticate user
      user = authenticate(username=username, password=password)

      if user is not None:
         # login user
         login(request, user)
         return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
      else:
         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

