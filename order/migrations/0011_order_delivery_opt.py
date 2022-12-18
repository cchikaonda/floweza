# Generated by Django 3.2.16 on 2022-12-17 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_remove_deliveryoptions_order'),
        ('order', '0010_payment_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_opt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.deliveryoptions'),
        ),
    ]
