from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView, FriendRequestView, FriendRequestUpdateView, FriendsListView, PendingFriendRequestsView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-requests/', FriendRequestView.as_view(), name='friend-requests'),
    path('friend-requests/<int:pk>/', FriendRequestUpdateView.as_view(), name='update-friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]
