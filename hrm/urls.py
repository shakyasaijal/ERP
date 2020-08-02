from django.urls import path, include
from hrm import views

urlpatterns = [
    path('trainings', views.list_trainings, name="hrm-trainings"),
    path('add-trainings', views.Trainings.as_view(), name="add-trainings"),
    path('trainings/<int:id>', views.TrainingsEdit.as_view(), name="edit-trainings"),
    path('training-delete/<int:id>', views.delete_training, name="delete-training")

]
