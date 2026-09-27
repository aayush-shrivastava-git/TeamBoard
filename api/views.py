from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task, Comment, KBEntry, QueryLog
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer,RegisterSerializer,KBEntrySerializer,QueryLogSerializer
# from django.db.models import Q
from django.db import transaction
from django.db.models import Q,Count
from .permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "company_name": user.company.company_name,
                "api_key": user.company.api_key,
            },
            status=status.HTTP_200_OK,
        )

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "username": user.username,
                "company_name": user.company.company_name,
                "api_key": user.company.api_key,
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user) | Project.objects.filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        project.members.add(self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            project__members=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            task__project__members=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class KBQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        search_term = request.data.get("search", "").strip()

        if not search_term:
            return Response(
                {"error": "search is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        company = request.user.company

        with transaction.atomic():
            entries = KBEntry.objects.filter(
                Q(question__icontains=search_term)
                | Q(answer__icontains=search_term)
            )
            count = entries.count()

            results = KBEntrySerializer(entries, many=True).data

            QueryLog.objects.create(
                company=company,
                search_term=search_term,
                results_count=len(results),
            )

        return Response(
            {
                "search": search_term,
                "count": count,
                "results": results,
            },
            status=status.HTTP_200_OK,
        )

class UsageSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        total_queries = QueryLog.objects.aggregate(
            total=Count("id")
        )["total"]

        active_companies = QueryLog.objects.values(
            "company"
        ).distinct().count()

        top_search_terms = (
            QueryLog.objects
            .values("search_term")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        return Response({
            "total_queries": total_queries,
            "active_companies": active_companies,
            "top_search_terms": list(top_search_terms),
        })