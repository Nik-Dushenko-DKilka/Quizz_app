from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import OuterRef, Exists
from django.db.models.functions import Lower, Trim

from quiz.api.serializers import QuestionSerializer, AnswerSerializer, QuizHistorySerializer
from quiz.models import Question, QuizHistory, UserAnswer


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        history_subquery = QuizHistory.objects.filter(
            user=user,
            question=OuterRef('pk')
        )
        return Question.objects.annotate(
            is_learned=Exists(history_subquery)
        ).filter(is_learned=False)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def answer(self, request, pk=None):
        question = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_answer_text = serializer.validated_data['text'].strip().lower()
        user = request.user

        correct_answer = None
        for ans in question.answers.all():
            if ans.text.strip().lower() == user_answer_text:
                correct_answer = ans
                break
        if not correct_answer:
            return Response({"correct": False}, status=status.HTTP_200_OK)

        UserAnswer.objects.get_or_create(
            user=user,
            question=question,
            answer=correct_answer
        )

        total_correct_answers = question.answers.count()
        user_correct_answers = UserAnswer.objects.filter(user=user, question=question).count()

        if user_correct_answers == total_correct_answers:
            QuizHistory.objects.get_or_create(
                user=user,
                question=question,
            )

        return Response({"correct": True}, status=status.HTTP_200_OK)


class HistoryViewSet(viewsets.ModelViewSet):
    serializer_class = QuizHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizHistory.objects.filter(user=self.request.user).select_related('question')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        score = QuizHistory.total_marks(request.user)

        return Response({
            "score": score,
            "history": serializer.data
        }, status=status.HTTP_200_OK)
