# Generated by Django 4.0.3 on 2022-04-10 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_generic_features', '0005_balance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nft',
            old_name='currency_type',
            new_name='blockchain',
        ),
    ]