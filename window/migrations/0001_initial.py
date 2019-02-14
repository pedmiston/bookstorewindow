# Generated by Django 2.1.5 on 2019-02-13 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "google_book_id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=100)),
                ("authors", models.CharField(max_length=100)),
                ("image", models.URLField()),
                ("publisher", models.CharField(max_length=100)),
                ("subtitle", models.CharField(blank=True, max_length=200)),
            ],
        )
    ]
