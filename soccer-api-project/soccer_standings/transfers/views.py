from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    return render(request, "transfers/index.html", {})

def team_list(request, pk):
    url = "https://v3.football.api-sports.io/teams?league={league_id}&season=2024".format(league_id=pk)

    headers = {
        'x-rapidapi-key': '9d4202b218ff9bc5640d6d2694bfc35a',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    teams = requests.get(url, headers=headers).json().get('response')
    teams.sort()
    return render(request, "transfers/team_list.html", {'teams': teams})