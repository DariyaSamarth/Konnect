from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.hashers import check_password,make_password
from datetime import date
from .models import *
from .serializers import *
from django.urls import reverse
import json

# Create your views here.

class SignInPage(APIView):
    def get(self,request):
        template = loader.get_template('home/SignIn.html')
        context = {}
        return HttpResponse(template.render(context, request))
    
class SignUpPage(APIView):
    def get(self,request):
        template = loader.get_template('home/SignUp.html')
        context = {}
        return HttpResponse(template.render(context, request))



class HomePage(APIView):
    def get(self,request):
        template = loader.get_template('home/home.html')
        context = {}
        return HttpResponse(template.render(context, request))

class KonnectMain(APIView):
    def get(self,request):
        template = loader.get_template('home/konnect.html')
        id = request.query_params['id']
        context = {
            'id':id
        }
        return HttpResponse(template.render(context, request))



class UserProfile(APIView):
    def get(self,request):
        template = loader.get_template('home/profile.html')
        id = request.query_params['id']
        try:
            user_QS = User.objects.get(id=id)
        except Exception as e:
                return Response(
                        data = {'message':'User not found'},
                        status= status.HTTP_404_NOT_FOUND
                    )
        if(user_QS):
                serializer = UserSerializer(user_QS)
                user_json = JSONRenderer().render(data=serializer.data)
                user = json.loads(user_json)
        
        user_details ={
            'name' : user['name'],
            'mail': user['mail_id'],
            'skype': user['skype_id'],
            'project':user['project']
        }
        try:
            manager_QS = User.objects.get(id=user['manager'])
        except Exception as e:
                return Response(
                        data = {'message':'Manager details incorrect'},
                        status= status.HTTP_404_NOT_FOUND
                    )
        if(manager_QS):
                serializer = UserSerializer(manager_QS)
                manager_json = JSONRenderer().render(data=serializer.data)
                manager = json.loads(manager_json)
        user_details['manager'] = manager['name']
        user_posts={}
        user_links={}
        user_skills={}
        if(user['posts']):
            user_posts = json.loads(user['posts'])
        if(user['skills']):
            user_skills = json.loads(user['skills'])
        if(user['links']):
            user_links = json.loads(user['links'])
        detail_url = f'../LinkAndSkills/?id={user['id']}'
        context = {
            'id':id,
            'user':user_details,
            'posts':user_posts,
            'skills':user_skills,
            'links':user_links,
            'detail_url':detail_url
        }
        return HttpResponse(template.render(context, request))

class AddSkillLink(APIView):
    def get(self,request):
        template = loader.get_template('home/AddSkillLink.html')
        id = request.query_params['id']
        context = {
            'id':id
        }
        return HttpResponse(template.render(context, request))




#api that do not load a tempelate

class register(APIView):
    # user has unique Email and Skype ID
    # user's password is hashed and stored
    def post(self,request):
        try:
            data = dict(request.data)
            for key in data:
                data[key]=data[key][0]
            data['password']=make_password(data['password'])

            serializer = UserSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                return redirect('../SignInPage/')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(type(e).__name__,status =status.HTTP_500_INTERNAL_SERVER_ERROR)

