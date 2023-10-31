from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.hashers import check_password,make_password
from datetime import date
from .models import *
from .serializers import *
import json

# Create your views here.

class register(APIView):
    # user has unique Email and Skype ID
    # user's password is hashed and stored
    def post(self,request):
        try:
            data = request.data
            data['password']=make_password(data['password'])
            serializer = UserSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(type(e).__name__,status =status.HTTP_500_INTERNAL_SERVER_ERROR)

class login(APIView):
    def post(self,request):
        try:
            data = request.data
            try:
                user_QS = User.objects.get(mail_id=data['mail_id'])
            except Exception as e:
                return Response(
                        data = {'message':'User not found'},
                        status= status.HTTP_404_NOT_FOUND
                    ) 
            if(user_QS):
                serializer = UserSerializer(user_QS)
                user_json = JSONRenderer().render(data=serializer.data)
                user = json.loads(user_json)
                flag = check_password(data['password'],user['password'])
                if(flag):
                    return Response(
                        data = user,status=status.HTTP_202_ACCEPTED
                    )
                else:
                    return Response(
                        data = {'message':'Password not matching'},
                        status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                    )               
        except Exception as e:
            print(e)
            return Response(type(e).__name__,status =status.HTTP_500_INTERNAL_SERVER_ERROR)

class createPost(APIView):
    # API for creating post
    def post(self,request):
        try:
            data = request.data
            try:
                user_QS = User.objects.get(id=data['owner'])
                # finding the user
            except Exception as e:
                return Response(
                        data = {'message':'User not found'},
                        status= status.HTTP_404_NOT_FOUND
                    ) 
            
            if(user_QS):
                
                data['date_created']= date.today()
                post_serializer = PostSerializer(data = data)
                
                if(post_serializer.is_valid()):
                    # post made and saving post data for later use
                    post_serializer.save()
                    post_json = JSONRenderer().render(data=post_serializer.data)
                    post = json.loads(post_json)

                    # getting the user
                    user_serializer = UserSerializer(user_QS)
                    user_json = JSONRenderer().render(data=user_serializer.data)
                    user = json.loads(user_json)

                    # updating the user post data
                    posts = {}
                    if(user['posts']):
                        posts = json.loads(user['posts'])
                    posts[post['id']]=post['content']
                    user['posts']=json.dumps(posts)

                    #updating the user data
                    user_serializer = UserSerializer(user_QS,data=user,partial=True)

                    if(user_serializer.is_valid()):
                        user_serializer.save()
                        return Response(data=post_serializer.data, status=status.HTTP_201_CREATED)
                    return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response(str(e),status =status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class commentOnPost(APIView):
    def post(self,request):
        try:
            # checking if owner and post exist
            post = request.query_params['post']
            owner = request.data['owner']
            flag = User.objects.filter(id=owner).exists() and Post.objects.filter(id=post).exists()

            if(flag):
                data = request.data
                data['post']=post
                data['date_created']= date.today()
                comment_seializer = CommentSerializer(data=data)
                # creating the comment
                if(comment_seializer.is_valid()):
                    comment_seializer.save()
                    comment_json = JSONRenderer().render(data=comment_seializer.data)
                    comment = json.loads(comment_json)

                    #finding the post
                    post_QS = Post.objects.get(id=post)
                    post_serializer = PostSerializer(post_QS)
                    post_json = JSONRenderer().render(data=post_serializer.data)
                    post = json.loads(post_json)

                    #updating the comment on the post
                    comments = {}
                    if(post['comments']):
                        comments = json.loads(post['comments'])
                    comments[comment['id']]=comment['content']
                    post['comments']=json.dumps(comments)

                    post_serializer = PostSerializer(post_QS,data=post,partial=True)

                    if(post_serializer.is_valid()):
                        post_serializer.save()
                        return Response(data=comment_seializer.data, status=status.HTTP_201_CREATED)
                    return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(data=comment_seializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"message":"post or owner data incorrect"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            return Response(str(e),status =status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class nextApi(APIView):
    pass