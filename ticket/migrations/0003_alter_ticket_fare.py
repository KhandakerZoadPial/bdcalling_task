# Generated by Django 5.1.2 on 2024-10-16 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_alter_ticket_fare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='fare',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
