# Generated by Django 3.2.13 on 2022-09-08 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_alter_task_zoomurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='ZoomURL',
            field=models.URLField(max_length=256, verbose_name='Zoom URL'),
        ),
    ]
