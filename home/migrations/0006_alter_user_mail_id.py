# Generated by Django 4.2.6 on 2023-10-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_user_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mail_id',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
