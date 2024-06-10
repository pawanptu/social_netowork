from django.shortcuts import render

# api/views.py
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, FriendRequestSerializer
from .models import FriendRequest
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta

User = get_user_model()

class CustomPagination(PageNumberPagination):
    page_size = 10

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = User.objects.filter(email__iexact=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('q', '')
        if '@' in keyword:
            return User.objects.filter(email__iexact=keyword)
        return User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))

class FriendRequestView(generics.ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )

    def perform_create(self, serializer):
        to_user_id = self.request.data.get('to_user')
        to_user = User.objects.get(id=to_user_id)
        if not FriendRequest.objects.filter(from_user=self.request.user, to_user=to_user, status='pending').exists():
            now = datetime.now()
            one_minute_ago = now - timedelta(minutes=1)
            recent_requests_count = FriendRequest.objects.filter(from_user=self.request.user, created_at__gte=one_minute_ago).count()
            if recent_requests_count < 3:
                serializer.save(from_user=self.request.user, to_user=to_user)
            else:
                return Response({'error': 'Too many requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            return Response({'error': 'Request already sent'}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestUpdateView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')

    def perform_update(self, serializer):
        status = self.request.data.get('status')
        if status in ['accepted', 'rejected']:
            serializer.save(status=status)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
        )
        friend_ids = [f.from_user.id if f.to_user == user else f.to_user.id for f in friends]
        return User.objects.filter(id__in=friend_ids)

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
