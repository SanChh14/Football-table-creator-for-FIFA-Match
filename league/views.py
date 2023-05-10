from django.shortcuts import render, redirect
from addteam import forms, models

def home(request):
    th = ['Clubs', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
    matches = models.Fixtures.objects.all().filter(status = 1)
    teams = models.Team.objects.all()
    for club in teams:
        team = {'mp':0, 'w':0, 'd':0, 'l':0, 'gf':0, 'ga':0, 'gd':0, 'pts':0}
        home = matches.filter(t1 = club.name)
        away = matches.filter(t2 = club.name)
        for match in home:
            team['mp']+=1
            team['gf']+=match.t1g
            team['ga']+=match.t2g
            if match.t1g > match.t2g:
                team['w'] += 1
                team['pts'] += 3
            elif match.t1g < match.t2g:
                team['l'] += 1
            else:
                team['d']+= 1
                team['pts'] += 1
        for match in away:
            team['mp']+=1
            team['gf']+=match.t2g
            team['ga']+=match.t1g
            if match.t2g > match.t1g:
                team['w'] += 1
                team['pts'] += 3
            elif match.t2g < match.t1g:
                team['l'] += 1
            else:
                team['d'] += 1
                team['pts'] += 1
        team['gd'] = team['gf'] - team['ga']
        club.mp = team['mp']
        club.w = team['w']
        club.d = team['d']
        club.l = team['l']
        club.gf = team['gf']
        club.ga = team['ga']
        club.gd = team['gd']
        club.pts = team['pts']
        club.save()
    teams = teams.order_by('-pts', '-gd', '-gf')
    return render(request, 'home.html', {'home':'active', 'head':th, 'teams':teams})

def teams(request):
    teams = models.Team.objects.all()
    form = forms.Team()
    if request.method == 'POST':
        if 'add' in request.POST:
            form = forms.Team(request.POST)
            if form.is_valid():
                form.save()
                newTeam = models.Team.objects.get(name = request.POST['name'])
                allTeams = models.Team.objects.all()
                if allTeams.count()>0:
                    for team in allTeams:
                        print(team.name)
                        if(team.name != request.POST['name']):
                            fixture = models.Fixtures(t1=newTeam.name, t2=team.name)
                            fixture.save()
                            fixture = models.Fixtures(t1=team.name, t2=newTeam.name)
                            fixture.save()
                return redirect('/teams')
        if 'delete' in request.POST:
            try:
                form = models.Team.objects.get(name = request.POST['name'])
                form.delete()
                home = models.Fixtures.objects.all().filter(t1 = request.POST['name'])
                away = models.Fixtures.objects.all().filter(t2 = request.POST['name'])
                home.delete()
                away.delete()
                return redirect('/teams')
            except:
                return redirect('/teams')
    return render(request, 'teams.html', {'teams':'active', 'form':form, 'allteams':teams})

def fixtures(request):
    teams = models.Team.objects.all().order_by('pts')
    matchlist = list()
    for team in teams:
        name = team.name
        slug = name.replace(' ','-')
        matchlist.append([name, slug])
    return render(request, 'fixtures.html', {'fixtures':'active', 'matchlist':matchlist})

def matches(request, slug):
    home = models.Fixtures.objects.all().filter(t1 = slug.replace('-',' '))
    away = models.Fixtures.objects.all().filter(t2 = slug.replace('-',' '))
    matchdata = [home,away]
    if request.method == 'POST':
        if 'Play' in request.POST:
            match = models.Fixtures.objects.get(t1 = request.POST['t1'], t2 = request.POST['t2'])
            if request.POST['t1g'] != '':
                try:
                    a = int(request.POST['t1g'])
                    match.t1g = request.POST['t1g']
                except:
                    match.t1g = 0
            else:
                match.t1g = 0
            if request.POST['t2g'] != '':
                try:
                    a = int(request.POST['t2g'])
                    match.t2g = request.POST['t2g']
                except:
                    match.t2g = 0
            else:
                match.t2g = 0
            match.status = 1
            match.save()
            rdct = '/fixtures/'+request.POST['slug'].replace(' ','-')
            return redirect(rdct)
        if 'Unplay' in request.POST:
            match = models.Fixtures.objects.get(t1 = request.POST['t1'], t2 = request.POST['t2'])
            match.status = 0
            match.save()
            rdct = '/fixtures/'+request.POST['slug'].replace(' ','-')
            return redirect(rdct)
    return render(request, 'matches.html', {'fixtures':'active', 'matchdata':matchdata})
