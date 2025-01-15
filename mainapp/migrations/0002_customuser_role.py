# Generated by Django 4.2.9 on 2025-01-14 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student')], default='student', max_length=10),
        ),
    ]
