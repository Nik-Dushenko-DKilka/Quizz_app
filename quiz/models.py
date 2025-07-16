from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100 ,unique=True)
    mark = models.PositiveIntegerField(default=5)

    def __str__(self) -> str:
        return f'Word: {self.text}, mark: {self.mark}'


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=100)

    class Meta:
        unique_together = ('question', 'text') 


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')



class QuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} learned '{self.question.text}' at {self.answered_at}"

    @staticmethod
    def total_marks(user):
        return QuizHistory.objects.filter(user=user).aggregate(
            total=models.Sum('question__mark')
        )['total'] or 0
