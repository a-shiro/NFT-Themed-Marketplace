# Generated by Django 4.0.3 on 2022-04-20 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_generic_features', '0010_rename_my_collection_profile_collection_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='nft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web_generic_features.nft'),
        ),
    ]
