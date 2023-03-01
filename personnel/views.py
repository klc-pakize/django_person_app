from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView,  RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import Department, Personnel
from .serializers import DepartmentSerializer, PersonnelSerializer, DepartmentPersonnelSerializer
from .permissions import IsStaffOrReadOnly, IsOwnerAndStaffOrReadOnly

# Create your views here.

class DepartmentView(ListCreateAPIView):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class PersonnelView(ListCreateAPIView):

    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = [IsAuthenticated]  # Unregistered users cannot take any action


#! Non-staff users can only do get, staff users can create. We can do this with permissions, but we have seen that it is done in a different way.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user.is_staff:
            personnel = self.perform_create(serializer)
            data = {
                "message":f"Personnel {personnel.first_name} saved successfully.",
                "personnel": serializer.data
            }

        else:
            data = {
                "message":f"You are not authorized.",
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        person = serializer.save()
        return person


class PersonnelDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = [IsAuthenticated, IsOwnerAndStaffOrReadOnly]


class DepartmentDetail(ListAPIView):
    serializer_class = DepartmentPersonnelSerializer
    queryset = Department.objects.all()
    
#! We created it to be able to write dynamic endpoints

    def get_queryset(self):
        name = self.kwargs["department"]
        return Department.objects.filter(name__iexact=name)  # iexact = do not make case insensitive


class DepartmentDetailView(RetrieveAPIView):
    serializer_class = DepartmentPersonnelSerializer
    queryset = Department.objects.all()
    lookup_field = "name"