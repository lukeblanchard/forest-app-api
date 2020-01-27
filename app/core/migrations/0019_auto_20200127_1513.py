# Generated by Django 2.1.15 on 2020-01-27 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20200121_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='metric_system',
        ),
        migrations.AddField(
            model_name='project',
            name='measurement_system',
            field=models.CharField(choices=[('english', 'english'), ('metric', 'metric')], default='metric', max_length=8),
        ),
        migrations.AlterField(
            model_name='sampledesign',
            name='var',
            field=models.CharField(choices=[('HGT', 'HGT'), ('DBH', 'DBH')], default=None, max_length=3),
        ),
        migrations.AlterField(
            model_name='tree',
            name='live_crown_ratio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='treereference',
            name='max_density_index',
            field=models.IntegerField(default=None),
        ),
    ]
