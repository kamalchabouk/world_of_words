# Generated by Django 5.0.3 on 2024-03-27 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_order_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='author',
        ),
    ]
