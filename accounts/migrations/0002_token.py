# Generated by Django 4.0.2 on 2022-11-02 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blacklistedtoken', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'token',
            },
        ),
    ]
