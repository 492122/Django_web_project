from django.core.cache import cache
from django.core.management.base import BaseCommand
from app.models import Profile, Tag
from django.db.models import Count, Q
from datetime import datetime
from  dateutil import relativedelta
class Command(BaseCommand):

    def handle(self, *args, **options):
        current_datetime = datetime.now()
        sort_datetime=current_datetime - relativedelta.relativedelta(months=1)
        users_rating = Profile.objects.all().annotate(cnt=Count('question',filter=Q(question__date_published__gte=sort_datetime))
        +Count('answer',filter=Q(answer__date_published__gte=sort_datetime,answer__correct=True))).order_by('-cnt')[:5]
        tags_rating=Tag.objects.all().annotate(cnt=Count('tag')).order_by('-cnt')[:5]
        cache.set('users_rating',users_rating,86400+3600)
        cache.set('tags_rating',tags_rating,86400+3600)