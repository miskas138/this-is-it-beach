from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control

from account.views import dashboard
from .forms import *


@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # απενεργοποίηση του back button στον browser
@login_required
def home_page(request):
    events = Event.objects.all().order_by('-information__dateTime')
    carousel_events = events[:10]
    paginator = Paginator(events, 3)
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        events = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'ajax_list.html', {'events': events, 'carousel_events': carousel_events})
    return render(request, 'home.html', {'section': 'home', 'events': events, 'carousel_events': carousel_events})



@login_required
@user_passes_test(lambda u: u.groups.filter(name='advanced_user'), dashboard)
def event_create(request):
    if request.method == 'POST':
        event = EventCreateForm(data=request.POST, files=request.FILES)
        information = InformationForm(data=request.POST)
        location = LocationForm(data=request.POST)
        if event.is_valid() and location.is_valid() and information.is_valid():
           # cd = form.cleaned_data
            new_event = event.save(commit=False)
            new_event.user = request.user
            new_event.save()
            new_information = information.save(commit=False)
            new_information.event = new_event
            new_information.save()
            new_location = location.save(commit=False)
            new_location.event = new_event
            new_location.save()
            return redirect('home_page')
    else:
        event = EventCreateForm()
        information = InformationForm()
        location = LocationForm()
    return render(request, 'event_create.html', {'event': event, 'information': information, 'location': location})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True, groups__name='advanced_user')

    return render(request, 'organizers/organizers_list.html', {'users': users})