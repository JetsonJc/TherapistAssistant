from django.db import models

class Exercise(models.Model):
    id = models.AutoField(
        help_text="Identificador de la tabla.",
        primary_key=True
    )
    name = models.CharField(
        unique=True,
        max_length=50, 
        help_text="Exercise name."
    )
    descripcion = models.TextField(
        null=True,
        help_text="Description of the exercise."
    )
    path_video = models.CharField(
        unique=True,
        max_length=255,
        help_text="Video path."
    )
    path_points = models.CharField(
        unique=True,
        max_length=255,
        help_text="Points file path."
    )

    class Meta:
            db_table = 'exercise'