from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from api.filters import TitleFilter
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleReadSerializer, TitleSerializer,
                             AdminActionsSerializer, GetTokenSerializer,
                             RegistrationSerializer, UserDataSerializer,
                             ReviewSerializer, CommentSerializer)
from api.permissions import IsAdminOrReadOnly, IsAdmin, IsAuthorOrAdminOrModer
from api_yamdb.settings import EMAIL_HOST_USER
from users.models import User


from reviews.models import Category, Genre, Title, Review


class CategoryViewSet(CreateModelMixin, ListModelMixin,
                      DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


def send_confirmation_code_to_user_email(username):
    user = get_object_or_404(User, username=username)
    code = default_token_generator.make_token(user)
    email = str(user.email)
    send_mail(
        'Код подтверждения',
        f'Используйте этот код {code} для получения токена',
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


class APIUserRegistration(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code_to_user_email(serializer.data['username'])
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetJWTToken(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = GetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.data['username']
        )
        if default_token_generator.check_token(
            user, serializer.data['confirmation_code']
        ):
            return Response(
                {'token': str(AccessToken.for_user(user))},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Код подтверждения неверен'},
            status=status.HTTP_400_BAD_REQUEST
        )


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminActionsSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'


class APIUserData(APIView):
    serializer_class = UserDataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrAdminOrModer,)
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrAdminOrModer,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()
