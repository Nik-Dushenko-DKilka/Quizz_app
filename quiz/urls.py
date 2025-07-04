from rest_framework.routers import DefaultRouter
from quiz.views import HistoryViewSet, QuestionViewSet


app_name = 'quiz'

router = DefaultRouter()
router.register(r'question', QuestionViewSet, basename='questions')
router.register(r'history', HistoryViewSet, basename='answer')

urlpatterns = router.urls
