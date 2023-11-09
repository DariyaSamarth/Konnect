"""
URL configuration for Konnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.HomePage.as_view()),
    path('konnect/',views.KonnectMain.as_view()),

    path('user-profile/',views.UserProfile.as_view()),

    path('SignInPage/',views.SignInPage.as_view()),
    path('SignUpPage/',views.SignUpPage.as_view()),

    path('LinkAndSkills/',views.AddSkillLink.as_view()),

    path('PostDetail/',views.PostDetails.as_view()),
    
    path('register/',views.register.as_view()),
    path('login/',views.login.as_view()),

    path('create-post/',views.createPost.as_view()),
    path('add-comment/',views.commentOnPost.as_view()),
    path('upvote-post/',views.upvotePost.as_view()),
    path('downvote-post/',views.downvotePost.as_view()),

    path('addSkill/',views.AddSkill.as_view()),
    path('addLink/',views.AddLink.as_view()),

    path('upvote-comment/',views.upvoteComment.as_view()),
    path('downvote-comment/',views.downvoteComment.as_view()),

    path('delete-comment/',views.deleteComment.as_view()),
    path('delete-post/',views.deletePost.as_view())
]
