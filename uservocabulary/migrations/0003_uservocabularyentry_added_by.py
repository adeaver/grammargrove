# Generated by Django 4.2.2 on 2023-07-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uservocabulary', '0002_uservocabularyentry_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservocabularyentry',
            name='added_by',
            field=models.TextField(choices=[('user', 'User'), ('onboarding', 'Onboarding')], default='user'),
        ),
    ]
