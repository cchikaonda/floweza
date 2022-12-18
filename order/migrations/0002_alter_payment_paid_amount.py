# Generated by Django 3.2.16 on 2022-12-13 09:36

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='MWK', max_digits=14),
        ),
    ]
