# myuz

<div style="display: flex; justify-content: center; align-items: center; height: 35vh;">
  <img src="./myuz/logos/phusis_logo.png" width="200" class="img-fluid" alt="Phusis Logo">
</div>

- [myuz](#myuz)
  - [Intro](#intro)
  - [myuz's current state](#myuzs-current-state)
    - [Back end](#back-end)
    - [Front end](#front-end)
  - [Setup](#setup)
    - [Requirements](#requirements)
    - [Setup instructions](#setup-instructions)
  - [Creating your own phusis project definitions](#creating-your-own-phusis-project-definitions)
  - [Creating your own phusis agent definitions](#creating-your-own-phusis-agent-definitions)
  - [Quick guide to creating your own phusis implementation](#quick-guide-to-creating-your-own-phusis-implementation)

## Intro

The core belief driving the Myuz platform is that the most effective AI applications arise from the collaboration between domain experts and AI systems. As demonstrated in the field of text-to-image AI generators, top-performing results are most often achieved when expert photographers work closely with AI technologies. By offering a platform for users with niche knowledge to develop custom AI-powered projects, Myuz seeks to give thinkers and creators from any field a simplified path to levaraging AI for their projects.

Myuz is a play on the word "muse" that we like to bakronym to "My Unleashed Zeal." We're hoping this name reflects the platform's goal of giving creators and thinkers extra resources to indulge their passions. For all the millions of people that lack the time it would take to devote themselves to a project close to their hearts, myuz unleash their zeal.

## myuz's current state

### Back end

There are currently two componenets to the myuz project, *phusis* and *noveller*:

**phusis**: A Django app that serves as a platform for developing AI assited project structures. It provides abstract classes and engines for AI agents and AI developed/assisted projects to be used in various applications.

**noveller**: An example implementation of the Phusis platform, specifically tailored for literary projects. It includes concrete classes derived from the Phusis abstract agent, such as CharacterAgents, WorldBuildingAgents, and ConflictAndResolutionAgents. Noveller implements 'Book' as the concreate of the AbstractPhusisProject class and defines concrete classes for the attributes of literary projects like Chapter, Plot, Scene, and LiteraryStyle, derived from the abstract PhusisProjectAttribute class. It also establish a number of AI agent types for the swarm that is directed at the project, such as the CharacterAgent and LiteraryStyleAgent.

By offering such a customizable and adaptable platform, myuz empowers users with niche expertise to develop AI-powered applications tailored to their specific requirements. By combining their domain knowledge with the power of AI, users can create mental maps of their projects and deploy arrays of agents designed to work together, ultimately producing superior outcomes compared to existing multi-agent systems.

> NOTE: In it's current incarnation, developing your own phusis project implementation requires an understanding of some of the principles of Object Oriented Programming and an ability to code in Python. While the noveller example should provide most people a good jumping off point for their own projects, we're hoping to make this more accessible in the future.

### Front end

I am currently levaraging Django's UI tools to create a prototype, but I am planning to move to a React front end in the near future. Would be very interested in collaborating with a front end developer on this project.

## Setup

### Requirements

This project was built with:
* [Django 4.2](https://www.djangoproject.com/download/)
* [python 3.10.6](https://www.python.org/downloads/release/python-3106/)
* [pip 22.0.2](https://pypi.org/project/pip/22.0.2/)
* [PostgreSQL 14.7](postgresql.org/ftp/source/v14.7/)
  
You will also need:
* [an openai account and API key](https://platform.openai.com/account/api-keys)
* [a pinecone account, API key and region](https://www.pinecone.io/)


### Setup instructions

The following instructions were put together and tested with WSL: Ubuntu on Windows 10 - setup may be different on your own machine

```bash
# add your secrets to the secrets folder
touch .secrets/openai_api_key
touch .secrets/pinecone_api_key
touch .secrets/pinecone_api_region # this looks something like 'asia-southeast1-gcp' and can be found alongside your API key in the pinecone console

# set up your virtual environment
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# install postgres and follow installation and setup instructions for your system
# https://www.postgresqltutorial.com/postgresql-getting-started/
# remember the password you set for the postgres user, we're going to use it later

# add these lines to your ~/.bashrc or ~/.bash_profile
export POSTGRES_PW=''   #the password you set for the postgres user
export MYUZ_DB_PW=''    #the password you want to set for the myuz db user
export MYUZ_DB_USER=''  #the user you want to set for the myuz db user

#depending on whether you added the above...
. ~/.bashrc
. ~/.bash_profile

# This will start the postgres server if it's not already running
# create the myuz database, create and run the migrations for the noveller and phusis apps,
# init the db with data for agents and an example novel,
# and create the pinecone index for the pinecone key
./blank_slate all

#If you just want to restart the server if it's not running on system restart
sudo service postgresql start
sudo service postgresql status

# run the server
python3 manage.py runserver
```

## Creating your own phusis project definitions

myuz (the django project) will be the site of multiple project types that will utilize the phusis platform.

This repo provides a novel writing project type, 'noveller', as an example. However, there are opportunities to use the phusis platform for many other types of projects (research papers, DnD campaigns, business plans, event management, etc.).

phusis (the platform) and noveller (the application) are each apps within the myuz project. But you can create your own apps to implement your own project types.

Check out the AbstractPhusisProject model and related models in `phusis/agent_models.py` for the abstracts available to create new project types.

Then check out the implementation of those abstracts in the noveller app in `noveller/noveller_models.py` and `noveller/noveller_agents.py`.

To create your own implementation of the phusis platform, create a new django app within the myuz django project. For guidance you can read the Django project/app tutorial [here](https://docs.djangoproject.com/en/4.2/intro/tutorial01/) - there is also a quick-start guide specific to phusis [below](#quick-guide-to-creating-your-own-phusis-implementation).


## Creating your own phusis agent definitions

For now, my own agent recipes are remaining private, but here is a guide on creating your own.

Take a look at the AbstractAgent model in `phusis/agent_models.py` for available attributes for defining your agents. Example concretes of this abstract can be found in `noveller/noveller_agents.py`

Say you are creating a phusis application 'shopper.' You will need to create a JSON representation of your agent and save it in the `agent_data` directory `shopper/phusis-secret-sauce/agent_data`

You can even create a number of agents as an array in one json file. I like to keep agent 'types' in separate files, but you can do it however you like.

```json
[
    {
        "class_name": "ResearchAgent",
        "properties":{
            "name": "Historical Fiction Investigator",
            "elaboration": "This agent is skilled at unearthing historical facts and details, providing rich context for crafting immersive historical fiction.",
            "impersonations": ["Hilary Mantel", "Bernard Cornwell", "Ken Follett"],
            "personality_traits": ["Detail-oriented", "Persistent", "Curious"],
            "goals": ["Uncover historical facts", "Provide context", "Enhance authenticity"],
            "roles": ["Historical researcher", "Fact-checker", "Context provider"],
            "qualifications": ["History expert", "Primary source analyst", "Fact verifier"]
        } 
    },
    {
        "class_name": "ResearchAgent",
        "properties":{
            "name": "Science Consultant",
            "elaboration": "Adept at researching scientific concepts and breakthroughs, this agent provides accurate and engaging scientific context for your story.",
            "impersonations": ["Carl Sagan", "Neil deGrasse Tyson", "Brian Greene"],
            "personality_traits": ["Analytical", "Inquisitive", "Rational"],
            "goals": ["Research scientific concepts", "Clarify complex ideas", "Ensure accuracy"],
            "roles": ["Scientific researcher", "Expert consultant", "Idea simplifier"],
            "qualifications": ["Science expert", "Clear communicator", "Fact verifier"]
        }
    },
    {
        "class_name": "ResearchAgent",
        "properties":{
            "name": "Cultural Anthropologist",
            "elaboration": "Proficient in studying and analyzing cultural practices and customs, this agent provides deep insights into diverse societies for your narrative.",
            "impersonations": ["Margaret Mead", "Claude Lévi-Strauss", "Zora Neale Hurston"],
            "personality_traits": ["Empathetic", "Observant", "Open-minded"],
            "goals": ["Study cultural practices", "Analyze customs", "Provide societal insights"],
            "roles": ["Cultural researcher", "Society analyst", "Tradition explorer"],
            "qualifications": ["Anthropology expert", "Cross-cultural communicator", "Ethnographer"]
        }
    }
]

```

Then when you have your agent data ready, you can run the following command to create your agents in the database:

```bash
app='shopper'
python manage.py init_agents ${app}
```

## Quick guide to creating your own phusis implementation

The name of the example implementation here is 'shopper'

1. Make sure you have django installed
    - ```bash
      python -m django --version
2. Create a new django app within the myuz project
    - ```bash
      python manage.py startapp shopper
3. Write your first view - `shopper/views.py`
    - ```python
      from django.http import HttpResponse

      def index(request):
      return HttpResponse("Hello, world. You're at the shoppper index.")
4. Wire up your new view - `shopper/urls.py`
    - ```python
      from django.urls import path
      from . import views

      urlpatterns = [
          path('', views.index, name='index'),
      ]
5. Add your new app to the myuz project - `myuz/settings.py`
    - ```python
      INSTALLED_APPS = [
          'shopper.apps.ShopperConfig',
          'noveller.apps.NovellerConfig',
          'phusis.apps.PhusisConfig',
          ...
      ]
6. Make the shopper app modificalbe in the admin view - `shopper/admin.py`
    - ```python
      from django.contrib import admin
      from django.db import models

      for model in dir():
          try:
              if issubclass(eval(model), models.Model):
                  admin.site.register(eval(model))
          except:
              pass
7. Based on what you believe is required for an agent swarm to complete the project of your choosing, create your agent, project and project atributte class definitions in `shoppper/` (noveller's implementation is a good example)
     - (Optional) Create your own pre-defined agents in JSON format to preload into your app. Store them in 
        - `shopper/phusis-projects/shopper/init_agents/`
     - (Optional) Create your own pre-defined project in JSON format to preload into your app. Store them in 
        - `shopper/phusis-projects/shopper/projects/${project_name}/init_project/`
8. Run the following commands to create the tables for your custom implementations in the database:
    - ```bash
      python manage.py makemigrations shopper --empty
      python manage.py makemigrations phusis --empty
      python manage.py makemigrations phusis
      python manage.py makemigrations shopper
      python manage.py migrate 

      #and if you created JSON data for agents and project
      python manage.py init_agents shopper
      python manage.py init_project shopper
9. Run the server:
    - ```bash
      python manage.py runserver
    - then navigate to `localhost:8000/admin` to see your new app in the admin view 
    - and `localhost:8000/shopper` to see shopper's html hello world     