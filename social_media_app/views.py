from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets, status



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serialized_profile = ProfileSerializer(profile, many=False)
    return Response(serialized_profile.data)

@api_view(['POST'])
@permission_classes([])
def create_user(request):
    user = User.objects.create(
        username = request.data['username'],
    )   
    user.set_password(request.data['password'])
    user.save()
    profile = Profile.objects.create(
        user = user,
        first_name = request.data['first_name'],
        last_name = request.data['last_name']
    )

    profile.save()
    profile_serialized = ProfileSerializer(profile)
    return Response(profile_serialized.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_post(request):
    user = request.user 
    profile = Profile.objects.get(user = user)
    print('Profile', profile)


@permission_classes([IsAuthenticated])  
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        post_data = {
            'user': request.user.pk, 
            'content': request.data['content']
        }
        serialized_data = PostSerializer(data= post_data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        else: 
            return Response(serialized_data.errors, status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.content = request.data['content']  
        post.save()
        serialized_data = PostSerializer(post)
        return Response(serialized_data.data)
        
    
