# Generated by Django 3.2.16 on 2022-12-10 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20221210_0520'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='ecom_product6_b.png', null=True, upload_to='items/'),
        ),
        migrations.DeleteModel(
            name='ItemImage',
        ),
    ]
