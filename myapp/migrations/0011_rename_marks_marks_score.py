# Generated by Django 3.2.20 on 2023-10-13 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_marks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marks',
            old_name='Marks',
            new_name='Score',
        ),
    ]
