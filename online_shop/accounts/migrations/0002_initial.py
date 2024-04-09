# Generated by Django 4.2.11 on 2024-04-08 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shop', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='order_history',
            field=models.ManyToManyField(blank=True, related_name='custom_user_orders', to='shop.order'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shopping_cart',
            field=models.ManyToManyField(blank=True, related_name='custom_user_cart', to='shop.book'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='custom_user_wishlist', to='shop.book'),
        ),
    ]
