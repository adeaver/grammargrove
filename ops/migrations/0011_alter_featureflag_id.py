# Generated by Django 4.2.4 on 2023-08-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0010_remove_featureflag_valid_featureflag_int_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featureflag',
            name='id',
            field=models.TextField(choices=[('grammar_rule_fetches_enabled', 'grammar_rule_fetches_enabled'), ('practice_reminder_emails_enabled', 'practice_reminder_emails_enabled'), ('recaptcha_enabled', 'recaptcha_enabled'), ('grammar_rule_scavenger_enabled', 'grammar_rule_scavenger_enabled'), ('grammar_rule_validation_enabled', 'grammar_rule_validation_enabled'), ('use_only_high_quality_grammar_rules_examples_enabled', 'use_only_high_quality_grammar_rules_examples_enabled'), ('number_of_validation_examples_per_cycle', 'number_of_validation_examples_per_cycle')], editable=False, primary_key=True, serialize=False),
        ),
    ]
