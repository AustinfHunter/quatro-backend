# Generated by Django 5.1.1 on 2024-10-31 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_userfitnessprofile_daily_calorie_goal_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userfitnessprofile",
            name="age",
            field=models.IntegerField(null=True),
        ),
    ]