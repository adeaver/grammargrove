# Generated by Django 4.2.2 on 2023-07-01 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0003_alter_quizquestion_last_displayed_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='last_answered_correctly_at',
        ),
        migrations.RemoveField(
            model_name='quizquestion',
            name='number_of_times_answered_correctly',
        ),
        migrations.CreateModel(
            name='QuizResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_correct', models.BooleanField(default=False)),
                ('last_displayed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]