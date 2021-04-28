from django.db import models
from .user_type import UserType

class User(models.Model):
    id = models.AutoField(
        help_text="Identificador de la tabla.",
        primary_key=True
    )
    name = models.CharField(
        max_length=50, 
        help_text="Patient name."
    )
    last_name = models.CharField(
        max_length=50,
        help_text="Patient's first surname."
    )
    second_name = models.CharField(
        null=True,
        max_length=50,
        help_text="Patient's second last name."
    )
    email = models.EmailField(
        unique=True,
        help_text="Patient email."
    )
    password = models.CharField(
        max_length=80, 
        help_text="Patient password."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="New patient registration date."
    )
    user_type = models.ForeignKey(
        UserType,
        null=True,
        help_text="Therapist identifier.",
        on_delete=models.DO_NOTHING
    )
    therapist = models.ForeignKey(
        'self',
        null=True,
        help_text="Therapist identifier.",
        on_delete=models.DO_NOTHING
    )

    class Meta:
            db_table = 'user'