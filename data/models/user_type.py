from django.db import models

class UserType(models.Model):
    id = models.AutoField(
        help_text="Identificador de la tabla.",
        primary_key=True
    )
    user_type = models.CharField(
        unique=True,
        max_length=50, 
        help_text="User type."
    )
    description = models.CharField(
        max_length=255,
        help_text="User type description."
    )

    class Meta:
            db_table = 'user_type'