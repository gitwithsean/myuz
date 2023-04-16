from django.http import HttpResponse
from django.apps import apps
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .forms import *
from django.shortcuts import render
# from pprint import pprint
  
  
def index(request):
    return HttpResponse("Hello, world. You're at the phusis index.")

def phusis_swarm(request):
    all_agent_model_class_names = []
    all_agent_model_classes = AbstractAgent.__subclasses__()
    
    for agent_class in all_agent_model_classes:
        all_agent_model_class_names.append(agent_class.__name__)
        
    # model_names = ['TO DO FILL IN']
    model_names = all_agent_model_class_names
    for name in all_agent_model_class_names:
        if '_' not in name and 'singleton' not in name:
            print(f"{name}")
    
    form_tuples = get_phusis_model_form_tuples_for(model_names)

    if request.method == 'POST':
        forms = [tuple['form_class'](request.POST, prefix=tuple['model_class'].__name__.lower()) for tuple in form_tuples]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            return redirect('phusis_swarm')  # Redirect to the same page or another page after saving the data

    print(f"form_tuples: \n{form_tuples}")
    
    # context = {tuple['model_class'].__name__.lower() + '_form': tuple['form_class'](prefix=tuple['model_class'].__name__.lower()) for tuple in form_tuples}
    # print(f"context \n: {context}")
    
    forms_dict = {}
    for form_tuple in all_phusis_model_form_tuples:
        model_name = form_tuple["model_class"].__name__.lower()
        print(f"form_tuple['form_class']: {form_tuple['form_class']}")
        forms_dict[f"{model_name}_form"] = form_tuple["form_class"]()

    # Pass the forms dictionary to the template
    return render(request, 'phusis/phusis_swarm.html', {
        'model_names': model_names,
        'forms': forms_dict,
    })

def all_model_view_tuples_for(requested_models, view_class):
    model_create_view_tuples = []
    for tuple in get_phusis_model_serializer_tuples_for(requested_models):
        model_class = tuple['model_class']
        serializer_class =  tuple['serializer_class']
        class_name = model_class.__name__ + 'ListCreateView'
        meta_attrs = {
            'model': model_class
        }
        
        phusis_create_view_class = type(
            class_name, 
            (view_class,),
            {
                'Meta': type('Meta', (), meta_attrs),
                'queryset':  model_class.objects.all(),
                'serializer_class': serializer_class
            }
        )
        
        globals()[class_name] = phusis_create_view_class
        
        model_create_view_tuples.append({"model_class":model_class, "view_class": phusis_create_view_class})
    return model_create_view_tuples
 
class PhusisListCreateViewMater():
    def all_model_list_create_view_tuples():
        return all_model_view_tuples_for(apps.all_models['phusis'], generics.ListCreateAPIView)     

class PhusisRUDViewMaker():
    def all_model_rud_view_tuples():
        
        return all_model_view_tuples_for(apps.all_models['phusis'], generics.RetrieveUpdateDestroyAPIView)   
                
                
class UpdateAllPhusisModelsViewMaker(APIView):
    update_all_Phusis_models_views = []
    
    def get(self, request): 
        return GetAllPhusisModelsViewMaker.get(self, request)     
    
    def put(self, request):
        
        models = apps.all_models['phusis']
        for model_name in models:
            model = models[model_name]
            if '_' not in model_name and model.expose_rest == True:
                for entry in SerializerMaker.all_phusis_model_serializer_tuples:
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

class GetAllPhusisModelsViewMaker(APIView):
    def get(self, request):
        response_data = {}

        for tuple in get_phusis_model_serializer_tuples_for(""):
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
  
  