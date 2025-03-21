# Generated by Django 5.1.7 on 2025-03-14 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join_up', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.TextField()),
            ],
        ),
    ]
