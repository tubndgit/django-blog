# Generated by Django 2.2 on 2020-05-09 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200509_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
    ]
