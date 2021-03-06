# Generated by Django 4.0.3 on 2022-04-19 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_generic_features', '0008_alter_balance_balance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collected',
            options={'verbose_name_plural': "Profile's collection"},
        ),
        migrations.AlterModelOptions(
            name='nft',
            options={'verbose_name': 'NFT'},
        ),
        migrations.AddField(
            model_name='collected',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nft',
            name='likes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
