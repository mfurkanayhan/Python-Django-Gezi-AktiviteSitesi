# Generated by Django 3.1.7 on 2021-04-02 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
