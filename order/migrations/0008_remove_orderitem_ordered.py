# Generated by Django 3.2.16 on 2022-12-15 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_remove_orderitem_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ordered',
        ),
    ]