# Generated by Django 4.2.3 on 2023-07-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0004_eventt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_ahmad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('data', models.JSONField()),
            ],
        ),
    ]
