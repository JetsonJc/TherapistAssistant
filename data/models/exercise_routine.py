from django.db import models
from .exercise import Exercise
from .routine import Routine

class ExerciseRoutine(models.Model):
    id = models.AutoField(
        help_text="Identificador de la tabla.",
        primary_key=True
    )
    exercise = models.ForeignKey(
        Exercise,
        help_text="Exercise identifier.",
        on_delete=models.DO_NOTHING
    )
    routine = models.ForeignKey(
        Routine,
        help_text="Routine identifier.",
        on_delete=models.DO_NOTHING
    )

    class Meta:
        db_table = 'exercise_routine'
