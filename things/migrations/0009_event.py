# Generated by Django 4.2.3 on 2023-07-09 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0008_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=2)),
                ('data', models.TextField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
