# Generated by Django 4.1.3 on 2022-11-30 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0005_alter_ad_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location", name="lat", field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="location", name="lng", field=models.FloatField(null=True),
        ),
    ]