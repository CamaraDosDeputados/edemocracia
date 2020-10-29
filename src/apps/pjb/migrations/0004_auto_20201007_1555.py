# Generated by Django 2.2.10 on 2020-10-07 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pjb', '0003_auto_20201006_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='projetopjb',
            name='ano',
            field=models.IntegerField(default=2020),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projetopjb',
            name='sigla_tipo',
            field=models.CharField(default='PL', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projetopjb',
            name='numero',
            field=models.CharField(max_length=4),
        ),
    ]