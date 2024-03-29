# Generated by Django 4.2.2 on 2023-07-27 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('grammarrules', '0013_grammarruleexample_contains_non_labeled_words_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usergrammarrules', '0004_usergrammarruleentry_added_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergrammarruleentry',
            name='notes',
        ),
        migrations.CreateModel(
            name='UserGrammarRuleNote',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('example', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grammarrules.grammarruleexample')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'example'], name='usergrammar_user_id_de7d22_idx')],
            },
        ),
    ]
