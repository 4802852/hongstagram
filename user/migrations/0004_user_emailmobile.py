# Generated by Django 3.2.2 on 2021-05-11 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210511_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emailmobile',
            field=models.CharField(default='0123456789', max_length=100),
            preserve_default=False,
        ),
    ]
