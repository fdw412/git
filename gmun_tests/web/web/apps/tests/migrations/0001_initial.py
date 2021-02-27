# Generated by Django 3.0.6 on 2020-05-12 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autotest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=200, verbose_name='название теста')),
                ('test_text', models.TextField(verbose_name='исторические данные теста')),
            ],
        ),
    ]
