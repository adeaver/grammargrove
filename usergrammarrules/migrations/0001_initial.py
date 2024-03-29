# Generated by Django 4.2.2 on 2023-06-17 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grammarrules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGrammarRuleEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notes', models.TextField(null=True)),
                ('grammar_rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grammarrules.grammarrule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='usergrammarruleentry',
            constraint=models.UniqueConstraint(fields=('user', 'grammar_rule'), name='user_grammar_rule_idx'),
        ),
    ]
