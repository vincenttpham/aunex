# Generated by Django 3.2.3 on 2021-07-11 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20210711_0004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='position',
            new_name='inventory_position',
        ),
        migrations.AddField(
            model_name='product',
            name='page_position',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
