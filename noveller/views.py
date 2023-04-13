from django.http import HttpResponse
from django.apps import apps
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import ModelSerializer
from pprint import pprint
  
def index(request):
    return HttpResponse("Hello, world. You're at the noveller index.")


class NovellerModelListCreateViewMaker(generics.ListCreateAPIView):
    all_noveller_create_views = []
    
    models = apps.all_models['noveller']
    for model_name in models:
        model = models[model_name]
        if '_' not in model_name and model.expose_rest == True:
            for entry in ModelSerializer.all_serializers:
                if entry['model'] == model:
                    queryset = model.objects.all()  
                    serializer_class = entry["serializer_class"]
                    class_name = model.__name__ + 'ListCreateView'
                    meta_attrs = {
                        'model': model
                    }
                    noveller_create_view_class = type(class_name, (generics.ListCreateAPIView,), {'Meta': type('Meta', (), meta_attrs)})
                    globals()[class_name] = noveller_create_view_class
                    all_noveller_create_views.append({"model":model, "view_class": noveller_create_view_class})
                

class NovellerModelRUDViewMaker(generics.RetrieveUpdateDestroyAPIView):
    all_noveller_rud_views = []
    
    models = apps.all_models['noveller']
    for model_name in models:
        model = models[model_name]
        if '_' not in model_name and model.expose_rest == True:
            for entry in ModelSerializer.all_serializers:
                if entry['model'] == model:
                    srlzr_class = entry["serializer_class"]
                    class_name = model.__name__ + 'ListCreateView'
                    print(f"class_name = {class_name}")
                    noveller_rud_view_class = type(
                        class_name, 
                        (generics.RetrieveUpdateDestroyAPIView,), 
                    {
                        'queryset': model.objects.all(),
                        'serializer_class': srlzr_class,
                    },
                    )
                    globals()[class_name] = noveller_rud_view_class
                    all_noveller_rud_views.append({"model":model, "view_class": noveller_rud_view_class})

class UpdateAllNovellorModelsViewMaker(APIView):
    update_all_novellor_models_views = []
    
    def get(self, request): 
        return GetAllNovellorModelsViewMaker.get(self, request)     
    
    def put(self, request):
        
        models = apps.all_models['noveller']
        for model_name in models:
            model = models[model_name]
            if '_' not in model_name and model.expose_rest == True:
                for entry in ModelSerializer.all_serializers:
                    if entry['model'] == model:
                        model = entry['model']
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
        models = apps.all_models['noveller']
        for model_name in models:
            model = models[model_name]
            if '_' not in model_name and model.expose_rest == True:
                for entry in ModelSerializer.all_serializers:
                    if entry['model'] == model:
                        serializer_class = entry['serializer_class']
                        all_instances_of_model = model.objects.all()
                        if all_instances_of_model.__len__() > 0:   
                            model_name_plural = model_name+'s'
                            model_serializer = serializer_class(all_instances_of_model, many=True)
                            response_data[model_name_plural] = model_serializer.data

        return Response(response_data)
    