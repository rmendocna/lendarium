# Generated by Django 2.2 on 2019-12-08 16:49

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('portugal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nutsii',
            options={'verbose_name': 'NUTS', 'verbose_name_plural': 'NUTS'},
        ),
        migrations.RenameField(
            model_name='freguesia',
            old_name='area2008_1',
            new_name='area',
        ),
        migrations.AddField(
            model_name='nutsii',
            name='code',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='nutsii',
            name='level',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nutsii',
            name='lft',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nutsii',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='portugal.NUTSII'),
        ),
        migrations.AddField(
            model_name='nutsii',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nutsii',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
    ]
