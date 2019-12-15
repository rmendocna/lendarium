# Generated by Django 2.2 on 2019-05-10 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legends', '0005_auto_20190507_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='narrative',
            name='many_names',
            field=models.ManyToManyField(help_text='Names occourring or referred to on the Text', to='legends.Name'),
        ),
        migrations.AlterField(
            model_name='narrativeversion',
            name='narrative',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='narrativeversion_related', to='legends.Narrative', verbose_name='Record'),
        ),
    ]
