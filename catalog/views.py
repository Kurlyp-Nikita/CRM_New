from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from .models import UserProfile, Lead, Client, Team
from django.contrib.auth.decorators import login_required
from .forms import AddleadForm, AddClientForm, AddTeamForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


@login_required
def myaccount(request):
    team = Team.objects.filter(created_by=request.user).first()

    data = {'team': team}
    return render(request, 'userprofile/myaccount.html', data)


@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user).first()
    leads = Lead.objects.filter(team=team, converted_to_client=False).order_by('-created_at')[0:5]
    clients = Client.objects.filter(team=team).order_by('-created_at')[0:5]

    data = {
        'leads': leads,
        'clients': clients,
    }

    return render(request, 'dashboard.html', data)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Сохраняем нового пользователя
            user = form.save()

            # Создаем профиль пользователя
            UserProfile.objects.create(user=user)

            # Создаем команду для нового пользователя
            team = Team.objects.create(name='The team name', created_by=user)
            team.members.add(user)
            team.save()

            # Перенаправляем на страницу входа
            return redirect('login')
    else:
        form = UserCreationForm()

    data = {'form': form}
    return render(request, 'userprofile/signup.html', data)


@login_required
def edit_team(request, id):
    team = get_object_or_404(Team, id=id)

    if request.method == 'POST':
        form = AddTeamForm(request.POST, instance=team)

        if form.is_valid():
            form.save()
            messages.success(request, 'The changes was saved.')
            return redirect('myaccount')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = AddTeamForm(instance=team)

    data = {
        'form': form,
        'team': team,
    }
    return render(request, 'team/edit_team.html', data)


@login_required
def add_team(request):
    if request.method == 'POST':
        form = AddTeamForm(request.POST)

        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            messages.success(request, 'The lead was created.')
            return redirect('teams_list')
    else:
        form = AddTeamForm()

    data = {'form': form}
    return render(request, 'team/add_team.html', data)


@login_required
def teams_list(request):
    teams = Team.objects.filter(created_by=request.user)

    data = {'teams': teams}
    return render(request, 'team/teams_list.html', data)


@login_required
def teams_detail(request, id):
    team = Team.objects.get(id=id)

    data = {'team': team}
    return render(request, 'team/team_detail.html', data)


@login_required
def teams_delete(request, id):
    team = Team.objects.get(id=id)
    team.delete()

    messages.success(request, 'The lead was deleted.')
    return redirect('teams_list')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()

    data = {'form': form}
    return render(request, 'userprofile/loginup.html', data)


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def leads_delete(request, id):
    lead = Lead.objects.get(id=id)
    lead.delete()

    messages.success(request, 'The lead was deleted.')
    return redirect('leads_list')


@login_required
def edit_lead(request, id):
    lead = get_object_or_404(Lead, id=id)

    if request.method == 'POST':
        form = AddleadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            messages.success(request, 'The changes were saved.')
            return redirect('leads_list')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = AddleadForm(instance=lead)

    data = {'form': form}
    return render(request, 'lead/edit_leads.html', data)


@login_required
def add_lead(request):
    team = Team.objects.filter(created_by=request.user).first()
    if request.method == 'POST':
        form = AddleadForm(request.POST)

        if form.is_valid():
            # Получаем команду так же, как и в `add_client`
            team = Team.objects.filter(created_by=request.user).first()
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()
            messages.success(request, 'The lead was created.')
            return redirect('leads_list')
    else:
        form = AddleadForm()

    data = {
        'form': form,
        'team': team
    }
    return render(request, 'lead/add_lead.html', data)



@login_required
def leads_detail(request, id):
    lead = Lead.objects.get(id=id)

    data = {'lead': lead}
    return render(request, 'lead/leads_detail.html', data)


@login_required
def leads_list(request):
    leads = Lead.objects.filter(created_by=request.user, converted_to_client=False)

    data = {'leads': leads}
    return render(request, 'lead/leads_list.html', data)


@login_required
def convert_to_client(request, id):
    lead = get_object_or_404(Lead, id=id)
    team = Team.objects.filter(created_by=request.user).first()

    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
        team=team
    )

    lead.converted_to_client = True
    lead.save()
    messages.success(request, 'The lead converted to client.')

    return redirect('clients_list')


@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)

    data = {'clients': clients}
    return render(request, 'clients/clients_list.html', data)


@login_required
def clients_detail(request, id):
    client = get_object_or_404(Client, id=id)

    data = {'client': client}
    return render(request, 'clients/clients_detail.html', data)


@login_required
def add_client(request):
    team = Team.objects.filter(created_by=request.user).first()
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user).first()
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, 'The lead was create.')
            return redirect('clients_list')
    else:
        form = AddClientForm()

    data = {
        'form': form,
        'team': team,
    }
    return render(request, 'clients/add_client.html', data)


@login_required
def edit_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
            messages.success(request, 'The changes were saved.')
            return redirect('clients_list')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = AddleadForm(instance=client)

    data = {'form': form}
    return render(request, 'clients/edit_client.html', data)


@login_required
def clients_delete(request, id):
    client = Client.objects.get(id=id)
    client.delete()

    messages.success(request, 'The lead was deleted.')
    return redirect('clients_list')



