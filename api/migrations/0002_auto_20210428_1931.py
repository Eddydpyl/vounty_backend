# Generated by Django 3.2 on 2021-04-28 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='vote_count',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='granted',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='entry',
            name='vote_count',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='fund',
            name='charge',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='like',
            field=models.BooleanField(db_index=True),
        ),
        migrations.AlterField(
            model_name='vounty',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='vounty',
            name='featured',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='vounty',
            name='fund_count',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='vounty',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='vounty',
            name='prize',
            field=models.FloatField(db_index=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='vounty',
            name='subtitle',
            field=models.CharField(db_index=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='vounty',
            name='title',
            field=models.CharField(db_index=True, default='', max_length=100),
        ),
    ]
