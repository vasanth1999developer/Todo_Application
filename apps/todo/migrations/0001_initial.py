# Generated by Django 5.1.4 on 2024-12-18 09:52

import apps.common.helpers
import apps.common.model_fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('image', apps.common.model_fields.AppImageField(blank=True, max_size=1, null=True, upload_to=apps.common.helpers.file_upload_path)),
                ('username', models.CharField(default=None, max_length=512, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('image', apps.common.model_fields.AppImageField(blank=True, max_size=1, null=True, upload_to=apps.common.helpers.file_upload_path)),
                ('file', apps.common.model_fields.AppSingleFileField(blank=True, max_size=10, null=True, upload_to=apps.common.helpers.file_upload_path)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task_date', models.DateField()),
                ('is_complete', models.BooleanField(default=False)),
                ('on_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reminder_time', models.DateTimeField()),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reminder', to='todo.task')),
            ],
        ),
    ]