class login(APIView):
    def post(self,request):
        try:
            data = dict(request.data)
            for key in data:
                data[key]=data[key][0]
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
                    response = HttpResponse("Cookie set and redirecting...")
                    response.set_cookie('mail_id', data['mail_id'], max_age=3600)
                    return redirect(f'../konnect/?id={user['id']}')
                else:
                    return Response(
                        data = {'message':'Password not matching'},
                        status= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                    )               
        except Exception as e:
            print(e)
            return Response(type(e).__name__,status =status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddSkill(APIView):
    def post(self,request):
        try:
            data = dict(request.data)
            for key in data:
                data[key]=data[key][0]
            id = data['id']

            try:
                user_QS = User.objects.get(id=id)
                # finding the user
            except Exception as e:
                return Response(
                        data = {'message':'User not found'},
                        status= status.HTTP_404_NOT_FOUND
                    ) 
            
            if(user_QS):
                user_serializer = UserSerializer(user_QS)
                user_json = JSONRenderer().render(data=user_serializer.data)
                user = json.loads(user_json)

                skills = {}
                if(user['skills']):
                    skills = json.loads(user['skills'])
                key = len(skills)+1
                skills[key]=data['skill']
                user['skills']=json.dumps(skills)
                user_serializer = UserSerializer(user_QS,data=user,partial=True)

                if(user_serializer.is_valid()):
                        user_serializer.save()
                        return redirect(f'../user-profile/?id={user['id']}')
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        except Exception as e:
            print(e)
            return Response(type(e).__name__,status =status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddLink(APIView):
    def post(self,request):
        try:
            data = dict(request.data)
            for key in data:
                data[key]=data[key][0]
            id = data['id']

            try:
                user_QS = User.objects.get(id=id)
                # finding the user
            except Exception as e:
                return Response(
                        data = {'message':'User not found'},
                        status= status.HTTP_404_NOT_FOUND
                    ) 
            
            if(user_QS):
                user_serializer = UserSerializer(user_QS)
                user_json = JSONRenderer().render(data=user_serializer.data)
                user = json.loads(user_json)

                links = {}
                if(user['links']):
                    links = json.loads(user['links'])
                links[data['link_key']]=data['link']
                user['links'] = json.dumps(links)

                user_serializer = UserSerializer(user_QS,data=user,partial=True)

                if(user_serializer.is_valid()):
                        user_serializer.save()
                        return redirect(f'../user-profile/?id={user['id']}')
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


     
class upvotePost(APIView):
    def put(self,request):
        try:
            post = request.query_params['post']
            owner = request.data['owner']
            flag = User.objects.filter(id=owner).exists() and Post.objects.filter(id=post).exists()

            if(flag):
                post_QS = Post.objects.get(id=post)
                post_serializer = PostSerializer(post_QS)
                post_json = JSONRenderer().render(data=post_serializer.data)
                post = json.loads(post_json)

                post['upvotes']=post['upvotes']+1
                post_serializer = PostSerializer(post_QS,data=post,partial=True)

                if(post_serializer.is_valid()):
                    post_serializer.save()
                    return Response(data={"message":"post upvoted"}, status=status.HTTP_200_OK)
                return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"message":"owner or post data incorrect"}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print(str(e))
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class downvotePost(APIView):
    def put(self,request):
        try:
            post = request.query_params['post']
            owner = request.data['owner']
            flag = User.objects.filter(id=owner).exists() and Post.objects.filter(id=post).exists()

            if(flag):
                post_QS = Post.objects.get(id=post)
                post_serializer = PostSerializer(post_QS)
                post_json = JSONRenderer().render(data=post_serializer.data)
                post = json.loads(post_json)

                post['downvotes']=post['downvotes']+1
                post_serializer = PostSerializer(post_QS,data=post,partial=True)

                if(post_serializer.is_valid()):
                    post_serializer.save()
                    return Response(data={"message":"post downvoted"}, status=status.HTTP_200_OK)
                return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"message":"owner or post data incorrect"}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print(str(e))
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


  
class upvoteComment(APIView):
    def put(self,request):
        try:
            com = request.query_params['comment']
            owner = request.data['owner']
            flag = User.objects.filter(id=owner).exists() and comment.objects.filter(id=com).exists()
            if(flag):
                comment_QS = comment.objects.get(id=com)
                comment_serializer = CommentSerializer(comment_QS)
                comment_json = JSONRenderer().render(data=comment_serializer.data)
                com = json.loads(comment_json)

                com['upvotes']=com['upvotes']+1
                comment_serializer = CommentSerializer(comment_QS,data=com,partial=True)

                if(comment_serializer.is_valid()):
                    comment_serializer.save()
                    return Response(data={"message":"comment upvoted"}, status=status.HTTP_200_OK)
                return Response(data=comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"message":"owner or comment data incorrect"}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print(str(e))
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class downvoteComment(APIView):
    def put(self,request):
        try:
            com = request.query_params['comment']
            owner = request.data['owner']
            flag = User.objects.filter(id=owner).exists() and comment.objects.filter(id=com).exists()
            if(flag):
                comment_QS = comment.objects.get(id=com)
                comment_serializer = CommentSerializer(comment_QS)
                comment_json = JSONRenderer().render(data=comment_serializer.data)
                com = json.loads(comment_json)

                com['downvotes']=com['downvotes']+1
                comment_serializer = CommentSerializer(comment_QS,data=com,partial=True)

                if(comment_serializer.is_valid()):
                    comment_serializer.save()
                    return Response(data={"message":"comment downvoted"}, status=status.HTTP_200_OK)
                return Response(data=comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"message":"owner or comment data incorrect"}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print(str(e))
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   
class deleteComment(APIView):
    def delete(self,request):
        try:
            com = request.query_params['comment']
            user = request.data['user']
            flag = comment.objects.filter(id=com).exists() and User.objects.filter(id=user).exists()
            
            if(flag):
                comment_QS = comment.objects.get(id=com)
                comment_serializer = CommentSerializer(comment_QS)
                comment_json = JSONRenderer().render(data=comment_serializer.data)
                com = json.loads(comment_json)

                post_QS = Post.objects.get(id=com['post'])
                post_serializer = PostSerializer(post_QS)
                post_json = JSONRenderer().render(data=post_serializer.data)
                post = json.loads(post_json)
                checker = user == post['owner']
                if(checker):
                    comments = json.loads(post['comments'])
                    id = str(com['id'])
                    comments.pop(id)
                    post['comments'] = json.dumps(comments)

                    post_serializer = PostSerializer(post_QS,data=post,partial=True)

                    if(post_serializer.is_valid()):
                        post_serializer.save()
                        comment_QS.delete()
                        return Response(data={"message":"comment deleted"}, status=status.HTTP_201_CREATED)
                    return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(
                    data = {"message":"unauthorised delete"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            return Response(data={"message":"owner or comment data incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class deletePost(APIView):
    def delete(self,request):
        try:
            post = request.query_params['post']
            user = request.data['user']
            flag = Post.objects.filter(id=post).exists() and User.objects.filter(id=user).exists()
            
            if(flag):

                post_QS = Post.objects.get(id=post)
                post_serializer = PostSerializer(post_QS)
                post_json = JSONRenderer().render(data=post_serializer.data)
                post = json.loads(post_json)
                checker = user == post['owner']
                
                if(checker):
                    
                    user_QS = User.objects.get(id=user)
                    user_serializer = UserSerializer(user_QS)
                    user_json = JSONRenderer().render(data=user_serializer.data)
                    user = json.loads(user_json)
                    print("reached here")

                    posts = json.loads(user['posts'])
                    id = str(post['id'])
                    posts.pop(id)
                    user['posts'] = json.dumps(posts)

                    user_serializer = UserSerializer(user_QS,data=user,partial=True)

                    if(user_serializer.is_valid()):

                        comments = json.loads(post['comments'])
                        for id in comments:
                            comment_QS = comment.objects.get(id=id)
                            comment_QS.delete()
                        post_QS.delete()
                        user_serializer.save()
                        return Response(data={"message":"post deleted"}, status=status.HTTP_201_CREATED)

                    return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(
                    data = {"message":"unauthorised delete"},
                    status=status.HTTP_401_UNAUTHORIZED
                )                
            
            return Response(data={"message":"owner or comment data incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)