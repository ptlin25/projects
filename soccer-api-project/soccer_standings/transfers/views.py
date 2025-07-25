from django.shortcuts import render
import requests
import os

# Create your views here.
def index(request):
    return render(request, "transfers/index.html", {})

def team_list(request, pk):
    url = "https://v3.football.api-sports.io/teams?league={league_id}&season=2024".format(league_id=pk)
    
    headers = {
        'x-rapidapi-key': os.environ['API_KEY'],
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.get(url, headers=headers).json().get('response')
    teams = [info['team'] for info in response]
    teams.sort(key=lambda team: team['name'])
    return render(request, "transfers/team_list.html", {'teams': teams})

def team_transfers(request, team_id):
    url = "https://v3.football.api-sports.io/transfers?team={team_id}".format(team_id=team_id)

    headers = {
        'x-rapidapi-key': os.environ['API_KEY'],
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    transfers = requests.get(url, headers=headers).json().get('response')
    transfers.sort(key=lambda transfer: transfer['transfers'][0]['date'], reverse=True)

    url = "https://v3.football.api-sports.io/teams?id={team_id}".format(team_id=team_id)

    headers = {
        'x-rapidapi-key': os.environ['API_KEY'],
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    team_info = requests.get(url, headers=headers).json().get('response')[0].get('team')
    team_name = team_info.get('name')

    return render(request, "transfers/team_transfers.html", {'team_id': team_id, 'team_name': team_name, 'transfers': transfers})

