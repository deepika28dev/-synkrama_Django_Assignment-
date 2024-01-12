# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth.models import User 
from rest_framework.permissions import IsAuthenticated

class PostListCreateView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.filter(author=request.user, is_deleted=False)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Assign the authenticated user to the post
            serializer.validated_data['author'] = request.user

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PostDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk, author=self.request.user, is_deleted=False)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        post = self.get_object(pk)
        if post:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post:
            
            post.is_deleted = True
            post.save()
            return Response({'detail': 'Soft deleted successfully.'})
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)



class BlockedUserListView(APIView):

    def get(self, request):
        blocked_users = BlockedUser.objects.filter(user=request.user)
        serializer = BlockedUserSerializer(blocked_users, many=True)
        return Response({'blocked_users': serializer.data})

class BlockUserView(APIView):
    def post(self, request):
        blocked_user_id = request.data.get('blocked_user')
        if blocked_user_id:
            try:
                blocked_user = User.objects.get(pk=blocked_user_id)
                blocked_relationship, created = BlockedUser.objects.get_or_create(user=request.user, blocked_user=blocked_user)
                if created:
                    return Response({'detail': 'User blocked successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'detail': 'User already blocked.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'detail': 'Blocked user not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Blocked user ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)

class UnblockUserView(APIView):

    def delete(self, request):
        blocked_user_id = request.data.get('blocked_user')
        if blocked_user_id:
            try:
                blocked_user = User.objects.get(pk=blocked_user_id)
                BlockedUser.objects.filter(user=request.user, blocked_user=blocked_user).delete()
                return Response({'detail': 'User unblocked successfully.'})
            except User.DoesNotExist:
                return Response({'detail': 'Blocked user not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Blocked user ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)