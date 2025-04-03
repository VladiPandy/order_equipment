# Generated by Django 4.2.5 on 2025-04-03 10:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basic_elements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPerAnalyze',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('limit_samples', models.IntegerField(default=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Ограничение по колличеству анализов')),
                ('analazy_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyze_2', to='basic_elements.analyze', verbose_name='Анализ')),
                ('project_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_2', to='basic_elements.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Проект Анализу',
                'verbose_name_plural': 'Проекты Анализам',
            },
        ),
        migrations.CreateModel(
            name='OperatorPerEquipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_priority', models.BooleanField(default=False, verbose_name='Имеет ли оператор приоритет')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='basic_elements.equipment', verbose_name='Прибор')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executor_2', to='basic_elements.executor', verbose_name='Исполнитель')),
            ],
            options={
                'verbose_name': 'Оператор по оборудованию',
                'verbose_name_plural': 'Операторы по оборудованию',
            },
        ),
        migrations.CreateModel(
            name='AnalyzePerEquipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('count_samples', models.IntegerField(default=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Суточный лимит проб')),
                ('analazy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyze_1', to='basic_elements.analyze', verbose_name='Анализ')),
                ('equipment_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment_2', to='basic_elements.equipment', verbose_name='Прибор')),
            ],
            options={
                'verbose_name': 'Анализы по оборудованию',
                'verbose_name_plural': 'Анализы по оборудованию',
            },
        ),
    ]
