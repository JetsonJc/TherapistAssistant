from django.db import models

class Routine(models.Model):
    id = models.AutoField(
        help_text="Identificador de la tabla.",
        primary_key=True
    )
    name = models.CharField(
        unique=True,
        max_length=50, 
        help_text="Routine name."
    )
    descripcion = models.TextField(
        null=True,
        help_text="Description of the routine."
    )

    class Meta:
            db_table = 'routine'