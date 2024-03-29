# Generated by Django 3.2.2 on 2021-05-20 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=512, primary_key=True, serialize=False)),
                ('summary', models.CharField(max_length=2048)),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productManual', to='catalogue.manual')),
                ('gallery', models.ManyToManyField(blank=True, related_name='gallery', to='catalogue.Image')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productImage', to='catalogue.image')),
                ('specSheet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specSheet', to='catalogue.image')),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSeries',
            fields=[
                ('name', models.CharField(max_length=512, primary_key=True, serialize=False)),
                ('summary', models.CharField(max_length=2048)),
                ('description', models.CharField(max_length=9192)),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banner', to='catalogue.image')),
                ('category', models.ManyToManyField(to='catalogue.Category')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seriesImage', to='catalogue.image')),
                ('infoImage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seriesInfoImage', to='catalogue.image')),
                ('products', models.ManyToManyField(blank=True, related_name='products', to='catalogue.Product')),
                ('type', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='type', to='catalogue.producttype')),
            ],
        ),
    ]
