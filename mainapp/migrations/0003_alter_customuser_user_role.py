# Generated by Django 3.2.16 on 2022-11-27 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_customuser_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Seller', 'Seller'), ('Transporter', 'Transporter'), ('Customer', 'Customer')], default='General User', max_length=15),
        ),
    ]
