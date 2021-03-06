# Generated by Django 3.1.1 on 2020-09-22 02:09

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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('color', models.CharField(max_length=7, verbose_name='Hex color')),
                ('icon', models.CharField(max_length=30, verbose_name='Material Design Icon code')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='task_app.category')),
            ],
        ),
    ]
