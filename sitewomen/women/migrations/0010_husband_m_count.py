# Generated by Django 5.2 on 2025-04-29 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0009_alter_women_husband'),
    ]

    operations = [
        migrations.AddField(
            model_name='husband',
            name='m_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
