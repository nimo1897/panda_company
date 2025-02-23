# Generated by Django 5.1.5 on 2025-02-12 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0002_company_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='funds_out',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
