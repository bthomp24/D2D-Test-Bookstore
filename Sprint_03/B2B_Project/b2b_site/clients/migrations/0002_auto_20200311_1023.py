# Generated by Django 3.0.4 on 2020-03-11 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='site_slug',
        ),
        migrations.AddField(
            model_name='company',
            name='slugs',
            field=models.ManyToManyField(to='clients.Site_Slug'),
        ),
    ]
