# Generated by Django 5.0.1 on 2024-02-01 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gingko', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='end_index',
            field=models.IntegerField(null=True),
        ),
    ]
