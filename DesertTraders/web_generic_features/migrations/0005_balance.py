# Generated by Django 4.0.3 on 2022-04-08 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_generic_features', '0004_rename_collection_profile_my_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('balance', models.FloatField(default=10)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='web_generic_features.profile')),
            ],
        ),
    ]
