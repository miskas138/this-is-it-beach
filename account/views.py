from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import *
from django.contrib.auth.models import Group


@cache_control(no_cache=True, must_revalidate=True, no_store=True)#απενεργοποίηση του back button στον browser
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES )
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            group = Group.objects.get(name='simple_user')
            group.user_set.add(new_user)
            cd = profile_form.cleaned_data
            profile = Profile.objects.create(user=new_user, date_of_birth=cd['date_of_birth'], #request.POST.get('bday',''),
                                             gender=cd['gender'], photo=cd['photo'])

            return render(request, 'registration/register_done.html', {'new_user': new_user, 'profile': profile})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})
