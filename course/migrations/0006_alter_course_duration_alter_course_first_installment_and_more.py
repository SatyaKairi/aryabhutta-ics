# Generated by Django 4.1 on 2022-08-20 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='first_installment',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='second_installment',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='third_installment',
            field=models.IntegerField(),
        ),
    ]
