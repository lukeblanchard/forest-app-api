# Generated by Django 2.1.15 on 2020-01-20 20:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200120_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='sample_design',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, null=True, size=5),
        ),
    ]
