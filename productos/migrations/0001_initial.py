# Generated by Django 5.2.1 on 2025-07-03 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=50)),
                ('empaque', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
    ]
