# Generated by Django 3.2.16 on 2022-12-15 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_remove_payment_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order_type',
        ),
    ]
