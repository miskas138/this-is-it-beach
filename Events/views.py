from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_POST
from taggit.models import Tag
from datetime import timedelta

from Events.filters import PostFilter
from account.views import dashboard
from .forms import *
from django.contrib.auth.models import User
from django.utils import timezone
import html


@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # απενεργοποίηση του back button στον browser
@login_required
def home_page(request, tag_pk=None, section=None, tag_name=None):
    tag_list = Tag.objects.all()

    pinaks = Calendar.calendarDate()

    pinaks2 = Calendar.calendarDate(7)

    pinaks3 = Calendar.calendarDate(14)

    pinaks4 = Calendar.calendarDate(21)

    events = Event.objects.all().order_by('-information__dateTime')
    content = request.GET.get('content','')
    date = request.GET.get('date','')
    if section:
        events = events.filter(section=section)
    if date:
        events = events.filter(information__dateTime__date__exact=date)
    tag = None
    if tag_pk:
        tag = get_object_or_404(Tag, pk=tag_pk)
        events = events.filter(tags__in=[tag])
    if content:
        events_found = set()
        for event in events:
            if event.content:
                if content in event.get_content_text():
                    events_found.add(str(event.pk))
        events = Event.objects.filter(pk__in=events_found)

    event_filter = PostFilter(request.GET, queryset=events)
    events = event_filter.qs
    carousel_events = events[:8]
    paginator = Paginator(events, 4)
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
                                                  'carousel_events': carousel_events,
                                                  })
    return render(request, 'home.html', {'section': section,
                                         'events': events,
                                         'carousel_events': carousel_events,
                                         'tag': tag,
                                         'filter': event_filter,
                                         'pinaks': pinaks,
                                         'pinaks2': pinaks2,
                                         'pinaks3': pinaks3,
                                         'pinaks4': pinaks4,
                                         'tag_list': tag_list})




@login_required
@user_passes_test(lambda u: u.groups.filter(name='advanced_user'), dashboard)
def event_create(request):
    tags = Tag.objects.all()
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))
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
                                                 'tags': tags, 'filter': event_filter})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True, groups__name='advanced_user')
    user_carousel = users.order_by('-date_joined')[:6]
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))
    pinaks = Calendar.calendarDate()
    pinaks2 = Calendar.calendarDate(7)
    pinaks3 = Calendar.calendarDate(14)
    pinaks4 = Calendar.calendarDate(21)
    return render(request, 'organizers/organizers_list.html', {'users': users,
                                                               'filter': event_filter,
                                                               'user_carousel': user_carousel,
                                                               'pinaks': pinaks,
                                                               'pinaks2': pinaks2,
                                                               'pinaks3': pinaks3,
                                                               'pinaks4': pinaks4,})


def event_details(request, pk):
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))

    event = get_object_or_404(Event, pk=pk)
    likes = event.likes.all()
    user_like = likes.filter(user=request.user)
    comments = event.comments.filter(active=True).order_by('-created')[:50]
    View.objects.get_or_create(event=event, user=request.user)
    views = event.view.all().count()
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

    return render(request, 'event_details.html', {'event': event,
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
                                                 'filter': event_filter,
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


@login_required
def user_details(request, username):
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))

    user = get_object_or_404(User, username=username, is_active=True)
    profile = Advanced_Profile.objects.get(user=user)
    comments = profile.user_comments.filter(active=True).order_by('-created')[:50]
    events = user.events_created.all().order_by('-information__dateTime')
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
    if request.method == 'POST':
        comment_form = UserCommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.profile = Advanced_Profile.objects.get(user=user)
            new_comment.user = request.user
            new_comment.save()
            comment_form = UserCommentForm()
    else:
        comment_form = UserCommentForm()
        new_comment = None
    if request.is_ajax():
        return render(request, 'ajax_list.html', {'events': events})

    return render(request, 'organizers/hookDetails.html', {'user': user, 'events': events,
                                                           'comments': comments,
                                                           'comment_form': comment_form,
                                                           'new_comment': new_comment,
                                                           'filter': event_filter,
                                                           })

@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action=='follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


def event_video_uploads(request, pk):
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))

    event = get_object_or_404(Event, pk=pk)
    video_uploads = event.video_uploads.all()
    paginator = Paginator(video_uploads, 3)
    page = request.GET.get('page')
    try:
        video_uploads = paginator.page(page)
    except PageNotAnInteger:
        video_uploads = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        video_uploads = paginator.page(paginator.num_pages)


    likes = event.likes.all()
    user_like = likes.filter(user=request.user)
    comments = event.comments.filter(active=True).order_by('-created')[:50]
    View.objects.get_or_create(event=event, user=request.user)
    views = event.view.all().count()
    total_registered = event.register.all()
    similar_events = event.tags.similar_objects()
    tags = event.tags.all()
    new_comment = None
    try:
        user_registered = event.register.get(user=request.user)
    except:
        user_registered = None

    if request.method == 'POST':
        form = VideoUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.event = event
            new_item.save()

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.event = event
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

        form = VideoUploadForm()
    if request.is_ajax():
        return render(request, 'video_uploads.html', {'video_uploads': video_uploads})


    return render(request, 'video_uploads_2.html', {'event': event,
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
                                                    'video_uploads': video_uploads,
                                                    'form': form,
                                                    'filter': event_filter
                                                    })


