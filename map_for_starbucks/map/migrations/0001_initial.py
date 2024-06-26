# Generated by Django 4.1 on 2023-07-28 01:55

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShopList",
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
                (
                    "postcode",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="postcode"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="address"
                    ),
                ),
                (
                    "prefecture",
                    models.CharField(
                        blank=True, max_length=5, null=True, verbose_name="prefecture"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="shopname"
                    ),
                ),
                (
                    "latitude",
                    models.FloatField(blank=True, null=True, verbose_name="latitude"),
                ),
                (
                    "longitude",
                    models.FloatField(blank=True, null=True, verbose_name="longitude"),
                ),
                (
                    "drivethrough",
                    models.BooleanField(
                        blank=True, null=True, verbose_name="drivethrough"
                    ),
                ),
                (
                    "businesshour",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="businesshour",
                    ),
                ),
                (
                    "closed",
                    models.BooleanField(blank=True, null=True, verbose_name="closed"),
                ),
                (
                    "yuya",
                    models.BooleanField(blank=True, null=True, verbose_name="yuya"),
                ),
                ("non", models.BooleanField(blank=True, null=True, verbose_name="non")),
                (
                    "monday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="monday"
                    ),
                ),
                (
                    "tuesday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="tuesday"
                    ),
                ),
                (
                    "wednesday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="wednesday"
                    ),
                ),
                (
                    "thursday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="thursday"
                    ),
                ),
                (
                    "friday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="friday"
                    ),
                ),
                (
                    "saturday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="saturday"
                    ),
                ),
                (
                    "sunday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="sunday"
                    ),
                ),
                (
                    "holiday",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="holiday"
                    ),
                ),
            ],
        ),
    ]
