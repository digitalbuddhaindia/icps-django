# Generated by Django 4.0.2 on 2022-08-26 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_remove_qprhighcourt_age_group_15_18_childern_in_rci_16_a_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qprhighcourt',
            old_name='spu_posco_vac_in_key_st_and_al_bo_sanctioned_positions_12',
            new_name='spu_pocso_vac_in_key_st_and_al_bo_sanctioned_positions_12',
        ),
        migrations.RenameField(
            model_name='qprhighcourt',
            old_name='spu_posco_vac_in_key_statutory_and_al_bo_filled_positions_12',
            new_name='spu_pocso_vac_in_key_statutory_and_al_bo_filled_positions_12',
        ),
        migrations.RenameField(
            model_name='qprhighcourt',
            old_name='spu_posco_vac_in_key_statutory_and_al_bo_vacant_positions_12',
            new_name='spu_pocso_vac_in_key_statutory_and_al_bo_vacant_positions_12',
        ),
    ]
