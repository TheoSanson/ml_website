# Generated by Django 4.0 on 2022-01-05 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration_website', '0009_examinationvenueassignment_current_examinees_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examination',
            options={'ordering': ['exam_date']},
        ),
        migrations.AlterField(
            model_name='examinationvenueassignment',
            name='examination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examinations', to='registration_website.examination'),
        ),
    ]
