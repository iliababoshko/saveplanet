# Generated by Django 4.1.7 on 2023-02-20 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0003_testage_themetest_remove_tests_name_tests_agedef_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testage',
            options={'ordering': ['agedef']},
        ),
        migrations.AlterModelOptions(
            name='tests',
            options={'ordering': ['agedef']},
        ),
        migrations.AlterModelOptions(
            name='themetest',
            options={'ordering': ['name']},
        ),
    ]
