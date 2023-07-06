from django.urls import path
from .views import AttendanceListCreateView, AttendanceRetrieveUpdateDeleteView

urlpatterns = [
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance_list_create'),
    path('attendance/<int:pk>/', AttendanceRetrieveUpdateDeleteView.as_view(), name='attendance_retrieve_update_delete'),
]
