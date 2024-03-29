# Generated by Django 2.2.2 on 2019-08-08 17:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Information Product')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Description')),
                ('asset_id', models.CharField(blank=True, default='', max_length=100, verbose_name='Product ID')),
                ('content_type', models.CharField(blank=True, choices=[('Alteryx App', 'Alteryx App'), ('Alteryx Workflow', 'Alteryx Workflow')], default='', max_length=20, verbose_name='Content Type')),
                ('project_name', models.CharField(blank=True, max_length=100, verbose_name='Project')),
                ('asset_url', models.URLField(blank=True, verbose_name='URL')),
                ('image_url', models.CharField(blank=True, max_length=100, verbose_name='Preview Image')),
                ('use_count', models.PositiveIntegerField(default=0, verbose_name='Run or Views')),
                ('asset_status', models.CharField(blank=True, default='New', max_length=50, verbose_name='Status')),
                ('created_at', models.DateField(default=datetime.date.today, null=True, verbose_name='Created')),
                ('modified_at', models.DateField(default=datetime.date.today, null=True, verbose_name='Modified')),
                ('published_at', models.DateField(default=datetime.date.today, null=True, verbose_name='Published')),
                ('content_id', models.PositiveIntegerField(default=0, null=True, verbose_name='Content ID')),
                ('repo_location', models.CharField(blank=True, default='', max_length=150, verbose_name='Repository')),
                ('doc_location', models.CharField(blank=True, default='', max_length=150, verbose_name='Documentation')),
                ('jira_location', models.CharField(blank=True, default='', max_length=150, verbose_name='JIRA Ticket')),
                ('asset_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Information Product',
                'ordering': ['-use_count'],
            },
        ),
    ]
