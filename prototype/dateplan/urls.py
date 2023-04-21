from django.urls import path

from . import views

app_name = 'dateplan'

urlpatterns = [
    path('', views.index, name="dateplan"),
    path('results/', views.results, name="results")

]