# Generated by Django 4.2.15 on 2024-08-29 04:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_alter_post_created_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255)),
                ('url', models.URLField(blank=True)),
                ('text', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]
