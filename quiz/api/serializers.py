from rest_framework import serializers

from quiz.models import Answers, Question, QuizHistory

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['text']


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'author', 'text', 'mark', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        question = Question.objects.get(text=validated_data.get('text'))

        if question:
            existing_answers = question.answers.values_list('text', flat=True)
            for ans in answers_data:
                if ans['text'] not in existing_answers:
                    Answers.objects.create(question=question, **ans)
            return question

        question = Question.objects.create(**validated_data)
        for ans in answers_data:
            Answers.objects.create(question=question, **ans)
        return question



class QuestionInfoSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['text', 'answers']


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
