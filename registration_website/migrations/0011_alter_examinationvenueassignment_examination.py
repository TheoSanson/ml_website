# Generated by Django 4.0 on 2022-01-05 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration_website', '0010_alter_examination_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationvenueassignment',
            name='examination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examination', to='registration_website.examination'),
        ),
    ]