# Generated by Django 3.2.16 on 2022-11-27 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_customuser_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Seller', 'Seller'), ('Transporter', 'Transporter'), ('Customer', 'Customer')], default='Customer', max_length=15),
        ),
    ]
