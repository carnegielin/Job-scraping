# Generated by Django 4.1 on 2022-08-20 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='detail_link',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
