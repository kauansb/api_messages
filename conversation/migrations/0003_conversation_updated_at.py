# Generated by Django 5.1.6 on 2025-03-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0002_remove_conversation_updated_at_alter_conversation_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
