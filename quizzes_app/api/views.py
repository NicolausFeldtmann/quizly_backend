from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import QuizzSerializer, SingleQuizzSerializer, UpdateSerializer
from quizzes_app.models import QuizzModel, QuestionsModel
from .permissions import IsOwnerOrAdmin

class QuizzListCreateView(generics.ListCreateAPIView):
    queryset = QuizzModel.objects.all()
    serializer_class = QuizzSerializer
    permission_classes = [IsAuthenticated]

    def get_ueryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return QuizzModel.objects.filter(user=self.request.user)
        return QuizzModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SingleQuizzView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = QuizzModel.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateSerializer
        return SingleQuizzSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return QuizzModel.objects.all()
        return QuizzModel.objects.filter(user=self.request.user)

    def get_object(self):
        pk = self.kwargs.get('pk')
        quiz = get_object_or_404(QuizzModel, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz

