from django.urls import path
from .authentication import views as auth
from .therapist import views as therapist
from .patient import views as patient
from .routine import views as routine
from .exercise import views as exercise
from .documents import views as document

urlpatterns = [
    path('login/', auth.AuthenticationDetail.as_view()),
    path('therapists/<int:patient_id>/patients/', therapist.PatientList.as_view()),
    path('patients/exercise/<int:exercise_id>/results/<int:patient_routine_id>/', patient.PatientResultsList.as_view()),
    path('routines/', routine.RoutineList.as_view()),
    path('routines/complete/', routine.CompleteRoutineList.as_view()),
    path('routines/<int:routine_id>/', routine.RoutineDetail.as_view()),
    path('exercises/', exercise.ExerciseList.as_view()),
    path('exercises/<int:exercise_id>/', exercise.ExerciseDetail.as_view()),
    path('patients/<int:patient_id>/routines/', patient.PatientRoutinesList.as_view()),
    path('patients/<int:patient_id>/routines/complete/', patient.PatientCompleteRoutinesList.as_view()),
    path('patients/<int:patient_id>/routines/<int:routine_id>/', patient.PatientRoutineDetail.as_view()),
    path('patients/exercise/results/', patient.PatientResultsCreate.as_view()),
    path('patients/result-exercise/<int:result_exercise_id>/', patient.PatientResultsDetail.as_view()),
    path('patients/exercise/<int:exercise_id>/results/<int:results_id>/', patient.PatientResultsList.as_view()),
    path('docs/', document.DocumentDetail.as_view()),
]