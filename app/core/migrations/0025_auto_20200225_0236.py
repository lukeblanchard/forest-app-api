# Generated by Django 2.1.15 on 2020-02-25 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200208_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='number',
            field=models.IntegerField(),
        ),
    ]
