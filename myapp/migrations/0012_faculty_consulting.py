# Generated by Django 3.2.20 on 2023-10-14 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_rename_marks_marks_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='consulting',
            field=models.CharField(default='', max_length=20),
        ),
    ]
