from django.db import models
from .user import User
from .routine import Routine

class PatientRoutine(models.Model):
    id = models.AutoField(
        help_text="Identificador de la tabla.",
        primary_key=True
    )
    routine = models.ForeignKey(
        Routine,
        help_text="Routine identifier.",
        on_delete=models.DO_NOTHING
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date of registration of a new relationship."
    )
    feedback = models.TextField(
        default=False,
        help_text="Therapist feedback."
    )
    active = models.BooleanField(
        default=True,
        help_text="Flag that indicates if the routine is active."
    )
    instructions = models.TextField(
        help_text="Instructions from the therapist on the routine."
    )
    patient = models.ForeignKey(
        User,
        help_text="Patient identifier.",
        on_delete=models.DO_NOTHING
    )

    class Meta:
            db_table = 'patient_routine'
