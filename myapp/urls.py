# urls.py
from django.urls import path
from .views import PostListCreateView, PostDetailView, BlockedUserListView, BlockUserView, UnblockUserView

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/get-blocked-user/', BlockedUserListView.as_view(), name='get-blocked-user'),
    path('api/block-user/', BlockUserView.as_view(), name='block-user'),
    path('api/unblock-user/', UnblockUserView.as_view(), name='unblock-user'),
]
