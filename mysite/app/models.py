from django.db import models

# Create your models here.

from app.managers import  QuestionManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):

    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    DEPARTMENT_CHOICES = [
    	('1', 'Отдел 1'),
    	('2', 'Отдел 2'),
    	('3', 'Отдел 3'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null = True, verbose_name='Avatar')
    nickname = models.CharField(max_length=100, unique=True, verbose_name='Nickname')
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField()

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name='Profile'
        verbose_name_plural='Profiles'
    

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    image=models.ImageField(upload_to='question_images', blank=True, null = True, verbose_name='QuestionImage')
    video=models.FileField(upload_to='question_videos',blank=True, null = True, verbose_name='QuestionVideo')
    date_published = models.DateTimeField(auto_now_add=True,verbose_name='Date published',db_index=True)
    is_published = models.BooleanField(verbose_name='Is published')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    votes = GenericRelation('Like', related_query_name='questions')
    tags=models.ManyToManyField('Tag',related_name='tags',related_query_name='tag')
    rating = models.IntegerField(default=0,db_index=True, verbose_name='Rating')
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Question'
        verbose_name_plural='Questions'

    def get_tags(self):
        return self.tags.get_queryset()

    def answers(self):
        return self.answer_set.get_queryset()

class Answer(models.Model):
    text = models.TextField(verbose_name='Text')
    correct = models.BooleanField(verbose_name='Correct')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True,verbose_name='Date published')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    votes = GenericRelation('Like', related_query_name='answers')
    rating = models.IntegerField(default=0, verbose_name='Rating')

    def __str__(self):
        return  'Комментарий  посту %s'%(self.question.title)
    

    class Meta:
        verbose_name='Answer'
        verbose_name_plural='Answers'

class Like(models.Model):
    LIKE = 1
    DISLIKE = -1
    CHOICES=((LIKE,'like'),(DISLIKE,'dislike'))
    ACTIONS={x[1]:x[0] for x in CHOICES}
 
    votes = models.SmallIntegerField(choices=CHOICES, verbose_name='Votes')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default='')
    object_id = models.PositiveIntegerField(default=0, verbose_name='Object id')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'Like от пользователя %s поста с id=%d'%(self.author.nickname,self.object_id)
    

    class Meta:
        verbose_name='Rating'
        verbose_name_plural='Ratings'

class Tag(models.Model):
    slug = models.SlugField(max_length=100,allow_unicode=True, verbose_name='Tag')

    def __str__(self):
        return self.slug
    

    class Meta:
        verbose_name='Tag'
        verbose_name_plural='Tags'

    def questions(self):
        return self.tags.all()