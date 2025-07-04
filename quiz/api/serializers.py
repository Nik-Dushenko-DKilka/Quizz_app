from rest_framework import serializers

from quiz.models import Question, QuizHistory


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    answer = serializers.CharField(write_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'author',
            'text',
            'mark',
            'answer'
        ]


class QuestionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'text',
            'answer'
        ]


class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()


class QuizHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    question = QuestionInfoSerializer(read_only=True)

    class Meta:
        model = QuizHistory
        fields = [
            'id',
            'user',
            'question',
            'answered_at',
        ]
