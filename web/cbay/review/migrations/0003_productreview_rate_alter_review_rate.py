# Generated by Django 4.2 on 2023-05-15 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_rename_rating_review_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='rate',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.FloatField(default=1),
        ),
    ]
