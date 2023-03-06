# Generated by Django 4.0.2 on 2023-03-06 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0024_alter_qprsupremecourt_working_strength_of_jjb_staff_in_the_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='centralsponsorship',
            name='state_children_availing_sponsership_cumulative',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='centralsponsorship',
            name='state_children_availing_sponsership_quarterly',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='centralsponsorship',
            name='state_children_scolership_added',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='centralsponsorship',
            name='state_children_scolership_exempted',
            field=models.IntegerField(default=0),
        ),
    ]
