# Generated by Django 3.1.6 on 2021-03-02 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('level', models.IntegerField(default=1)),
                ('xp_total', models.IntegerField(default=0)),
                ('xp_to_lvlup', models.IntegerField(default=1515)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=140)),
                ('xp', models.IntegerField(default=1)),
                ('completed', models.BooleanField(default=False)),
                ('dueDate', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='todos', to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=140)),
                ('multiplier', models.IntegerField(default=1)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='habits', to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=140)),
                ('xp', models.IntegerField(default=1)),
                ('completed', models.BooleanField(default=False)),
                ('timePeriod', models.CharField(blank=True, max_length=40)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCompleted', models.DateTimeField(blank=True, null=True)),
                ('habit', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='api.habit')),
            ],
        ),
    ]
