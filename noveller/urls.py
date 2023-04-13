from django.urls import path
from .views import NovellerModelListCreateViewMaker, NovellerModelRUDViewMaker
from . import views
from django.apps import apps

urlpatterns = [
    path('', views.index, name='index'),
]

models = apps.all_models['noveller']

for model_name in models:
    model = models[model_name]
    
    if '_' not in model_name and model.expose_rest == True:
        for entry in NovellerModelListCreateViewMaker.all_noveller_create_views:
            if entry['model'] == model:
                p = path(
                    f'{model_name.lower()}/', 
                    entry["view_class"].as_view(), 
                    name=f'{model_name.lower()}/book_list_create'
                )
                urlpatterns.append(p)
                
        for entry in NovellerModelRUDViewMaker.all_noveller_rud_views:
            if entry['model'] == model:
                p = path(
                    f'{model_name.lower()}/', 
                    entry["view_class"].as_view(), 
                    name=f'{model_name.lower()}/book_retrieve_update_destroy'
                )
                urlpatterns.append(p)
