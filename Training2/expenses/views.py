from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .permissions import IsOwner
from .serializers import ExpensesSerializer
from .models import Expense
from rest_framework import permissions
from .permissions import IsOwner


class ExpenseListAPIView(ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class=ExpensesSerializer
    queryset = Expense.objects.all()
    


    def perform_create(self, serializer):
        return serializer.save(owner= self.request.user)


    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    serializer_class=ExpensesSerializer
    queryset = Expense.objects.all()
    lookup_field= "id"


    # def perform_create(self, serializer):
    #     return serializer.save(owner= self.request.user)


    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)

