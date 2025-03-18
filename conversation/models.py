from django.db import models
import uuid

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Conversation {self.id} - {self.unique_identifier}"