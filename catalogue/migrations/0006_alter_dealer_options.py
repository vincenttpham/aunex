# Generated by Django 3.2.3 on 2021-07-04 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_dealer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dealer',
            options={'ordering': ['pk']},
        ),
    ]