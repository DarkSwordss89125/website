from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Blog

# --- Форма для отзывов ---
class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя", 
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Как к вам обращаться?'})
    )
    RATING_CHOICES = [
        ('5', 'Отлично'),
        ('4', 'Хорошо'),
        ('3', 'Нормально'),
        ('2', 'Плохо'),
    ]
    rating = forms.ChoiceField(
        label="Как вы оцениваете наш сайт?", 
        choices=RATING_CHOICES, 
        widget=forms.RadioSelect
    )
    FREQUENCY_CHOICES = [
        ('daily', 'Каждый день'),
        ('weekly', 'Раз в неделю'),
        ('rarely', 'Редко'),
        ('first', 'Я здесь впервые'),
    ]
    frequency = forms.ChoiceField(
        label="Как часто вы заходите на кулинарные сайты?", 
        choices=FREQUENCY_CHOICES
    )
    features = forms.MultipleChoiceField(
        label="Что вам больше всего нравится? (можно выбрать несколько)",
        choices=[
            ('recipes', 'Рецепты'),
            ('design', 'Дизайн'),
            ('history', 'Истории о еде'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    wishes = forms.CharField(
        label="Ваши пожелания и отзывы", 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите здесь...'}),
        required=False
    )

# --- Форма для регистрации ---
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

# --- Форма для комментария ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите ваш комментарий...'}),
        }
        labels = {
            'text': 'Ваш комментарий'
        }

# --- Форма для добавления статьи ---
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'short_description', 'full_content', 'image']