# Generated by Django 5.0 on 2024-05-03 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_alter_todo_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='priority',
        ),
        migrations.AddField(
            model_name='todo',
            name='priority',
            field=models.ManyToManyField(blank=True, null=True, to='todo.prioritychoices'),
        ),
    ]
