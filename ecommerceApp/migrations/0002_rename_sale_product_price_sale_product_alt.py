# Generated by Django 4.2.4 on 2023-08-27 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sale',
            new_name='price_sale',
        ),
        migrations.AddField(
            model_name='product',
            name='alt',
            field=models.CharField(max_length=600, null=True),
        ),
    ]