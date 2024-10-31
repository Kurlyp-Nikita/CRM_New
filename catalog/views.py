from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from .models import UserProfile, Lead, Client
from django.contrib.auth.decorators import login_required
from .forms import AddleadForm, AddClientForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def dashboard(request):
    return render(request, 'dasboard.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            userprofile = UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()

    data = {'form': form}
    return render(request, 'userprofile/signup.html', data)


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
    if request.method == 'POST':
        form = AddleadForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            messages.success(request, 'The lead was create.')
            return redirect('leads_list')
    else:
        form = AddleadForm()

    data = {'form': form}
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
    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user
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
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, 'The lead was create.')
            return redirect('clients_list')
    else:
        form = AddClientForm()

    data = {'form': form}
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
