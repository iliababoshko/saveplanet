# Generated by Django 4.1.7 on 2023-03-09 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0015_results_student_answerstudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='question',
            field=models.TextField(help_text='Введите вопрос', verbose_name='Вопрос'),
        ),
    ]
