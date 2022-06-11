
from django.contrib.contenttypes import fields
from django.utils import timezone
from django import forms

from django.contrib.auth.models import User
from app.models import *
import re



class LoginForm(forms.Form):

    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    
    class Meta:
        model=User
        fields=('username','password')



class QuestionForm(forms.ModelForm):
    title = forms.CharField(label="Фото",max_length=255, widget=forms.TextInput(attrs={'placeholder' : "Введите заголовок..."}))
    text = forms.CharField(label="Фото",widget=forms.Textarea(attrs={'placeholder': "Введите основной контент..."}))
    image=forms.ImageField(label="Фото",required=False)
    video=forms.FileField(label="Видео",required=False)
    tags = forms.CharField(label="Фото",max_length=255, widget=forms.TextInput(attrs={'placeholder' : "Добавьте теги через пробел..."}))

    class Meta:
        model = Question
        fields = ['title', 'text','image','video', 'tags']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(QuestionForm, self).save(commit=False)
        obj.author = self.author
        obj.is_published = True
        tag_list = self.cleaned_data['tags'].split(' ')
        tag_list = re.findall(r"[\w']+", self.cleaned_data['tags'])
        tag_objects = []
        for tag in tag_list:
            tag=tag.lower()
            if Tag.objects.filter(slug=tag).exists():
                tag_object = Tag.objects.all().get(slug=tag)
            else:
                tag_object=Tag(slug=tag)
                tag_object.save()
            tag_objects.append(tag_object)
        if commit:
            obj.save()
            for tag in tag_objects:
                obj.tags.add(tag)
        return obj

class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Добавьте комментарий...",'rows':3}))

    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, author, question, *args, **kwargs):
        self.author = author
        self.question = question
        super().__init__(*args, **kwargs)
        

    def save(self, commit=True):
        obj = super(AnswerForm, self).save(commit=False)
        obj.author = self.author
        obj.correct = False
        obj.date_published = timezone.now()
        obj.question = self.question
        if commit:
            obj.save()
        return obj 

class SettingsForm(forms.ModelForm):
    first_name=forms.CharField(label="Имя",max_length=100, required=False)
    last_name=forms.CharField(label="Фамилия",max_length=100, required=False)
    avatar = forms.ImageField(label="Аватар",required=False)
    nickname=forms.CharField(label="Nickname",max_length=100, required=False)
   



    class Meta:
        model=User
        fields=['first_name','last_name','nickname','avatar']
        widgets = {
        'first_name' : forms.TextInput(attrs={'placeholder' : 'Имя', 'class' : 'col-md-12 form-control'}),
        'last_name' : forms.TextInput(attrs={'placeholder' : 'Фамилия', 'class' : 'col-md-12 form-control'}),
        'nickname' : forms.TextInput(attrs={'placeholder' : 'Никнэйм', 'class' : 'col-md-12 form-control'}),
        'avatar' : forms.FileInput(attrs={'type' : 'file', 'class' : 'col-md-12'}),
    }

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['first_name']=user.first_name
        self.initial['last_name']=user.last_name
        self.initial['avatar']=user.profile.avatar
        self.initial['nickname']=user.profile.nickname

    
    def save(self,*args, **kwargs):
        user=super().save(*args, **kwargs)
        user.profile.nickname=self.cleaned_data['nickname']
        if self.cleaned_data['avatar']:
            user.profile.avatar=self.cleaned_data['avatar']
        else:
            user.profile.avatar=None
        user.profile.save()
        return user