# Generated by Django 5.0.1 on 2024-01-29 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gingko', '0005_alter_submission_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gingko.result'),
        ),
    ]
