from django.db import models
from django.db.models import Sum

class QuestionManager(models.Manager):
    use_for_related_fields = True

    def new_questions(self):
        return self.get_queryset().order_by('-date_published')

    def hot_questions(self):
        return self.get_queryset().order_by('-rating')
