# Generated by Django 5.1.3 on 2024-12-18 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_alter_reminder_modified_at_alter_task_modified_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]