# Generated by Django 2.2.3 on 2019-08-11 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='photo',
            field=models.ImageField(null=True, upload_to='<django.db.models.fields.AutoField>.jpg'),
        ),
    ]
