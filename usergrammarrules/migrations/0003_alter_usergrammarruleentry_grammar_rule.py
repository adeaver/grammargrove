# Generated by Django 4.2.2 on 2023-06-23 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grammarrules', '0009_alter_grammarrule_language_code_and_more'),
        ('usergrammarrules', '0002_usergrammarruleentry_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergrammarruleentry',
            name='grammar_rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grammar_rule', to='grammarrules.grammarrule'),
        ),
    ]
