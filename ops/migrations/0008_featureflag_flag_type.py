# Generated by Django 4.2.2 on 2023-08-07 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0007_alter_featureflag_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureflag',
            name='flag_type',
            field=models.TextField(choices=[('boolean', 'boolean'), ('integer', 'integer')], default='boolean'),
        ),
    ]
