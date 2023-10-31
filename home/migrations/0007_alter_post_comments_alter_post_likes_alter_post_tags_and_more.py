# Generated by Django 4.2.6 on 2023-10-31 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_user_mail_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='skype_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]