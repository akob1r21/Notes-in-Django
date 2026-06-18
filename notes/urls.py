from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes'),
    path('create-notes', views.create_notes, name='create_notes'),
    path('update-notes/<int:pk>', views.update_note, name='update_notes'),
    path('delete-notes/<int:pk>', views.delete_note, name='delete_notes'),
]
