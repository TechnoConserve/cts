# Generated by Django 3.0.7 on 2020-06-28 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant_database', '0007_auto_20200628_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(blank=True, max_length=70, unique=True),
        ),
    ]
