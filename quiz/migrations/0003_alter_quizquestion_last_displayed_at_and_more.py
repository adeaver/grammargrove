# Generated by Django 4.2.2 on 2023-06-24 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quizquestion_user_grammar_rule_entry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='last_displayed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='number_of_times_displayed',
            field=models.IntegerField(default=0),
        ),
    ]
