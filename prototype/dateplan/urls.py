from django.urls import path

from . import views
app_name = 'dateplan'

urlpatterns = [
    path('', views.index, name="dateplan"),
    path('results/', views.results, name="results"),
    path('user_history/', views.user_history, name='user_history'),
    path('index/', views.index, name='index'),
    path('clear_history/', views.clear_history, name='clear_history')
]
