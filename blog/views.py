import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from django.utils.timezone import now

from .forms import PostForm, CommentForm, UserEditeForm,RegistrationForm
from .models import Post, Category, Comment
from django.contrib.auth import login


def dummy():
    return str(random.randint(1, 10))


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count // 2 + 1
    return {"cat1": all[:half], "cat2": all[half:]}


# Create your views here.
def index(request):
    # posts = Post.objects.all()
    # posts = Post.objects.filter(title__contains='python')
    # posts = Post.objects.filter(published_date__year=2023)
    # posts = Post.objects.filter(category__name__iexact='python')
    posts = Post.objects.order_by('-published_date')
    # post = Post.objects.get(pk=2)
    context = {'posts': posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def post(request, title):
    post = get_object_or_404(Post, title=title)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {"post": post,'comments': comments,'new_comment': new_comment,'comment_form': comment_form}
    context.update(get_categories())

    return render(request, "blog/post.html", context=context)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {"posts": posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def about(request):
    return render(request, "blog/about.html")


def contacts(request):
    return render(request, "blog/contacts.html")


from django.db.models import Q


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def services(request):
    return render(request, "blog/services.html")


def pro_url(request, dynamic_url):
    print(dynamic_url)
    return render(request, "blog/services.html", context={"url": dynamic_url})

@login_required
def create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            return index(request)
    context = {'form': form}
    return render(request, "blog/create.html", context=context)
@login_required
def profile(request):
    return render(request, "blog/profile.html")





def edit_profile(request):
    if request.method == 'POST':
        form = UserEditeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditeForm(instance=request.user)

    return render(request, 'blog/edit_profile.html', {'form': form})




def registration_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})





