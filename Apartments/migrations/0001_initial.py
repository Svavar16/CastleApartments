# Generated by Django 2.2.1 on 2019-05-07 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streetName', models.CharField(max_length=255)),
                ('houseNumber', models.IntegerField(max_length=10)),
                ('city', models.CharField(max_length=255)),
                ('postalCode', models.IntegerField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Apartments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(max_length=20)),
                ('size', models.FloatField(max_length=5)),
                ('rooms', models.IntegerField(max_length=3)),
                ('privateEntrance', models.BooleanField()),
                ('animalsAllowed', models.BooleanField()),
                ('garage', models.BooleanField()),
                ('yearBuild', models.IntegerField()),
                ('locationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Apartments.Location')),
                ('sellerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candyImage', models.CharField(max_length=999)),
                ('apartmentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Apartments.Apartments')),
            ],
        ),
    ]
