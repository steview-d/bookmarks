# Generated by Django 2.2.7 on 2019-11-19 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0009_ticket_admin_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=6),
        ),
    ]
