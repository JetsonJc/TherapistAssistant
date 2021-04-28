from django.urls import path
from .authentication import views as auth
from .therapist import views as therapist
from .patient import views as patient

urlpatterns = [
    path('login/', auth.AuthenticationDetail.as_view()),
    path('therapists/<int:patient_id>/patients/', therapist.PatientList.as_view()),
    path('patients/exercise/<int:exercise_id>/results/<int:results_id>/', patient.PatientResultsList.as_view()),
]