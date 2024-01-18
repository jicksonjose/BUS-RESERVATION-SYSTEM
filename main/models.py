from django.db import models
import uuid
from django.db import models
import uuid
import datetime
from datetime import timedelta
from django.utils import timezone



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        abstract = True
        