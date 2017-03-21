from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.db.models import Q

# Create your views here.
def posts_home(request):
    return HttpResponse("<h1>Hello Good mornig.</h1>")

def posts_list(request):
    querysetlist = Post.objects.filter(draft=False)
    query = request.GET.get("search")

    if query:
        queryset = querysetlist.filter(
            Q(title__icontains = query) |
            Q(content__icontains = query)
            ).distinct()

    context = {
        "queryset": querysetlist,
        "title": "BLOG POST "
    }
    return render(request, "posts_list.html", context)
    #return HttpResponse("<h1>this is list.</h1>")

def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance= form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()
        instance.user =request.user
        messages.success(request, "Successfuly added this post")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"Failed to add this post")
    #if request.method=="post":
    #    content=request.POST.get("content")
    #    title=request.POST.get("title")
    #    Post.objects.create(title=title)
    #    Post.objects.create(content=content)
    context= {
        "form": form,
    }
    return render(request, "posts_form.html", context)
    #return HttpResponse("<h1>create.</h1>")

def posts_detail(request, id=None):
    instance= get_object_or_404(Post, id=id)
    context = {
        "title": "Post Detail",
        "instance": instance,
    }
    return render(request, "posts_detail.html", context)
    #return HttpResponse("<h>detail.</h1>")

def posts_update(request, id=None):
        instance = get_object_or_404(Post, id=id)
        form = PostForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            print form.cleaned_data.get("title")
            instance.save()
            messages.success(request, "Post is updated")
            return HttpResponseRedirect(instance.get_absolute_url())

        context = {
            "title": instance.title,
            "instance": instance,
            "form": form,
        }
        return render(request, "posts_form.html", context)
    #return HttpResponse("<h1>update.</h1>")

def posts_delete(request, id=None):
    isinstance = get_object_or_404(Post, id=id)
    isinstance.delete()
    return redirect("posts:list")
    return HttpResponse("<h1>delete.</h1>")
