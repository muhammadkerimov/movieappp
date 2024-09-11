
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('',views.home,name='home'),
    path('logout/', views.logout, name='logout'),
    path('movie/<str:movie_link>/',views.moviepage,name='moviepage'),
    path('movie/<str:movie_link>/play',views.movieplayer,name='movieplayer'),
    path('series/<str:series_link>/',views.open_series,name='open_series'),
    path('series/<str:series_link>/<str:season_link>/<str:episode_link>/',views.play_series,name='play_series'),
    path('addWatchListFilm/<str:movie_link>/',views.addWatchListMovie,name='addwatchlistmovie'),
    path('addWatchListSeries/<str:series_link>/', views.addWatchListSeries, name='addwatchlistseries'),
    path('saveWatchTimeFilm/<str:movie_link>/<str:time>/',views.saveWatchTimeFilm,name='watchtimesavefilm'),
    path('getEpisodes/<str:series_link>/<int:season_id>/',views.getEpisodes,name='GetEpisodes')

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
