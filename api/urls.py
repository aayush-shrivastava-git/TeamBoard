from rest_framework.routers import DefaultRouter
from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .views import ProjectViewSet, TaskViewSet, CommentViewSet,RegisterView, KBEntryViewSet,QueryLogViewSet,KBQueryView,UsageSummaryView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProjectViewSet,
    TaskViewSet,
    CommentViewSet,
    RegisterView,
    KBQueryView,
    UsageSummaryView,
    LoginView,
)

router = DefaultRouter()

router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")
router.register("comments", CommentViewSet, basename="comment")


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("kb/query/", KBQueryView.as_view(), name="kb-query"),
    path(
            "admin/usage-summary/",
            UsageSummaryView.as_view(),
            name="usage-summary",
        ),
] + router.urls