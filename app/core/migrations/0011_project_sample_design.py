# Generated by Django 2.1.15 on 2020-01-20 17:17

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_project_sample_design'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sample_design',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), default=list, null=True, size=5),
        ),
    ]
