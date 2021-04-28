from django.db import models
from .exercise import Exercise
from .patient_routine import PatientRoutine

class ResultExercise(models.Model):
    id = models.AutoField(
        help_text="Identificador de la tabla.",
        primary_key=True
    )
    exercise = models.ForeignKey(
        Exercise,
        help_text="Exercise identifier.",
        on_delete=models.DO_NOTHING
    )
    patient_routine = models.ForeignKey(
        PatientRoutine,
        help_text="Identifier of the patient routine relationship.",
        on_delete=models.DO_NOTHING
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date of registration of a new relationship."
    )
    path_video = models.CharField(
        unique=True,
        max_length=255,
        help_text="Patient video path."
    )
    path_points = models.CharField(
        unique=True,
        max_length=255,
        help_text="File path with patient points."
    )
    path_feedback = models.CharField(
        unique=True,
        max_length=255,
        help_text="Path with patient results by program."
    )

    class Meta:
            db_table = 'result_exercise'