# Generated by Django 4.2.2 on 2023-07-01 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_remove_quizquestion_last_answered_correctly_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizresponse',
            old_name='last_displayed_at',
            new_name='created_at',
        ),
    ]