# Generated by Django 4.2.2 on 2023-07-29 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0002_featureflag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featureflag',
            name='id',
            field=models.TextField(choices=[('grammar_rule_fetches_enabled', 'grammar_rule_fetches_enabled'), ('practice_reminder_emails_enabled', 'practice_reminder_emails_enabled')], editable=False, primary_key=True, serialize=False),
        ),
    ]
