# Generated by Django 3.1.7 on 2022-07-11 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0003_auto_20220711_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]