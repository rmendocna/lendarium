# Generated by Django 2.2 on 2019-12-08 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portugal', '0005_auto_20191208_2245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='concelho',
            options={'ordering': ['name'], 'verbose_name': 'County', 'verbose_name_plural': 'Counties'},
        ),
        migrations.AlterModelOptions(
            name='freguesia',
            options={'ordering': ['name'], 'verbose_name': 'County/Parish', 'verbose_name_plural': 'Counties and Parishes'},
        ),
        migrations.RenameField(
            model_name='concelho',
            old_name='nome',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='distrito',
            old_name='nome',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='freguesia',
            old_name='freguesia',
            new_name='name',
        ),
    ]