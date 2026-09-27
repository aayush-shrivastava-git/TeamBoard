from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_querylog"),
    ]

    operations = [
        migrations.RenameField(
            model_name="kbentry",
            old_name="content",
            new_name="answer",
        ),
        migrations.RenameField(
            model_name="kbentry",
            old_name="title",
            new_name="question",
        ),
        migrations.AddField(
            model_name="kbentry",
            name="category",
            field=models.CharField(
                choices=[
                    ("api", "API"),
                    ("database", "Database"),
                    ("cloud", "Cloud"),
                    ("framework", "Framework"),
                    ("general", "General"),
                ],
                default="general",
                max_length=20,
            ),
        ),
        migrations.RemoveField(
            model_name="kbentry",
            name="company",
        ),
        migrations.RenameField(
            model_name="querylog",
            old_name="created_at",
            new_name="queried_at",
        ),
        migrations.RenameField(
            model_name="querylog",
            old_name="query",
            new_name="search_term",
        ),
        migrations.AddField(
            model_name="querylog",
            name="results_count",
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name="querylog",
            name="user",
        ),
    ]