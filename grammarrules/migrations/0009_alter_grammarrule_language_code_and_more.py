# Generated by Django 4.2.2 on 2023-06-20 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grammarrules', '0008_grammarrule_language_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grammarrule',
            name='language_code',
            field=models.TextField(choices=[('ZHCHS', 'Simplified'), ('ZHCHT', 'Traditional'), ('ENG', 'English')]),
        ),
        migrations.AlterField(
            model_name='grammarruleexampleprompt',
            name='language_code',
            field=models.TextField(choices=[('ZHCHS', 'Simplified'), ('ZHCHT', 'Traditional'), ('ENG', 'English')]),
        ),
        migrations.AlterField(
            model_name='grammarrulehumanverifiedpromptexample',
            name='language_code',
            field=models.TextField(choices=[('ZHCHS', 'Simplified'), ('ZHCHT', 'Traditional'), ('ENG', 'English')]),
        ),
    ]
