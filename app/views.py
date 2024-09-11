from django.shortcuts import render , redirect
from .models import *
from itertools import chain
from django.http import HttpResponse , JsonResponse 
import random
from django.contrib import messages


# Create your views here.

def signup(request):
    if request.method == 'POST':
     try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        newUser = UsersApp(username=username, email=email, password=password)
        newUser.save()
        newLikeList = UserLikeList(user=newUser)
        newWatchList = WatchList(user=newUser) 
        newLikeList.save()
        newWatchList.save()
        return redirect('login')
     except Exception as e:
        if e=='UNIQUE constraint failed: app_usersapp.email':
            messages.error(request, 'Email already exists')
            return redirect('signup')

    return render(request, 'signup.html')


def login(request):

    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user1 = UsersApp.objects.filter(email=username, password=password).first()
        if  user1 :
            request.session['user_id'] = user1.user_id
            request.session['username'] = user1.username
            request.session['email'] = user1.email
            request.session['password'] = user1.password
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def logout(request):
    request.session.clear()
    return redirect('login')



def moviepage(request,movie_link):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    movie = Film.objects.get(film_link=movie_link)
    movie.watch_count += 1
    movie.save()
    similarmovies = Film.objects.filter(film_category=movie.film_category).exclude(film_id=movie.film_id)[:10]
    user = UsersApp.objects.get(user_id=request.session['user_id'])
    WatchLis = WatchList.objects.get(user=user).watchlist
    WatchLis = WatchLis['films'] 
    if movie.film_id in WatchLis:
        watchlist = True
    else:
        watchlist = False
    return render(request, 'open_movies.html', {'movie': movie,'similars':similarmovies,'doeswatch':watchlist})
   

def home(request):
    sorted_movie = Series.objects.all().order_by('watch_count')[:10:-1]
    sorted_series = Film.objects.all().order_by('watch_count')[:10:-1]
    try:
        user = UsersApp.objects.get(user_id=request.session['user_id'])
        continuewatchingfilm = ContinueWatchingFilm.objects.filter(user=user)
        wathclist = []
        watchlistfilmids = WatchList.objects.get(user=user).watchlist['films']
        watchlistseriesids = WatchList.objects.get(user=user).watchlist['series']
        watchlistids = watchlistfilmids + watchlistseriesids
        for i in watchlistfilmids:
            film = Film.objects.get(film_id=i)
            wathclist.append(film)
        for j in watchlistseriesids:
            series = Series.objects.get(series_id=j)
            wathclist.append(series)
        random.shuffle(wathclist)
    except:
        continuewatchingfilm = None
        wathclist = None
        watchlistids = None
    popular_movies = sorted(
    chain(sorted_movie, sorted_series),
    key=lambda x: x.watch_count
    )[::-1]
    
    random_main_movie = list(chain(Film.objects.order_by('?'), Series.objects.order_by('?')))
    random.shuffle(random_main_movie)
    random_main_movie = random_main_movie[0]
    just_release = sorted(chain(Film.objects.order_by('release_date'), Series.objects.order_by('release_date')),
    key=lambda x: x.release_date )[::-1]
    
    
    context = {
        'random_main_movie': random_main_movie,
        'popular_movies':popular_movies,
        'just_relases':just_release,
        'watchlist':wathclist,
        'ids':watchlistids,
        'contwatchfilms':continuewatchingfilm
    }
    return render(request, 'home.html',context)


def movieplayer(request,movie_link):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    movie = Film.objects.get(film_link=movie_link)
    user = UsersApp.objects.get(user_id=request.session['user_id'])
    try:
        watching = ContinueWatchingFilm.objects.get(user=user,film=movie)
        
    except:
        watching = ContinueWatchingFilm(user=user, film=Film.objects.get(film_link=movie_link))
        watching.save()
    
    return render(request, 'movieplayer.html', {'movie': movie,'watchingdata':watching})


def open_series(request,series_link):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    series = Series.objects.get(series_link=series_link)
    series_seasons = SeriesSeasons.objects.filter(series=series)
    series_episode = SeriesEpisodes.objects.filter(series=series,series_seasons=series_seasons[0])
    user = UsersApp.objects.get(user_id=request.session['user_id'])
    series.watch_count += 1
    series.save()
    watchlist = WatchList.objects.get(user=user).watchlist
    doesinWatchList = False
    films = watchlist['films']
    seriess = watchlist['series']
    if series.series_id in seriess:
        doesinWatchList = True
    similar_series = Series.objects.filter(series_category=series.series_category).exclude(series_id=series.series_id)[:10]
    context = {'series': series,'series_seasons':series_seasons,'series_episodes':series_episode,'similar_series':similar_series,'doeswatch':doesinWatchList }
    return render(request, 'open_series.html', context)



