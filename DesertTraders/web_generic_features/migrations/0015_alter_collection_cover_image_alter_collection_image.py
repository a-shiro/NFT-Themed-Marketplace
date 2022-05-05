# Generated by Django 4.0.3 on 2022-05-05 10:25

import DesertTraders.web_generic_features.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_generic_features', '0014_collection_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='collections/', validators=[DesertTraders.web_generic_features.validators.max_image_size]),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ImageField(upload_to='collections/', validators=[DesertTraders.web_generic_features.validators.max_image_size]),
        ),
    ]
