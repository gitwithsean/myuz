
# myuz

<div style="display: flex; justify-content: center; align-items: center; height: 35vh;">
  <img src="./myuz/logos/phusis_logo.png" width="200" class="img-fluid" alt="Phusis Logo">
</div>

The core belief driving the Myuz platform is that the most effective AI applications arise from the collaboration between domain experts and AI systems. As demonstrated in the field of text-to-image AI generators, top-performing results are most often achieved when expert photographers work closely with AI technologies. By offering a platform for users with niche knowledge to develop custom AI-powered projects, Myuz seeks to give thinkers and creators from any field a simplified path to levaraging AI for their projects.

Myuz is a play on the word "muse" that we like to bakronym to "My Unleashed Zeal." We're hoping this name reflects the platform's goal of giving creators and thinkers extra resources to indulge their passions. For all the millions of people that lack the time it would take to devote themselves to a project close to their hearts, myuz unleash their zeal.

## myuz's current state

### Back End

There are currently two componenets to the myuz project, *phusis* and *noveller*:

**Phusis**: A Django app that serves as a platform for developing AI assited project structures. It provides abstract classes and engines for AI agents and AI developed/assisted projects to be used in various applications.

**Noveller**: An example implementation of the Phusis platform, specifically tailored for literary projects. It includes concrete classes derived from the Phusis abstract agent, such as CharacterAgents, WorldBuildingAgents, and ConflictAndResolutionAgents. Noveller implements 'Book' as the concreate of the AbstractPhusisProject class and defines concrete classes for the attributes of literary projects like Chapter, Plot, Scene, and LiteraryStyle, derived from the abstract PhusisProjectAttribute class.

By offering a customizable and adaptable platform, myuz empowers users with niche expertise to develop AI-powered applications tailored to their specific requirements. By combining their domain knowledge with the power of AI, users can create mental maps of their projects and deploy arrays of agents designed to work together, ultimately producing superior outcomes compared to existing multi-agent systems.

NOTE: In it's current incarnation, developing your own phusis project implementation requires an understanding of some of the principles of Object Oriented Programming and an ability to code in Python. While the noveller example should provide most people a good jumping off point for their own projects, we're hoping to make this more accessible in the future.

### Front End

I am currently levaraging Django's UI tools to create a prototype, but I am planning to move to a React front end in the near future. Would be very interested in collaborating with a front end developer on this project.

## Setup

### Requirements

* [python >= 3.10.6](https://www.python.org/downloads/release/python-3106/)
* [pip >= 22.0.2](https://pypi.org/project/pip/22.0.2/)
* [an openai account and API key](https://platform.openai.com/account/api-keys)
* [a pinecone account, API key and region](https://www.pinecone.io/)

The following instructions were put together and tested with WSL: Ubuntu on Windows 10 - setup may be different on your own machine

```bash
# add your secrets to the secrets folder
touch ./secrets/openai_api_key
touch ./secrets/pinecone_api_key
touch ./secrets/pinecone_api_region # this looks something like 'asia-southeast1-gcp' and can be found alongside your API key in the pinecone console


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

## Creating your own Agent definitions

For now, my own agent recipes are remaining private, but here is a guide on creating your own.

Take a look at the AbstractAgent model in `myuz/phusis/agent_models.py` for possibilities for defining your agents.

You will need to create a JSON representation of your agent and save it in the `agent_data` directory `myuz/phusis/secret_sauce/phusis-secret-sauce/agent_data`

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
python manage.py init_agents phusis
```

## Creating your own Phusis Project definitions

myuz (the django project) will be the site of multiple project types that will utilize the assistive tools of the phusis platform.

This repo provides a novel writing project type (noveller) as an example. However, there are opportunities to use the phusis platform for many other types of projects (research papers, DnD campaigns, business plans, event management, etc.).

phusis (the platform) and noveller (the application) are each apps within the myuz project. You can create your own apps to implement your own project types.

Check out the AbstractPhusisProject model and related classes in `myuz/phusis/agent_models.py` for the abstracts available to create new project types.

Then check out the implementation of those abstracts in the noveller app in `myuz/noveller/noveller_models.py`

To create your own application of the phusis platform, create a new django app within the myuz django project. For guidance you can read the Django project/app tutorial [here](https://docs.djangoproject.com/en/4.2/intro/tutorial01/) 
