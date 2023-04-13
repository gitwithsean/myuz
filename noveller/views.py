from django.http import HttpResponse
from django.apps import apps
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
# from pprint import pprint
  
all_noveller_model_names = apps.all_models['noveller']
  
def index(request):
    return HttpResponse("Hello, world. You're at the noveller index.")

def all_model_view_tuples_for(requested_models, view_class):
    model_create_view_tuples = []
    for tuple in get_noveller_model_serializer_tuples_for(requested_models):
        model_class = tuple['model_class']
        serializer_class =  tuple['serializer_class']
        class_name = model_class.__name__ + 'ListCreateView'
        meta_attrs = {
            'model': model_class
        }
        
        noveller_create_view_class = type(
            class_name, 
            (view_class,),
            {
                'Meta': type('Meta', (), meta_attrs),
                'queryset':  model_class.objects.all(),
                'serializer_class': serializer_class
            }
        )
        
        globals()[class_name] = noveller_create_view_class
        
        model_create_view_tuples.append({"model_class":model_class, "view_class": noveller_create_view_class})
    return model_create_view_tuples
 
class NovellerListCreateViewMater():
    def all_model_list_create_view_tuples():
        return all_model_view_tuples_for(apps.all_models['noveller'], generics.ListCreateAPIView)     

class NovellerRUDViewMaker():
    def all_model_rud_view_tuples():
        
        return all_model_view_tuples_for(apps.all_models['noveller'], generics.RetrieveUpdateDestroyAPIView)   
                
                
class UpdateAllNovellorModelsViewMaker(APIView):
    update_all_novellor_models_views = []
    
    def get(self, request): 
        return GetAllNovellorModelsViewMaker.get(self, request)     
    
    def put(self, request):
        
        models = apps.all_models['noveller']
        for model_name in models:
            model = models[model_name]
            if '_' not in model_name and model.expose_rest == True:
                for entry in SerializerMaker.all_noveller_model_serializer_tuples:
                    if entry['model-class'].__name__ == model:
                        model = entry['model_class']
                        serializer = entry['serializer']
                        serializer = serializer(data=item)
                        for item in request.data.get(model.get_rest_name, []):
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

class GetAllNovellorModelsViewMaker(APIView):
    def get(self, request):
        response_data = {}

        for tuple in get_noveller_model_serializer_tuples_for(""):
            model_class = tuple['model_class']
            serializer_class =  tuple['serializer_class']
            all_instances_of_model = model_class.objects.all()
            if all_instances_of_model.__len__() > 1:   
                model_name_insert = model_class.__name__+'s'
            elif all_instances_of_model.__len__() > 1:
                model_name_insert = model_class.__name__
            else:
                break
            
            model_serializer = serializer_class(all_instances_of_model, many=True)
            response_data[model_name_insert] = model_serializer.data

        return Response(response_data)
    