from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import permission_classes
from rest_framework import status

from api.permissions import IsOwner, IsSuperAdmin, IsSuperAdminOrReadOnly
from api.paginations import SimpleResultPagination
from api.serializers import GenreSerializer, DirectorSerializer, MovieSerializer, AddUpdateMovieSerializer, UserSerializer
from apps.models import Genre, Director, Movie


# class Genres


# class GenresGenericAPILIST(
#     # ListAPIView, CreateAPIView,
#     ListCreateAPIView,
# ):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )


# class DetailGenreGenericAPIView(
#     # RetrieveAPIView, DestroyAPIView, UpdateAPIView
#     RetrieveUpdateDestroyAPIView,
# ):
#     queryset = Genre.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = GenreSerializer
#     lookup_field = 'id'
    

def fetch_list_genres(request):
    return render(request, 'api/genres.html')


class DirectorsGenericAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DirectorSerializer
    pagination_class = SimpleResultPagination


class DetailDirectorGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectorSerializer
    lookup_field = 'id'
    

def fetch_list_directors(request):
    return render(request, 'api/directors.html')
    

class MoviesGenericAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = SimpleResultPagination


class DetailMovieGenericAPIView(RetrieveUpdateDestroyAPIView,):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


#############


@api_view()
@permission_classes((AllowAny,))
def list_movies(request):
    movies = Movie.objects.all()
    count = movies.count()
    limit = request.GET.get('limit', 2)
    offset = request.GET.get('offset', 1)
    paginator = Paginator(movies, limit)
    movies = paginator.get_page(offset)
    serializer = MovieSerializer(instance=movies, many=True, context={'request': request})
    response = {
        'count': count,
        'limit': int(limit),
        'offset': int(offset),
        'page_count': paginator.num_pages,
        'data': serializer.data
    }
    return Response(response)


@api_view()
def detail_movies(request, id):
    movie = get_object_or_404(Movie, id=id)
    serializer = MovieSerializer(instance=movie, many=False, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def add_movie(request):
    serializer =  AddUpdateMovieSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    movie = serializer.save()
    serializer = AddUpdateMovieSerializer(instance=movie, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_movies(request, id):
    movie = get_object_or_404(Movie, id=id)
    serializer =  AddUpdateMovieSerializer(instance=movie, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    movie = serializer.save()
    response_serializer = MovieSerializer(instance=movie, context={'request': request})
    return Response(response_serializer.data)


@api_view(['DELETE'])
@permission_classes((IsOwner, ))
def delete_movies(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    return Response({'is_deleted': True}, status=status.HTTP_204_NO_CONTENT)


def fetch_movies(request):
    return render(request, 'api/movies.html')


@api_view()
@permission_classes((AllowAny,))
def list_users(request):
    users = User.objects.all()
    count = users.count()
    limit = request.GET.get('limit', 6)
    offset = request.GET.get('offset', 1)
    paginator = Paginator(users, limit)
    users = paginator.get_page(offset)
    serializer = UserSerializer(instance=users, many=True)
    response = {
        'count': count,
        'limit': int(limit),
        'offset': int(offset),
        'page_count': paginator.num_pages,
        'data': serializer.data
    }
    return Response(response)


@api_view()
@permission_classes((AllowAny,))
def list_genres(request):
    genres = Genre.objects.all()
    count = genres.count()
    limit = request.GET.get('limit', 6)
    offset = request.GET.get('offset', 1)
    paginator = Paginator(genres, limit)
    genres = paginator.get_page(offset)
    serializer = GenreSerializer(instance=genres, many=True)
    response = {
        'count': count,
        'limit': int(limit),
        'offset': int(offset),
        'page_count': paginator.num_pages,
        'data': serializer.data
    }
    return Response(response)


@api_view()
def detail_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    serializer = GenreSerializer(instance=genre, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def add_genre(request):
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    serializer = GenreSerializer(instance=genre, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((IsOwner, ))
def delete_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    genre.delete()
    return Response({'is_deleted': True}, status=status.HTTP_204_NO_CONTENT)


@api_view()
@permission_classes((AllowAny,))
def list_directors(request):
    directors = Director.objects.all()
    count = directors.count()
    limit = request.GET.get('limit', 2)
    offset = request.GET.get('offset', 1)
    paginator = Paginator(directors, limit)
    directors = paginator.get_page(offset)
    serializer = DirectorSerializer(instance=directors, many=True)
    response = {
        'count': count,
        'limit': int(limit),
        'offset': int(offset),
        'page_count': paginator.num_pages,
        'data': serializer.data
    }
    return Response(response)


@api_view()
def detail_director(request, id):
    director = get_object_or_404(Director, id=id)
    serializer = DirectorSerializer(instance=director, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def add_director(request):
    serializer = DirectorSerializer(data=request.data)
    if serializer.is_valid(): 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_director(request, id):
    director = get_object_or_404(Director, id=id)
    serializer = DirectorSerializer(instance=director, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, IsOwner))
def delete_director(request, id):
    director = get_object_or_404(Director, id=id)
    director.delete()
    return Response({'is_deleted': True}, status=status.HTTP_204_NO_CONTENT)


