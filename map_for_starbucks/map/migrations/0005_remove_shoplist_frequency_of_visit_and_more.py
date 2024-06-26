# Generated by Django 4.1 on 2023-12-28 07:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("map", "0004_shoplist_frequency_of_visit_shoplist_last_visit"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shoplist",
            name="frequency_of_visit",
        ),
        migrations.RemoveField(
            model_name="shoplist",
            name="last_visit",
        ),
        migrations.AddField(
            model_name="shoplist",
            name="non_frequency_of_visit",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="non_frequency_of_visit"
            ),
        ),
        migrations.AddField(
            model_name="shoplist",
            name="non_last_visit",
            field=models.CharField(
                blank=True, max_length=300, null=True, verbose_name="non_last_visit"
            ),
        ),
        migrations.AddField(
            model_name="shoplist",
            name="yuya_frequency_of_visit",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="yuya_frequency_of_visit"
            ),
        ),
        migrations.AddField(
            model_name="shoplist",
            name="yuya_last_visit",
            field=models.CharField(
                blank=True, max_length=300, null=True, verbose_name="yuya_last_visit"
            ),
        ),
    ]
