# Generated by Django 4.2.2 on 2023-07-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grammarrules', '0009_alter_grammarrule_language_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grammarrulecomponent',
            name='part_of_speech',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='GrammarRuleHumanVerifiedPromptExampleComponent',
        ),
    ]
