from django.db import models
import uuid


class PromptType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
class Prompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    prompt_type = models.ForeignKey('PromptType', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)    

    def __str__(self):
        return self.name
    

class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)

    def __str__(self):
        return self.name

class AgentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)

    def __str__(self):
        return self.name

class AgentsModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)

    def __str__(self):
        return self.name    
    
    