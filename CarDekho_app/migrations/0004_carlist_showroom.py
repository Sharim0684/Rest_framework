# Generated by Django 5.2.1 on 2025-05-21 05:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarDekho_app', '0003_showroomlist_alter_carlist_chassinumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='carlist',
            name='showroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='showrooms', to='CarDekho_app.showroomlist'),
        ),
    ]
