# Generated by Django 3.0.5 on 2021-10-20 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0006_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
