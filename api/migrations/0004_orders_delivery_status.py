# Generated by Django 5.1 on 2024-09-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_shipping_details_delivery_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivery_status',
            field=models.BooleanField(default=False),
        ),
    ]
