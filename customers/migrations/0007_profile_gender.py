# Generated by Django 5.1.5 on 2025-02-16 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_payment_sum_of_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10),
        ),
    ]
