# Generated by Django 4.2.2 on 2023-07-01 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_quizresponse_example_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizresponse',
            old_name='example_id',
            new_name='grammar_rule_example',
        ),
    ]