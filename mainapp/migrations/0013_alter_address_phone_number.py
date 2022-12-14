# Generated by Django 3.2.16 on 2022-12-15 08:52

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_alter_address_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default=None, max_length=128, region=None),
            preserve_default=False,
        ),
    ]
