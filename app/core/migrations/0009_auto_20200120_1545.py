# Generated by Django 2.1.15 on 2020-01-20 15:45

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_tree'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sample_design',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), default=list, null=True, size=5),
        ),
        migrations.AlterField(
            model_name='plot',
            name='stand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plots', to='core.Stand'),
        ),
        migrations.AlterField(
            model_name='stand',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stands', to='core.Project'),
        ),
        migrations.AlterField(
            model_name='tree',
            name='plot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trees', to='core.Plot'),
        ),
    ]
