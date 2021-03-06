# Generated by Django 3.2.6 on 2021-08-31 13:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BhaktamberCategories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reason', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Donation_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('donation_amount', models.IntegerField(default=None, validators=[django.core.validators.RegexValidator(message="Donation amount should be 1 or > 1 Rs'.", regex='^[1-9][0-9]*$')])),
                ('total_received_amount', models.FloatField(blank=True, default=0, null=True)),
                ('current_received_amount', models.IntegerField(default=None, validators=[django.core.validators.RegexValidator(message="Donation amount should be 1 or > 1 Rs'.", regex='^[1-9][0-9]*$')])),
                ('total_painding_amount', models.FloatField(blank=True, default=0, null=True)),
                ('donation_date', models.DateField(default=None)),
                ('donation_deposit_date', models.DateField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Bhaktamber_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templ.bhaktambercategories')),
            ],
            options={
                'verbose_name_plural': 'Donation_Details',
            },
        ),
        migrations.CreateModel(
            name='DonationStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDonation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(help_text='Mobile Format: +917028735596', max_length=128, region=None, unique=True)),
                ('address', models.CharField(default='', max_length=100)),
                ('adhar_number', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12,12}$', code='nomatch', message='Enter valid AADHAAR number')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='templ.city')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templ.state')),
            ],
            options={
                'verbose_name_plural': 'Donaties',
            },
        ),
        migrations.CreateModel(
            name='Transaction_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_received_amount', models.IntegerField(default=None, validators=[django.core.validators.RegexValidator(message="Donation amount should be 1 or > 1 Rs'.", regex='^[1-9][0-9]*$')])),
                ('donation_deposit_date', models.DateField(default=None)),
                ('donation_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templ.donation_details')),
            ],
        ),
        migrations.AddField(
            model_name='donation_details',
            name='donation_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templ.donationstatus'),
        ),
        migrations.AddField(
            model_name='donation_details',
            name='donor_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templ.userdonation'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templ.state'),
        ),
    ]
