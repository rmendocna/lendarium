# Generated by Django 2.2 on 2019-05-12 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motif', '0004_auto_20190512_1324'),
        ('legends', '0009_auto_20190511_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='narrative',
            name='motifs',
            field=models.ManyToManyField(to='motif.Motif'),
        ),
        migrations.AlterField(
            model_name='narrative',
            name='many_names',
            field=models.ManyToManyField(help_text='Names occurring or referred to in the Text', to='legends.Name'),
        ),
    ]
