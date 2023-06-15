# Generated by Django 4.2.2 on 2023-06-15 02:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('grammarrules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grammarrule',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='grammarrulecomponent',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]