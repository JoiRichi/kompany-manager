# Generated by Django 4.0 on 2021-12-29 19:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_rename_is_applicant_customuser_is_student_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_student',
            new_name='is_counter_staff',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='is_teacher',
            new_name='is_director',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_manager',
            field=models.BooleanField(default=False),
        ),
    ]
