# Generated by Django 2.2 on 2019-12-08 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portugal', '0003_auto_20191208_1658'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NUTSII',
            new_name='NUTS',
        ),
        migrations.AlterModelOptions(
            name='nuts',
            options={'ordering': ['lft'], 'verbose_name_plural': 'NUTS'},
        ),
        migrations.AlterField(
            model_name='concelho',
            name='nutsiii',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='portugal.NUTS', verbose_name='NUTS'),
        ),
        migrations.DeleteModel(
            name='NUTSIII',
        ),
    ]
