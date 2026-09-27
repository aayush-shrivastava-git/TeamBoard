from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    members = models.ManyToManyField(
        User,
        related_name="projects",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TODO",
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Company(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        CLIENT = "client", "Client"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company",
    )

    company_name = models.CharField(max_length=255)

    api_key = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class KBEntry(models.Model):
    class Category(models.TextChoices):
        API = "api", "API"
        DATABASE = "database", "Database"
        CLOUD = "cloud", "Cloud"
        FRAMEWORK = "framework", "Framework"
        GENERAL = "general", "General"

    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:80]

class QueryLog(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="query_logs",
    )
    search_term = models.CharField(max_length=255)
    results_count = models.IntegerField()
    queried_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.search_term