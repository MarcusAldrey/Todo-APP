# Generated by Django 3.0.6 on 2021-05-06 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('conclusion_date', models.DateField()),
                ('is_done', models.BooleanField()),
            ],
        ),
    ]
