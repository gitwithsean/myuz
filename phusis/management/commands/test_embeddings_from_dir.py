from django.core.management.base import BaseCommand
from phusis.agent_models import EmbeddingsAgentSingleton

class Command(BaseCommand):
    help = 'Runs a function in MyModel'

    def handle(self, *args, **options):
        embeddingsAgent = EmbeddingsAgentSingleton()
        embeddingsAgent.embed_files_from_dir()

