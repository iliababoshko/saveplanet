# Generated by Django 4.1.7 on 2023-03-03 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0008_alter_themetest_options_remove_answerstudent_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Ученики', 'verbose_name_plural': 'Ученики'},
        ),
        migrations.RemoveField(
            model_name='student',
            name='school',
        ),
        migrations.RemoveField(
            model_name='student',
            name='town',
        ),
    ]
