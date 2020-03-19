# Generated by Django 2.2.7 on 2020-03-19 11:46

from django.db import migrations, models
import links.models
import links.validators


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0034_bookmark_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=links.models.icon_location, validators=[links.validators.validate_icon_file_extension, links.validators.validate_icon_file_size]),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
