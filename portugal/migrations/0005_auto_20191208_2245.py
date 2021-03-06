# Generated by Django 2.2 on 2019-12-08 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portugal', '0004_auto_20191208_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='freguesia',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='freguesia',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='freguesia',
            name='rght',
            field=models.PositiveIntegerField(default=2, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='freguesia',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
    ]
