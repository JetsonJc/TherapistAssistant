# Generated by Django 3.2 on 2021-04-12 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(help_text='Identificador de la tabla.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Exercise name.', max_length=50, unique=True)),
                ('descripcion', models.TextField(help_text='Description of the exercise.', null=True)),
                ('path_video', models.CharField(help_text='Video path.', max_length=255, unique=True)),
                ('path_points', models.CharField(help_text='Points file path.', max_length=255, unique=True)),
            ],
            options={
                'db_table': 'exercise',
            },
        ),
        migrations.CreateModel(
            name='PatientRoutine',
            fields=[
                ('id', models.AutoField(help_text='Identificador de la tabla.', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date of registration of a new relationship.')),
                ('feedback', models.TextField(default=False, help_text='Therapist feedback.')),
                ('active', models.BooleanField(default=True, help_text='Flag that indicates if the routine is active.')),
                ('instructions', models.TextField(help_text='Instructions from the therapist on the routine.')),
            ],
            options={
                'db_table': 'patient_routine',
            },
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(help_text='Identificador de la tabla.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Routine name.', max_length=50, unique=True)),
                ('descripcion', models.TextField(help_text='Description of the routine.', null=True)),
            ],
            options={
                'db_table': 'routine',
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(help_text='Identificador de la tabla.', primary_key=True, serialize=False)),
                ('user_type', models.CharField(help_text='User type.', max_length=50, unique=True)),
                ('description', models.CharField(help_text='User type description.', max_length=255)),
            ],
            options={
                'db_table': 'user_type',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(help_text='Identificador de la tabla.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Patient name.', max_length=50)),
                ('last_name', models.CharField(help_text="Patient's first surname.", max_length=50)),
                ('second_name', models.CharField(help_text="Patient's second last name.", max_length=50, null=True)),
                ('email', models.EmailField(help_text='Patient email.', max_length=254, unique=True)),
                ('password', models.CharField(help_text='Patient password.', max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='New patient registration date.')),
                ('therapist', models.ForeignKey(help_text='Therapist identifier.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='data.user')),
                ('user_type', models.ForeignKey(help_text='Therapist identifier.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='data.usertype')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='ResultExercise',
            fields=[
                ('id', models.AutoField(help_text='Identificador de la tabla.', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date of registration of a new relationship.')),
                ('path_video', models.CharField(help_text='Patient video path.', max_length=255, unique=True)),
                ('path_points', models.CharField(help_text='File path with patient points.', max_length=255, unique=True)),
                ('path_feedback', models.CharField(help_text='Path with patient results by program.', max_length=255, unique=True)),
                ('exercise', models.ForeignKey(help_text='Exercise identifier.', on_delete=django.db.models.deletion.DO_NOTHING, to='data.exercise')),
                ('patient_routine', models.ForeignKey(help_text='Identifier of the patient routine relationship.', on_delete=django.db.models.deletion.DO_NOTHING, to='data.patientroutine')),
            ],
            options={
                'db_table': 'result_exercise',
            },
        ),
        migrations.AddField(
            model_name='patientroutine',
            name='patient',
            field=models.ForeignKey(help_text='Patient identifier.', on_delete=django.db.models.deletion.DO_NOTHING, to='data.user'),
        ),
        migrations.AddField(
            model_name='patientroutine',
            name='routine',
            field=models.ForeignKey(help_text='Routine identifier.', on_delete=django.db.models.deletion.DO_NOTHING, to='data.routine'),
        ),
        migrations.CreateModel(
            name='ExerciseRoutine',
            fields=[
                ('id', models.AutoField(help_text='Identificador de la tabla.', primary_key=True, serialize=False)),
                ('exercise', models.ForeignKey(help_text='Exercise identifier.', on_delete=django.db.models.deletion.DO_NOTHING, to='data.exercise')),
                ('routine', models.ForeignKey(help_text='Routine identifier.', on_delete=django.db.models.deletion.DO_NOTHING, to='data.routine')),
            ],
            options={
                'db_table': 'exercise_routine',
            },
        ),
    ]
