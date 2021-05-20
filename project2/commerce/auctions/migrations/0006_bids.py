# Generated by Django 3.2 on 2021-04-22 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_delete_alllisting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('bid', models.IntegerField()),
                ('listingId', models.IntegerField()),
            ],
        ),
    ]
