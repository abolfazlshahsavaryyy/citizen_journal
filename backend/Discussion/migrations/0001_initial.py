# Generated by Django 5.2.4 on 2025-07-12 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the discussion (e.g., group or chat title)', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Optional description or context for the discussion')),
                ('is_active', models.BooleanField(default=True, help_text='Can be used to archive or deactivate a discussion')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the discussion was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last time the discussion was updated')),
                ('page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Page.page')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the Topic was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last time the Topic was updated')),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='Discussion.discussion')),
            ],
        ),
    ]
