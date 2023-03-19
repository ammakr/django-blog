# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from requests import request

from blog.forms import CommentForm

from .models import Post

# Create your views here.


class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# def index(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]

#     return render(request, 'blog/index.html', {
#         "posts": latest_posts
#     })


class PostsView(ListView):
    template_name = "blog/posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, 'blog/posts.html', {
#         "posts": all_posts
#     })


class SingleView(View):
    template_name = "blog/single.html"
    model = Post

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/single.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("single", args=[slug]))

        context = {
            "post": post,
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/single.html", context)


# def single(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/single.html', {
#         "post": identified_post
#     })

class LaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if not stored_posts:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/later.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session['stored_posts'] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session['stored_posts'] = stored_posts
            return HttpResponseRedirect('/later')

        return HttpResponseRedirect('/later')
