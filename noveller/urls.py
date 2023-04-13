from django.urls import path
from .views import *
from . import views
from django.apps import apps

urlpatterns = [
    path('', views.index, name='index'),
    path('update_all_models/', UpdateAllNovellorModelsViewMaker.as_view(), name='update_all_models'),
    path('get_all_models/', GetAllNovellorModelsViewMaker.as_view(), name='get_all_models'),
]

models = apps.all_models['noveller']

for model_name in models:
    model = models[model_name]
    # print(f"model_name {model_name}")
    if '_' not in model_name and model.expose_rest == True:
        for entry in NovellerModelListCreateViewMaker.all_noveller_create_views:
            if entry['model'] == model:
                rest_name = model_name
                p = path(
                    f'{model_name.lower()}/', 
                    entry["view_class"].as_view(), 
                    name=f'{rest_name}_list_create'
                )
                urlpatterns.append(p)
                
        for entry in NovellerModelRUDViewMaker.all_noveller_rud_views:
            if entry['model'] == model:
                rest_name = model_name
                p = path(
                    f'{model_name.lower()}/', 
                    entry["view_class"].as_view(), 
                    name=f'{rest_name}_retrieve_update_destroy'
                )
                urlpatterns.append(p)