def play_series(request,series_link,season_link,episode_link):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    Serie = Series.objects.get(series_link=series_link)
    SerieSeason = SeriesSeasons.objects.get(series=Serie,series_seasons_link=season_link)
    SerieEpisode = SeriesEpisodes.objects.get(series_episode_link=episode_link,series=Serie,series_seasons=SerieSeason)
    nextepisode = SeriesEpisodes.objects.filter(series=Serie).order_by('series_episodes_id')
    currentindex = list(nextepisode).index(SerieEpisode)
    user = UsersApp.objects.get(user_id=request.session['user_id'])
    ContinueWatchingSeries.objects.get_or_create(user=user, series=SerieEpisode)
    try:
        nextepisode = nextepisode[currentindex + 1:][0]
    except:
        nextepisode = None
    context = {
        'episode':SerieEpisode,
        'next':nextepisode
    }
    return render(request, 'play_series.html',context)


def getEpisodes(request, series_link, season_id):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    try:

        series = Series.objects.get(series_link=series_link)

     
        series_season = SeriesSeasons.objects.get(series_seasons_id=season_id)


        series_episodes = SeriesEpisodes.objects.filter(series=series, series_seasons=series_season).values()


        context = {'episodes': list(series_episodes),'season_name':series_season.series_seasons_name,'episode_count':series_season.series_season_episode_count,'season_link':series_season.series_seasons_link}
        return JsonResponse(context)

    except Series.DoesNotExist:
        return JsonResponse({'error': 'Series not found'}, status=404)

    except SeriesSeasons.DoesNotExist:
        return JsonResponse({'error': 'Season not found'}, status=404)
    
    
def saveWatchTimeFilm(request, movie_link, time):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    user = UsersApp.objects.get(user_id=request.session['user_id'])
    movie = Film.objects.get(film_link=movie_link)
    watching = ContinueWatchingFilm.objects.get(user=user, film=movie)
    hours , minutes ,seconds = time.split(':')
    time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    if time.seconds==movie.film_duration.seconds:
        watching.delete()
    else:
        watching.continue_watching_time = time
        watching.save()
    return JsonResponse({'status': 'success'})
    
    
    
def saveWatchTimeSeries(request, series_link,season_link,episode_link , time):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    user = UsersApp.objects.get(user_id=request.session['user_id'])
    Serie = Series.objects.get(series_link=series_link)
    Season = SeriesSeasons.objects.get(series_seasons_link=season_link)
    seriesepisode = SeriesEpisodes.objects.get(series_episode_link=episode_link,series_seasons=Season,series=Serie)
    watching = ContinueWatchingSeries.objects.get(user=user, series=seriesepisode)
    hours , minutes ,seconds = time.split(':')
    time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    if time.seconds==movie.film_duration.seconds:
        watching.delete()
    else:
        watching.continue_watching_time = time
        watching.save()
    return JsonResponse({'status': 'success'})
def addWatchListMovie(request, movie_link):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    if request.session.get('user_id'):
        user = UsersApp.objects.get(user_id=request.session.get('user_id'))
        movie = Film.objects.get(film_link=movie_link)
        watchlist = WatchList.objects.get(user=user)
        if not movie.film_id in watchlist.watchlist['films']:
            watchlist.watchlist['films'].append(movie.film_id)
            watchlist.save() 
            res = {'status': 'success'}
        else:
            watchlist.watchlist['films'].remove(movie.film_id)
            watchlist.save()
            res = {'status': 'successdel'}
        watchlist.save()
        return JsonResponse(res)
    else:
        return redirect('login')
    
def addWatchListSeries(request, series_link):
 if request.session.get('user_id') is None:
    return redirect('login')
 else:
    if request.session.get('user_id'):
        user = UsersApp.objects.get(user_id=request.session.get('user_id'))
        movie = Series.objects.get(series_link=series_link)
        watchlist = WatchList.objects.get(user=user)
        if not movie.series_id in watchlist.watchlist['series']:
            watchlist.watchlist['series'].append(movie.series_id)
            watchlist.save() 
            res = {'status': 'success'}
        else:
            watchlist.watchlist['series'].remove(movie.series_id)
            watchlist.save()
            res = {'status': 'successdel'}
        watchlist.save()
        return JsonResponse(res)
    else:
        return redirect('login')
    
     