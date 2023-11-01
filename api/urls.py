from django.urls import path, include

import api.views
from . import views


urlpatterns = [
    path('users/', views.list_users),
    path('genres/', views.GenresGenericAPILIST.as_view()),
    path('genres/<int:id>/', views.DetailGenreGenericAPIView.as_view()),
    path('genres/fetch/', views.fetch_list_genres),
    path('directors/', views.DirectorsGenericAPIView.as_view()),
    path('directors/<int:id>/', views.DetailDirectorGenericAPIView.as_view()),
    path('directors/fetch/', views.fetch_list_directors),
    path('movies/', api.views.MoviesGenericAPIView.as_view()),
    path('movies/<int:id>/', api.views.DetailMovieGenericAPIView.as_view()),
    path('movies/fetch/', views.fetch_movies),
    path('auth/', include('api.auth.urls'))
]
