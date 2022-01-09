# Generated by Django 4.0 on 2022-01-08 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration_website', '0014_alter_subjectassignment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='examination_assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='student_examinations', to='registration_website.examinationvenueassignment'),
        ),
    ]
