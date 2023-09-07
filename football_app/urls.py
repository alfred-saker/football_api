from django.urls import path

from football_app import views
urlpatterns = [
  path('', views.index, name="home"),
  path('getCountry/', views.getApiCountry),
  path('listCountry/', views.listCountry, name="listcountry"),
  path('selectOption/', views.selectOption,name="select_option"),
  path('getApiLeague/', views.getApiLeague,name="getApiLeague"),
  path('infoLeague/<int:id_league>', views.getInfoleague,name="infoLeague"),
  # path('getTeams/<id_league>', views.getTeams,name="get_teams"),
]