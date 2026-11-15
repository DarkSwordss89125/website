from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import FeedbackForm, CustomUserCreationForm, CommentForm, BlogForm
from .models import Blog, Comment

def index(request):
    return render(request, 'index.html')

def links(request):
    return render(request, 'links.html')

def feedback(request):
    submitted_data = None
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            raw_rating = form.cleaned_data['rating']
            raw_frequency = form.cleaned_data['frequency']
            raw_features = form.cleaned_data['features']

            rating_text = dict(form.fields['rating'].choices).get(raw_rating)
            frequency_text = dict(form.fields['frequency'].choices).get(raw_frequency)
            features_text = [dict(form.fields['features'].choices).get(f) for f in raw_features]

            submitted_data = {
                'name': form.cleaned_data['name'],
                'rating': rating_text,
                'frequency': frequency_text,
                'features': features_text,
                'wishes': form.cleaned_data['wishes'],
            }
            form = FeedbackForm()
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form, 'submitted_data': submitted_data})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def blog_list(request):
    posts = Blog.objects.all().order_by('-published_date')
    return render(request, 'blog.html', {'posts': posts})

def blogpost(request, parameter):
    post = get_object_or_404(Blog, id=parameter)
    comments = post.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('blogpost', parameter=post.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blogpost.html', {'post': post, 'comments': comments, 'form': form})

def add_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = BlogForm()
    return render(request, 'add_post.html', {'form': form})

def video_page(request):
    return render(request, 'video.html')