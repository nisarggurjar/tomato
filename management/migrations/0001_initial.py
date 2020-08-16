# Generated by Django 3.0.7 on 2020-07-31 11:27

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('dis', models.TextField(blank=True, null=True)),
                ('img', models.FileField(blank=True, null=True, upload_to='')),
                ('img1', models.FileField(blank=True, null=True, upload_to='')),
                ('img2', models.FileField(blank=True, null=True, upload_to='')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('mrp', models.IntegerField(blank=True, null=True)),
                ('avail', models.BooleanField(blank=True, default=True, null=True)),
                ('cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Category')),
            ],
        ),
    ]
