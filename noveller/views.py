from django.http import HttpResponse
from django.apps import apps
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .noveller_models import *
from .serializers import *
from .forms import get_noveller_model_form_tuples_for, all_noveller_model_form_tuples, BookForm
from django.shortcuts import render
  
all_noveller_model_names = apps.all_models['noveller']
  
def index(request):
    return HttpResponse("Hello, world. You're at the noveller index.")

def novel_project(request):
    model_names = ['book', 'genre', 'character', 'setting', 'targetaudience', 'plot', 'chapter', 'storypacing', 'setting', 'bgresearch', 'character', 'literarystyleguide']
    
    # for name in all_noveller_model_names: if '_' not in name: print(f"{name}")
    
    form_tuples = get_noveller_model_form_tuples_for(model_names)

    if request.method == 'POST':
        forms = [tuple['form_class'](request.POST, prefix=tuple['model_class'].__name__.lower()) for tuple in form_tuples]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            return redirect('novel_project')  # Redirect to the same page or another page after saving the data
    
    forms_dict = {}
    for form_tuple in all_noveller_model_form_tuples:
        model_name = form_tuple["model_class"].__name__.lower()
        forms_dict[f"{model_name}_form"] = form_tuple["form_class"]()

    # Pass the forms dictionary to the template
    return render(request, 'noveller/novel_project.html', {
        'model_names': model_names,
        'forms': forms_dict,
    })

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
 
class NovellerListCreateViewMaker():
    def all_model_list_create_view_tuples():
        return all_model_view_tuples_for(apps.all_models['noveller'], generics.ListCreateAPIView)     

class NovellerRUDViewMaker():
    def all_model_rud_view_tuples():
        
        return all_model_view_tuples_for(apps.all_models['noveller'], generics.RetrieveUpdateDestroyAPIView)   
                
                
class UpdateAllNovellerModelsViewMaker(APIView):
    update_all_noveller_models_views = []
    
    def get(self, request): 
        return GetAllNovellerModelsViewMaker.get(self, request)     
    
    def put(self, request):
        
        models = apps.all_models['noveller']
        for model_name in models:
            model = models[model_name]
            if '_' not in model_name:
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

class GetAllNovellerModelsViewMaker(APIView):
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
  
def select_project(request):
    books = Book.objects.all()
    print(colored(books, "red"))
    return render(request, 'noveller/select_project.html', {'books': books})

def create_project(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('select_project')
    else:
        form = BookForm()
    return render(request, 'noveller/novel_project.html', {'form': form, 'action': 'Create'})


def edit_project(request):
    book_id = request.GET.get('book_id')
    if book_id:
        book = Book.objects.get(pk=book_id)
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                return redirect('select_project')
        else:
            form = BookForm(instance=book)
    else:
        return redirect('select_project')
    return render(request, 'noveller/novel_project.html', {'form': form, 'action': 'Edit', 'object': book})


def edit_project_attribute(request, attribute_type):
    attribute_id = request.GET.get('attribute_id')
    action = request.GET.get('action')
    if request.GET.get('related_field_name'): related_field_name = request.GET.get('related_field_name')
    model = None
    form_class = None

    for tuple in all_noveller_model_form_tuples:
        if attribute_type == tuple["model_class"].__name__.lower():
            model = tuple["model_class"]
            form_class = tuple["form_class"]
            break

    if not model or not form_class:
        return redirect('select_project')

    attributes = model.objects.all()
    instance = None

    if attribute_id:
        if action == 'create_related':
            instance = model()
            if related_field_name:
                setattr(instance, related_field_name, attribute_id)
        elif action == 'edit_related':
            instance = get_object_or_404(model, pk=attribute_id)
        else:
            instance = get_object_or_404(model, pk=attribute_id)
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('edit_project_attribute', kwargs={'attribute_type': attribute_type})}?attribute_id={form.instance.id}")

    else:
        form = form_class(instance=instance)

    return render(request, 'noveller/edit_project_attribute.html', {
        'attributes': attributes,
        'form': form,
        'attribute_type': attribute_type,
    })



def redirect_plural_to_singular(request, attribute_type_plural):
    attribute_type_singular = attribute_type_plural[:-1]
    return redirect('edit_project_attribute', request, attribute_type=attribute_type_singular)
