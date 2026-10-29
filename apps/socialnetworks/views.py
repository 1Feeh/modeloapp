#from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SocialnetworkForm
from .models import Socialnetwork
from django.contrib.auth.decorators import login_required

# Create your views here.
#@login_required(login_url='/contas/login/')
def add_socialnetwork(request):
    template_name = 'socialnetworks/add_socialnetwork.html'
    context = {}
    if request.method == 'POST':
        form = SocialnetworkForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('socialnetworks:list_socialnetworks')
    form = SocialnetworkForm()
    context['form'] = form
    return render(request, template_name, context)

def list_socialnetworks(request):
    template_name = 'socialnetworks/list_socialnetworks.html'
    socialnetworks = Socialnetwork.objects.filter()
    context = {
        'socialnetworks': socialnetworks
    }
    return render(request, template_name, context)

def edit_socialnetwork(request, id_socialnetwork):
    template_name = 'socialnetworks/add_socialnetwork.html'
    context ={}
    socialnetwork = get_object_or_404(Socialnetwork, id=id_socialnetwork)
    if request.method == 'POST':
        form = SocialnetworkForm(request.POST, instance=socialnetwork)
        if form.is_valid():
            form.save()
            return redirect('socialnetworks:list_socialnetworks')
    form = SocialnetworkForm(instance=socialnetwork)
    context['form'] = form
    return render(request, template_name, context)

def delete_socialnetwork(request, id_socialnetwork):
    socialnetwork = Socialnetwork.objects.get(id=id_socialnetwork)
    socialnetwork.delete()
    return redirect('socialnetworks:list_socialnetworks')
