# Generated by Django 5.1.2 on 2024-10-16 18:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('train', '0003_remove_train_stops_trainstop'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fare', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchased_at', models.DateTimeField(auto_now_add=True)),
                ('stops', models.ManyToManyField(to='train.trainstop')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train.train')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
