# Generated by Django 5.2.1 on 2025-07-04 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_mark', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.course')),
                ('exam_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.examtype')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.subject')),
            ],
        ),
        migrations.CreateModel(
            name='MarkRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('grade', models.CharField(max_length=40, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.marks')),
            ],
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]
