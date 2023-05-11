from django.urls import path, re_path
from .views import *
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="noveller API",
        default_version='v1',
        description="API documentation for the noveller app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="getintouchwithseanryan@gmail.com")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('', views.index, name='index'),
    path('novel_project/', views.novel_project, name='novel_project'),
    path('', views.select_project, name='select_project'),
    path('create/', views.create_project, name='create_project'),
    path('edit/', views.edit_project, name='edit_project'),
    path('edit/<str:attribute_type>/', views.edit_project_attribute, name='edit_project_attribute'),
    path('select_project/', views.select_project, name='select_project'),
    re_path(r'^edit/(?P<attribute_type_plural>[a-zA-Z]+s)/$', views.redirect_plural_to_singular, name='redirect_plural_to_singular'),
    # path('update_all_models/', UpdateAllNovellerModelsViewMaker.as_view(), name='update_all_models'),
    # path('get_all_models/', GetAllNovellerModelsViewMaker.as_view(), name='get_all_models'),
]

for tuple in NovellerListCreateViewMaker.all_model_list_create_view_tuples():
    model_name = tuple['model_class'].__name__.lower()
    view_class = tuple['view_class']  
    urlpatterns += [
        path(f'{model_name}/', view_class.as_view(), name=f'{model_name}_list_create'),
    ]
        
for tuple in NovellerRUDViewMaker.all_model_rud_view_tuples():                
    model_name = tuple['model_class'].__name__.lower()
    view_class = tuple['view_class']
    urlpatterns += [
        path(f'{model_name}/<uuid:pk>/', view_class.as_view(), name=f'{model_name}__retrieve_update_destroy')
    ]
    

urlpatterns += [  
    # Swagger/OpenAPI URL patterns
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]