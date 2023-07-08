from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from attendance.models import Attendance
from .serializers import AttendanceSerializer
# ------------------- attendance -------------------

# List all attendance or create a new attendance
class AttendanceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['employee']  # Specify the fields to search

# Retrieve, update or delete a comment instance
class AttendanceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



