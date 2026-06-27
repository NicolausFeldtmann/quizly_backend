from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import QuizzSerializer, SingleQuizzSerializer
from quizzes_app.models import QuizzModel, QuestionsModel
from .permissions import IsOwnerOrAdmin

class QuizzListCreateView(generics.ListCreateAPIView):
    queryset = QuizzModel.objects.all()
    serializer_class = QuizzSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SingleQuizzView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizzModel.objects.all()
    serializer_class = SingleQuizzSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


