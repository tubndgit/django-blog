# Generated by Django 2.2 on 2020-05-21 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_post_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(default='', null=True, upload_to='django-summernote/images/'),
        ),
    ]