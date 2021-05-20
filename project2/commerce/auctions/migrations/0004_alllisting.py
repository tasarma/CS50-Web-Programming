# Generated by Django 3.2 on 2021-04-20 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listingId', models.IntegerField()),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(max_length=256)),
                ('link', models.CharField(blank=True, default=None, max_length=265, null=True)),
            ],
        ),
    ]
