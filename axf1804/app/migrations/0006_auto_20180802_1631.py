# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-02 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_cartmode'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoodModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('og_num', models.IntegerField(default=1)),
                ('og_good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MarketGoods')),
            ],
            options={
                'db_table': 'axf_ordergoodmodel',
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_number', models.CharField(max_length=64)),
                ('o_data', models.DateTimeField(auto_now=True)),
                ('o_status', models.IntegerField(default=0)),
                ('o_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserModel')),
            ],
            options={
                'db_table': 'axf_ordermodel',
            },
        ),
        migrations.AddField(
            model_name='ordergoodmodel',
            name='og_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.OrderModel'),
        ),
    ]