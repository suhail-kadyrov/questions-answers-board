# Generated by Django 4.1.5 on 2023-01-24 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('semester', models.CharField(max_length=150)),
                ('is_completed', models.BooleanField(default=False)),
                ('started_at', models.DateField()),
                ('token', models.CharField(max_length=150)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professor', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(blank=True, related_name='course', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]