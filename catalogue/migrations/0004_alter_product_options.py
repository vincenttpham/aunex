# Generated by Django 3.2.3 on 2021-06-28 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_alter_image_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['pk']},
        ),
    ]
