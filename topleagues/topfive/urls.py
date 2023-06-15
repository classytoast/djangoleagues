from django.urls import path

from . import views


urlpatterns = [
    path('', views.LeaguesHome.as_view(), name='home'),
    path('about/', views.AboutLeagues.as_view(), name='about'),
    path('league/<slug:season_slug>/', views.ShowLeague.as_view(), name='league'),
    path('matches/<slug:season_slug>/', views.ShowMatches.as_view(), name='matches'),
]
