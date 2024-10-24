# Generated by Django 5.1.1 on 2024-10-20 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foods", "0003_abridgedfoodnutrient_abridgedfooditem"),
    ]

    operations = [
        migrations.CreateModel(
            name="LabelNutrients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fat", models.FloatField()),
                ("saturated_fat", models.FloatField()),
                ("trans_fat", models.FloatField()),
                ("cholesterol", models.FloatField()),
                ("sodium", models.FloatField()),
                ("carbohydrates", models.FloatField()),
                ("fiber", models.FloatField()),
                ("sugars", models.FloatField()),
                ("protein", models.FloatField()),
                ("calcium", models.FloatField()),
                ("iron", models.FloatField()),
                ("potassium", models.FloatField()),
                ("calories", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="AbridgedBrandedFoodItem",
            fields=[
                ("fdc_id", models.IntegerField(primary_key=True, serialize=False)),
                ("brand_owner", models.CharField()),
                ("description", models.CharField()),
                ("serving_size", models.IntegerField()),
                ("serving_size_unit", models.IntegerField()),
                (
                    "label_nutrients",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="foods.labelnutrients",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="AbridgedFoodItem",
        ),
        migrations.DeleteModel(
            name="AbridgedFoodNutrient",
        ),
    ]
