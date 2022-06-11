import json
from django.core.paginator import  Paginator
from app.forms import *
from app import models
from django.contrib import auth
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render,reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.cache import cache


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 10)
    page = request.GET.get('page')
    objects_page = paginator.get_page(page)
    return objects_page

def context_processor(request):
    return{
        'users_rating':cache.get('users_rating'),
        'tags_rating':cache.get('tags_rating')
    }

@login_required
def index(request):
    questions_list = models.Question.objects.new_questions()
    questions = paginate(questions_list, request)
    return render(request,'index.html',{'questions':questions})

def login(request,next='/app/'):
    error=""
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            user = auth.authenticate(request, username=cdata['username'], password=cdata['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('/app/')
        error = "Incorrect data"
    else:
        form = LoginForm()
    return render(request, 'login.html',{'form': form,'error':error,})

@login_required
def hot_questions(request):
    questions_list = models.Question.objects.hot_questions()
    questions = paginate(questions_list, request)
    return render(request,'hot_questions.html',{'questions':questions})

@login_required
def ask_question(request):
    error = ""
    if request.POST:
        form = QuestionForm(request.user.profile,
        data = request.POST,
        files=request.FILES,)
        if form.is_valid():
            try:
                question = form.save()
                return redirect(
                    reverse('one_question', args=[question.pk])
                )
            except:
                error = "Tag does not exist"
        else:
            error = "Incorrect data"
    else:
        form = QuestionForm(request.user.profile)
    return render(request, 'ask_question.html', {
        'form' : form,
        'error':error
    })

@login_required
def tag(request,tag_text):
    tag = get_object_or_404(models.Tag.objects, slug=tag_text)
    questions = paginate(tag.questions(), request)
    return render(request, 'tag.html', {
        'questions': questions,
        'tag' : tag_text
    })

@login_required
def profile(request,nickname):
    profile = get_object_or_404(models.Profile.objects, nickname=nickname)
    return render(request, 'profile.html', {
        'profile': profile
        })

@login_required
def one_question(request,question_id):
    error=""
    question = get_object_or_404(models.Question.objects, pk=question_id)
    answers = paginate(question.answers(), request)   
    if request.POST:
        form = AnswerForm(author=request.user.profile, question=question, data = request.POST)
        if form.is_valid():
            answer = form.save()
            return redirect(
               reverse('one_question', args=[question.pk])
            )
        else:
            error = "Incorrect data"
    else:
        form = AnswerForm(author=request.user.profile, question=question)
    return render(request, 'one_question.html', {
        'question' : question,
        'answers' : answers,
        'form' : form,
        'error': error
    })

@login_required
def settings(request):
    error = ""
    if request.POST:
        form = SettingsForm(request.user,
        data=request.POST,
        files=request.FILES,
        instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
        else:
            error = "Incorrect data"
    else:
        form=SettingsForm(request.user)
    return render(request, 'settings.html', {
        'form' : form,
        'error' : error
    })

def logout(request):
    auth.logout(request)
    return redirect('/app/login/')

@login_required
@require_POST
def vote(request):
    data=request.POST
    qid=data['qid']
    action=data['action']

    inc=models.Like.ACTIONS[action]

    question=models.Question.objects.get(pk=qid)
    try:
        likedislike=Like.objects.get(content_type=ContentType.objects.get_for_model(question),object_id=question.id,author=request.user.profile)
        likedislike.delete()
        rating=question.rating-inc
        question.rating=F('rating')-inc
        question.save()
        status="0"

    except:
        question.votes.create(votes=inc,author=request.user.profile)
        rating=question.rating+inc
        question.rating=F('rating')+inc
        question.save()
        status="1"        

    return HttpResponse(
            json.dumps({
                "rating": str(rating),
                "status":status,
            }),
            content_type="application/json"
        )

@login_required
@require_POST
def check(request):
    answer_id=request.POST['id']
    answer=Answer.objects.get(id=answer_id)
    answer.correct=request.POST['status']
    answer.save()
    return HttpResponse()

@login_required
def search(request):
    questions_list = models.Question.objects.filter(title__icontains=request.GET.get("search"))
    questions = paginate(questions_list, request)
    return render(request,'question_list.html',{'questions':questions,
    'search':request.GET.get("search")})

@login_required
def profile(request,nickname):
    profile = get_object_or_404(models.Profile.objects, nickname=nickname)
    return render(request, 'profile.html', {
        'profile': profile
        })

