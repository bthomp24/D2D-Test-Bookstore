# Generated by Django 3.0.2 on 2020-02-14 19:33

from django.db import migrations, models
import test_bookstore.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('ISBN', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('primary_author', models.CharField(max_length=100)),
                ('secondary_authors', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('description', models.TextField()),
                ('publisher', models.CharField(max_length=200)),
                ('release_date', models.CharField(max_length=15)),
                ('price', models.CharField(max_length=50)),
                ('series', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('volume_number', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('is_available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f', models.FileField(upload_to=test_bookstore.models.user_directory_path)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]