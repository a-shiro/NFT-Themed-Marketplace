# Generated by Django 4.0.3 on 2022-04-22 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_generic_features', '0011_alter_favorite_nft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nft',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]