# Generated by Django 4.1.7 on 2023-03-06 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_name_customuser_patronymic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='region',
            field=models.CharField(choices=[('72', 'Тюменская обл.'), ('story', 'Our Story')], help_text='Выберите регион вашего проживания', max_length=255, null=True, verbose_name='Регион'),
        ),
    ]
