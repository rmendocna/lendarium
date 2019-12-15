# Generated by Django 2.2 on 2019-04-15 01:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('is_type', models.BooleanField(default=True, verbose_name='Is Type?')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('comments', models.TextField(blank=True, verbose_name='Comments')),
                ('mask', models.CharField(blank=True, max_length=50, verbose_name='Mask')),
                ('modified', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='index_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Motif Index',
                'verbose_name_plural': 'Motif Indexes',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('num', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Num')),
                ('descriptor', models.TextField(blank=True, verbose_name='Description')),
                ('comments', models.TextField(blank=True, verbose_name='Comments')),
                ('index', models.ForeignKey(limit_choices_to={'is_type': True}, on_delete=django.db.models.deletion.PROTECT, to='motif.Index', verbose_name='index')),
                ('modified', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='type_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Type',
            },
        ),
        migrations.CreateModel(
            name='Motif',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('num', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Num')),
                ('descriptor', models.TextField(blank=True, verbose_name='Description')),
                ('comments', models.TextField(blank=True, verbose_name='Comments')),
                ('index', models.ForeignKey(limit_choices_to={'is_type': False}, on_delete=django.db.models.deletion.PROTECT, to='motif.Index', verbose_name='index')),
                ('modified', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='motif_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Motif',
            },
        ),
    ]