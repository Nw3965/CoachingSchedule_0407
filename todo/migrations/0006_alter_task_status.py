# Generated by Django 3.2.13 on 2022-06-19 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='Status',
            field=models.CharField(choices=[('予定', '予定'), ('実績', '実績'), ('スキップ', 'スキップ')], default='予定', max_length=16),
        ),
    ]
