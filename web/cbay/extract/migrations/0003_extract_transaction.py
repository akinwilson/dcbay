# Generated by Django 4.2 on 2023-05-13 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extract', '0002_extract_delete_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='extract',
            name='transaction',
            field=models.TextField(default=''),
        ),
    ]
