from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.groups.filter(name='advanced_user'), 'account/dashboard')
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        mapForm = PlaceForm(data=request.POST)
        if form.is_valid() and mapForm.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.author = request.user
            new_item.save()
            new_map = mapForm.save(commit=False)
            new_map.post = new_item
            new_map.save()
            return redirect('home_page')
    else:
        form = PostCreateForm()
        mapForm = PlaceForm()
    return render(request, 'shituation/post_create.html', {'form':form, 'mapForm': mapForm})