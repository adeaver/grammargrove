# Generated by Django 4.2.2 on 2023-08-04 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grammarrules', '0014_grammarruleexample_validation_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='grammarruleexample',
            name='validation_result',
            field=models.TextField(null=True),
        ),
    ]
