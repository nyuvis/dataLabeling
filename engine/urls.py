"""datalabeling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from . import views

app_name = 'engine'
urlpatterns = [
    path('', views.index, name='index'),
    path('datasetOverview', views.datasetOverview, name = 'datasetOverview'),
    path('randomSampling', views.randomSampling, name = 'randomSampling'),
    path('visSel', views.visSel, name = 'visSel'),
    path('classifierVis', views.classifierVis, name = 'classifierVis'),
    path('radarVis', views.radarVis, name = 'radarVis'),
    path('parallelVis', views.parallelVis, name = 'parallelVis'),
    path('dotVis', views.dotVis, name = 'dotVis'),
    path('outputSometing',views.outputSometing, name = 'outputSometing'),
    path('labelSingleDoc', views.labelSingleDoc, name = 'labelSingleDoc'),
    path('saveLabledDataToFile', views.saveLabledDataToFile, name = "saveLabledDataToFile")
]
