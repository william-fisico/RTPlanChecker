# Generated by Django 3.2 on 2021-05-09 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_consistency', '0003_auto_20210509_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rt_techniques',
            name='qa_calc_check',
            field=models.ManyToManyField(blank=True, to='plan_consistency.QACalcCheck'),
        ),
        migrations.AlterField(
            model_name='rt_techniques',
            name='qa_planar_dose',
            field=models.ManyToManyField(blank=True, to='plan_consistency.QAPlanarDose'),
        ),
        migrations.AlterField(
            model_name='rt_techniques',
            name='qa_point_dose',
            field=models.ManyToManyField(blank=True, to='plan_consistency.QAPointDose'),
        ),
        migrations.AlterField(
            model_name='rt_techniques',
            name='treatment_machine',
            field=models.ManyToManyField(blank=True, to='plan_consistency.TreatmentMachine'),
        ),
    ]
