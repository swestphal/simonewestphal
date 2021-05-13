# Generated by Django 3.2 on 2021-05-13 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_tags'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='blogarticle',
        ),
        migrations.AddField(
            model_name='tag',
            name='post',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tags_of_posts', to='blog.post'),
            preserve_default=False,
        ),
    ]
