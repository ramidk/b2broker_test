# Generated by Django 5.0.4 on 2024-04-26 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=18, default=0, max_digits=32)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txid', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=18, max_digits=32)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.wallet')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]