# Generated by Django 4.1.7 on 2023-03-09 14:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0018_alter_userpay_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tests',
            name='userpay',
            field=models.ManyToManyField(help_text='Выберите покупателей', null=True, to=settings.AUTH_USER_MODEL, verbose_name='Покупатели'),
        ),
    ]
