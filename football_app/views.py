from django.shortcuts import render

from django.core.paginator import Paginator
import requests
from datetime import datetime
from .models import Pays,League
# Create your views here.

def index(request):
  return render(request, 'home.html')

def getApiCountry(request):
  headers = {
    "X-RapidAPI-Key": "e9ed93335d8ab3a06790861f1ff27d92",
    "accept":"application/json"
  }

  url = "https://v3.football.api-sports.io/countries"

  response = requests.get(url, headers=headers)
  data = response.json()

  for indice in range(0, (data['results'])):
    country_name = data['response'][indice]['name']
    country_flag = data['response'][indice]['flag']
    data_country = {
      'country_name':country_name,
      'country_flag':country_flag
    }
  Pays.objects.create(nom_pays=data_country['country_name'],drapeau=data_country['country_flag'])


def listCountry(request):
  # getApiCountry(request)
  queryset = Pays.objects.all()
  paginator = Paginator(queryset, per_page=8)  # 10 éléments par page
  page = request.GET.get('page')
  items = paginator.get_page(page)
  return render(request, 'football/country_foot.html',{'items':items})

def selectOption(request):
  return render(request, "football/select_option.html")

def getApiLeague(request):
  headers = {
    "X-RapidAPI-Key": "e9ed93335d8ab3a06790861f1ff27d92",
    "accept":"application/json"
  }

  url_league = "https://v3.football.api-sports.io/leagues"

  response_url = requests.get(url_league, headers=headers)
  data_league = response_url.json()

  league_data_info = {}  # Initialisez les variables en dehors de la boucle
  league_data_country = {}
  league_data_season = {}
  data = [] # Initialisez également data en dehors de la boucle

  if 'response' in data_league:
    for indice_league in range((data_league['results'])):
      league_data_info = {}
      league_data_country = {}
      league_data_season = {}

      if 'league' in data_league['response'][indice_league]:

        league_data_info = {
          'id':data_league['response'][indice_league]['league']['id'],
          'name':data_league['response'][indice_league]['league']['name'],
          'type':data_league['response'][indice_league]['league']['type'],
          'logo':data_league['response'][indice_league]['league']['logo']
        }

      if 'country' in data_league['response'][indice_league]:
        league_data_country = {
          'nom_pays':data_league['response'][indice_league]['country']['name'],
          'flag':data_league['response'][indice_league]['country']['flag']
        }


      if 'seasons' in data_league['response'][indice_league]:
        seasons = data_league['response'][indice_league]['seasons']
        for season in seasons:
            league_data_season = {
                'annee': season['year'],
                'date_debut': season['start'],
                'date_fin': season['end'],
                'currently': season['current']
            }
      
      data.append({
        'league_data_info': league_data_info,
        'league_data_country': league_data_country,
        'league_data_season': league_data_season,
      })

  print(data)
  # for league_data in data:
  #   League.objects.create(
  #       id_league=league_data['league_data_info']['id'],
  #       nom_league=league_data['league_data_info']['name'],
  #       logo=league_data['league_data_info']['logo'],
  #       types=league_data['league_data_info']['type'],

  #       pays=league_data['league_data_country']['nom_pays'],
  #       flags=league_data['league_data_country']['flag'],

  #       annee=league_data['league_data_season']['annee'],
  #       date_debut=league_data['league_data_season']['date_debut'],
  #       date_fin=league_data['league_data_season']['date_fin'],
  #       currently=league_data['league_data_season']['currently'],
  #   )

  list_league = League.objects.all().distinct('id_league')
  paginator = Paginator(list_league, per_page=20)  # 10 éléments par page
  page = request.GET.get('page')
  items = paginator.get_page(page)
  current_year = datetime.now()
  print(current_year)

  return render(request, "football/league_foot.html",{"items":items,"current_year":current_year})

def getInfoleague(request,id_league):

  data_season = []
  data_teams = []

  url_teams = "https://v3.football.api-sports.io/teams"
  url_season = "https://v3.football.api-sports.io/leagues/seasons"

  headers = {
      "X-RapidAPI-Key": "e9ed93335d8ab3a06790861f1ff27d92",
      "accept": "application/json"
  }


  # Je recupere d'abord toutes les saisons
  response_season = requests.get(url_season, headers=headers)
  if response_season.status_code ==200:
    data = response_season.json()
    for indice_season in range(data['results']):
      data_season_date = {
        'annee':data['response'][indice_season]
      }
      # print(data['response'][indice_season])

      data_season.append({
        'data_season_date':data_season_date
      })
    # print(data_season)

    if data_season:
      for season_data in data_season:
        # Recuperation de l'id de la season
        season = season_data['data_season_date']['annee']

        params = {"league": id_league,"season":season}
        response_teams = requests.get(url_teams,headers=headers, params=params)
        data_team = response_teams.json()
        if data_team['results'] ==0:
          print("aucune information sur cette saison")
        for i_team in range(data_team['results']):
          data_teams.append({
            'teams_years':data_team['response'][i_team]
          })
      print(data_teams)
      return render(request, "football/infos_league.html",{'data_teams':data_teams})
  else:
      print(f"La requête a échoué avec le code de statut : {response.status_code}")
  return render(request, "football/infos_league.html",{'data_teams':data_teams})


