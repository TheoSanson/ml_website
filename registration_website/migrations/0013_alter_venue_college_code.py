# Generated by Django 4.0 on 2022-01-06 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration_website', '0012_alter_examinationvenueassignment_examination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='college_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='registration_website.college'),
        ),
    ]