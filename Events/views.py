from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_POST
from taggit.models import Tag

from account.views import dashboard
from .forms import *


@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # απενεργοποίηση του back button στον browser
@login_required
def home_page(request, tag_slug=None, section=None):
    events = Event.objects.all().order_by('-information__dateTime')
    music_events = events.filter(section="ΜΟΥΣΙΚΗ")[:5]
    theater_events = events.filter(section="ΘΕΑΤΡΟ")
    movie_events = events.filter(section="ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ")
    dancing_events = events.filter(section="ΧΟΡΟΣ")
    exhibition_events = events.filter(section="ΕΚΘΕΣΗ")
    misc_events = events.filter(section="ΔΙΑΦΟΡΕΣ")
    if section:
        events = events.filter(section=section)
    else:
        section = 'home'
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        events = events.filter(tags__in=[tag])
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
        return render(request, 'ajax_list.html', {'events': events,
                                                  'carousel_events': carousel_events})
    return render(request, 'home.html', {'section': section,
                                         'events': events,
                                         'music_events': music_events,
                                         'theater_events': theater_events,
                                         'exhibition_events': exhibition_events,
                                         'dancing_events': dancing_events,
                                         'movie_events': movie_events,
                                         'misc_events': misc_events,
                                         'carousel_events': carousel_events,
                                         'tag': tag})



@login_required
@user_passes_test(lambda u: u.groups.filter(name='advanced_user'), dashboard)
def event_create(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        event = EventCreateForm(data=request.POST, files=request.FILES)
        information = InformationForm(data=request.POST)
        location = LocationForm(data=request.POST)
        if event.is_valid() and location.is_valid() and information.is_valid():
           # cd = form.cleaned_data
            new_event = event.save(commit=False)
            new_event.user = request.user
            new_event.save()
            event.save_m2m()
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

    return render(request, 'event_create.html', {'event': event, 'information': information, 'location': location,
                                                 'tags': tags})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True, groups__name='advanced_user')

    return render(request, 'organizers/organizers_list.html', {'users': users})


def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    likes = event.likes.all()
    user_like = likes.filter(user=request.user)
    comments = event.comments.filter(active=True).order_by('-created')[:50]
    View.objects.get_or_create(event=event, user=request.user)
    views = event.register.all().count()
    total_registered = event.register.all()
    similar_events = event.tags.similar_objects()
    tags = event.tags.all()
    try:
        user_registered = event.register.get(user=request.user)
    except:
        user_registered = None


    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.event = event
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
        new_comment = None

    return render(request,'event_details.html', {'event': event,
                                                 'comments': comments,
                                                 'comment_form': comment_form,
                                                 'new_comment': new_comment,
                                                 'likes': likes,
                                                 'user_like': user_like,
                                                 'total_registered': total_registered,
                                                 'user_registered': user_registered,
                                                 'views': views,
                                                 'similar_events': similar_events,
                                                 'tags': tags,
                                                 })

@login_required
@require_POST
def event_like(request):
    event_id = request.POST.get('id')
    action = request.POST.get('action')
    if event_id and action:
        try:
            event = Event.objects.get(id=event_id)
            if action == 'like':

                Like.objects.get_or_create(event=event, user=request.user)
            else:

                Like.objects.filter(event=event, user=request.user).delete()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
@require_POST
def event_register(request):
    event_id = request.POST.get('id')
    action = request.POST.get('action')
    if event_id and action:
        try:
            event = Event.objects.get(id=event_id)
            if action == 'register':
                Register.objects.get_or_create(event=event, user=request.user)
            else:
                Register.objects.filter(event=event, user=request.user).delete()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})
