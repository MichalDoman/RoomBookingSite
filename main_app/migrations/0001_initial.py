# Generated by Django 4.1.7 on 2023-02-22 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('capacity', models.IntegerField()),
                ('has_projector', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.room')),
            ],
            options={
                'unique_together': {('date', 'room_id')},
            },
        ),
    ]
