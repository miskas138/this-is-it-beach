from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control

from Events.models import Event
from .forms import *
from django import template
from django.contrib.auth.models import Group



@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # απενεργοποίηση του back button στον browser
@login_required
def dashboard(request):
    events = Event.objects.all()
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'events': events})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            group = Group.objects.get(name='simple_user')
            group.user_set.add(new_user)
            cd = profile_form.cleaned_data
            profile = Profile.objects.create(user=new_user, date_of_birth=cd['date_of_birth'],
                                             # request.POST.get('bday',''),
                                             gender=cd['gender'], photo=cd['photo'])

            return render(request, 'registration/register_done.html', {'new_user': new_user, 'profile': profile})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})


def register_type(request):
    return render(request, 'registration/register_type.html')


def advanced_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = AdvancedProfileEditForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            group = Group.objects.get(name='advanced_user')
            group.user_set.add(new_user)
            cd = profile_form.cleaned_data
            profile = Advanced_Profile.objects.create(user=new_user,
                                                      organization_name=cd['organization_name'],
                                                      photo=cd['photo'],
                                                      address=cd['address'],
                                                      city=cd['city'],
                                                      phone_number=cd['phone_number'])

            return render(request, 'registration/register_done.html', {'new_user': new_user, 'profile': profile})
    else:
        user_form = UserRegistrationForm()
        profile_form = AdvancedProfileEditForm()
    return render(request, 'registration/advanced_register.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if request.user.groups.filter(name='simple_user').exists():
            profile_form = ProfileEditForm(instance=request.user.profile,
                                           data=request.POST,
                                           files=request.FILES)
        else:
            profile_form = AdvancedProfileEditForm(instance=request.user.advanced_profile,
                                                   data=request.POST,
                                                   files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'registration/edit_done.html')
    else:
        user_form = UserEditForm(instance=request.user)
        if request.user.groups.filter(name='simple_user').exists():
            profile_form = ProfileEditForm(instance=request.user.profile)
        else:
            profile_form = AdvancedProfileEditForm(instance=request.user.advanced_profile)
    return render(request, 'registration/edit.html', {'user_form': user_form, 'profile_form': profile_form})


