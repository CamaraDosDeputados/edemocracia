# Generated by Django 2.2.10 on 2021-04-12 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pjb', '0006_auto_20210331_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='partidopjb',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='partido_pjb_foto/'),
        ),
    ]