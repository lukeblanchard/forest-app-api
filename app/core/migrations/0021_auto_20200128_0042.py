# Generated by Django 2.1.15 on 2020-01-28 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_merge_20200127_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treereference',
            name='max_density_index',
            field=models.IntegerField(),
        ),
    ]