def event_mp3_uploads(request, pk):
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))

    event = get_object_or_404(Event, pk=pk)
    mp3_uploads = event.mp3_uploads.all()
    paginator = Paginator(mp3_uploads, 5)
    page = request.GET.get('page')
    try:
        mp3_uploads = paginator.page(page)
    except PageNotAnInteger:
        mp3_uploads = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        mp3_uploads = paginator.page(paginator.num_pages)


    likes = event.likes.all()
    user_like = likes.filter(user=request.user)
    comments = event.comments.filter(active=True).order_by('-created')[:50]
    View.objects.get_or_create(event=event, user=request.user)
    views = event.view.all().count()
    total_registered = event.register.all()
    similar_events = event.tags.similar_objects()
    tags = event.tags.all()
    new_comment = None
    try:
        user_registered = event.register.get(user=request.user)
    except:
        user_registered = None

    if request.method == 'POST':
        mp3_form = Mp3UploadForm(data=request.POST, files=request.FILES)
        if mp3_form.is_valid():
            new_item = mp3_form.save(commit=False)
            new_item.user = request.user
            new_item.event = event
            new_item.save()

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.event = event
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

        mp3_form = Mp3UploadForm()
    if request.is_ajax():
        return render(request, 'mp3_list.html', {'mp3_uploads': mp3_uploads})


    return render(request, 'mp3_uploads.html', {'event': event,
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
                                                'mp3_uploads': mp3_uploads,
                                                'mp3_form': mp3_form,
                                                'filter': event_filter
                                                })


def event_image_uploads(request, pk):
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))

    event = get_object_or_404(Event, pk=pk)
    image_uploads = event.image_uploads.all()
    paginator = Paginator(image_uploads, 3)
    page = request.GET.get('page')
    try:
        image_uploads = paginator.page(page)
    except PageNotAnInteger:
        image_uploads = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        image_uploads = paginator.page(paginator.num_pages)


    likes = event.likes.all()
    user_like = likes.filter(user=request.user)
    comments = event.comments.filter(active=True).order_by('-created')[:50]
    View.objects.get_or_create(event=event, user=request.user)
    views = event.view.all().count()
    total_registered = event.register.all()
    similar_events = event.tags.similar_objects()
    tags = event.tags.all()
    new_comment = None
    try:
        user_registered = event.register.get(user=request.user)
    except:
        user_registered = None

    if request.method == 'POST':
        image_form = ImageUploadForm(data=request.POST, files=request.FILES)
        if image_form.is_valid():
            new_item = image_form.save(commit=False)
            new_item.user = request.user
            new_item.event = event
            new_item.save()

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.event = event
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

        image_form = ImageUploadForm()
    if request.is_ajax():
        return render(request, 'image_list.html', {'image_uploads': image_uploads})


    return render(request, 'image_uploads.html', {'event': event,
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
                                                  'image_uploads': image_uploads,
                                                  'image_form': image_form,
                                                  'filter': event_filter
                                                  })


@login_required
@user_passes_test(lambda u: u.groups.filter(name='advanced_user'), home_page)
def organization_charts(request):
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))

    events_views = Event.objects.filter(user=request.user, view__created__gte=timezone.datetime.now()-timedelta(days=30)).order_by('title').annotate(n=models.Count("pk"))
    events_likes = Event.objects.filter(user=request.user, likes__created__gte=timezone.datetime.now()-timedelta(days=30)).order_by('title').annotate(n=models.Count("pk"))
    events_registered = Event.objects.filter(user=request.user, register__created__gte=timezone.datetime.now()-timedelta(days=300)).order_by('title').annotate(n=models.Count("pk"))

    #posts = Views.objects.filter(post__author=request.user, created__gte=timezone.datetime.now()-timedelta(days=15))
    return render(request, 'organization_charts.html', {'events_views': events_views,
                                                        'events_likes': events_likes,
                                                        'events_registered': events_registered,
                                                        'filter': event_filter})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='advanced_user'), home_page)
def event_statistics_details(request, pk):
    event_filter = PostFilter(request.GET, queryset=Event.objects.all().order_by('-information__dateTime'))

    event = get_object_or_404(Event, pk=pk)
    events_views = event.view.filter(created__gte=timezone.datetime.now() - timedelta(days=300)).count()
    events_likes = event.likes.filter(created__gte=timezone.datetime.now() - timedelta(days=300)).count()
    events_registered = event.register.filter(created__gte=timezone.datetime.now() - timedelta(days=300)).count()
    events_comments = event.comments.filter(created__gte=timezone.datetime.now() - timedelta(days=300)).count()

    return render(request, 'event_statistics_details.html', {'event': event,
                                                             'events_views': events_views,
                                                             'events_likes': events_likes,
                                                             'events_registered': events_registered,
                                                             'events_comments': events_comments,
                                                             'filter': event_filter})

