# Generated by Django 4.0 on 2022-03-05 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_management_app', '0003_alter_timemanagement_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemanagement',
            name='date',
            field=models.DateField(unique=True, verbose_name='日付'),
        ),
    ]
