# Generated by Django 4.0.3 on 2022-04-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_generic_features', '0013_profile_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='collections/'),
        ),
    ]
