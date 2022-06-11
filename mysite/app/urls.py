from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('login<path:next>', views.login, name = 'login'),
	path('hot/', views.hot_questions,name='hot'),
    path('logout/', views.logout, name='logout'),
	path('tag/<str:tag_text>/', views.tag,name = 'tag'),
	path('questions/<int:question_id>/', views.one_question,name='one_question'),
	path('ask/', views.ask_question,name='ask'),
	path('settings', views.settings, name = 'settings'),
    path('vote/',views.vote,name='vote'),
	path('search/', views.search, name='search'),
	path('check/',views.check,name='check'),
	path('profile/<str:nickname>/', views.profile,name = 'profile')
]
