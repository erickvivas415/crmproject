# Generated by Django 5.1.3 on 2025-06-18 02:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_job'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heard_about', models.CharField(choices=[('LinkedIn', 'LinkedIn'), ('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('LIF Website', 'LIF Website'), ('Other', 'Other')], default='LIF Website', max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('area_of_study', models.CharField(max_length=255)),
                ('resilience_growth', models.TextField()),
                ('career_vision_strategy', models.TextField()),
                ('passion_for_finance', models.TextField()),
                ('optional_additonal_info', models.TextField(blank=True, null=True)),
                ('transcript', models.FileField(blank=True, null=True, upload_to='transcripts/')),
                ('award_letter', models.FileField(blank=True, null=True, upload_to='award_letters/')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scholarship', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Scholarship Application',
                'verbose_name_plural': 'Scholarship Applications',
                'ordering': ['user'],
            },
        ),
    ]
