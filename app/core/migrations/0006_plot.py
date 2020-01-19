# Generated by Django 2.1.15 on 2020-01-15 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200115_0217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('slope', models.FloatField()),
                ('aspect', models.CharField(max_length=255)),
                ('stand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Stand')),
            ],
        ),
    ]