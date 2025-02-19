# Generated by Django 4.2.5 on 2025-02-19 12:26

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
            name='IsOpenRegistration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_open', models.BooleanField(default=False, verbose_name='Открыть регистрацию')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Статус открытой регистрации',
                'verbose_name_plural': 'Статусы открытой регистрации',
            },
        ),
        migrations.CreateModel(
            name='OpenWindowForOrdering',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.CharField(choices=[('19.02.2025', '19.02.2025'), ('20.02.2025', '20.02.2025'), ('21.02.2025', '21.02.2025'), ('22.02.2025', '22.02.2025'), ('23.02.2025', '23.02.2025'), ('24.02.2025', '24.02.2025'), ('25.02.2025', '25.02.2025'), ('26.02.2025', '26.02.2025'), ('27.02.2025', '27.02.2025'), ('28.02.2025', '28.02.2025'), ('01.03.2025', '01.03.2025'), ('02.03.2025', '02.03.2025'), ('03.03.2025', '03.03.2025'), ('04.03.2025', '04.03.2025'), ('05.03.2025', '05.03.2025'), ('06.03.2025', '06.03.2025'), ('07.03.2025', '07.03.2025'), ('08.03.2025', '08.03.2025'), ('09.03.2025', '09.03.2025'), ('10.03.2025', '10.03.2025'), ('11.03.2025', '11.03.2025')], max_length=200, verbose_name='Дата открытия записи')),
                ('start_time', models.CharField(choices=[('00:00', '00:00'), ('01:00', '01:00'), ('02:00', '02:00'), ('03:00', '03:00'), ('04:00', '04:00'), ('05:00', '05:00'), ('06:00', '06:00'), ('07:00', '07:00'), ('08:00', '08:00'), ('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00'), ('22:00', '22:00'), ('23:00', '23:00'), ('24:00', '24:00')], max_length=50, verbose_name='Время открытия бонирования')),
                ('end_time', models.CharField(choices=[('00:00', '00:00'), ('01:00', '01:00'), ('02:00', '02:00'), ('03:00', '03:00'), ('04:00', '04:00'), ('05:00', '05:00'), ('06:00', '06:00'), ('07:00', '07:00'), ('08:00', '08:00'), ('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00'), ('22:00', '22:00'), ('23:00', '23:00'), ('24:00', '24:00')], max_length=50, verbose_name='Время закрытия бронирования')),
                ('for_priority', models.BooleanField(default=False, verbose_name='Для приоритетных')),
            ],
            options={
                'verbose_name': 'Окно для заказа',
                'verbose_name_plural': 'Окна для заказа',
            },
        ),
        migrations.CreateModel(
            name='WorkingDayOfWeek',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('monday', models.BooleanField(default=False, verbose_name='Понедельник')),
                ('tuesday', models.BooleanField(default=False, verbose_name='Вторник')),
                ('wednesday', models.BooleanField(default=False, verbose_name='Среда')),
                ('thursday', models.BooleanField(default=False, verbose_name='Четверг')),
                ('friday', models.BooleanField(default=False, verbose_name='Пятница')),
                ('saturday', models.BooleanField(default=False, verbose_name='Суббота')),
                ('sunday', models.BooleanField(default=False, verbose_name='Воскресенье')),
            ],
            options={
                'verbose_name': 'Рабочий день недели',
                'verbose_name_plural': 'Рабочие дни недели',
            },
        ),
        migrations.CreateModel(
            name='WorkerWeekStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('monday', models.CharField(choices=[('Работает', 'Работает'), ('Выходной', 'Выходной'), ('Отпуск', 'Отпуск'), ('Болеет', 'Болеет')], default='Работает', verbose_name='Понедельник')),
                ('tuesday', models.CharField(choices=[('Работает', 'Работает'), ('Выходной', 'Выходной'), ('Отпуск', 'Отпуск'), ('Болеет', 'Болеет')], default='Работает', verbose_name='Вторник')),
                ('wednesday', models.CharField(choices=[('Работает', 'Работает'), ('Выходной', 'Выходной'), ('Отпуск', 'Отпуск'), ('Болеет', 'Болеет')], default='Работает', verbose_name='Среда')),
                ('thursday', models.CharField(choices=[('Работает', 'Работает'), ('Выходной', 'Выходной'), ('Отпуск', 'Отпуск'), ('Болеет', 'Болеет')], default='Работает', verbose_name='Четверг')),
                ('friday', models.CharField(choices=[('Работает', 'Работает'), ('Выходной', 'Выходной'), ('Отпуск', 'Отпуск'), ('Болеет', 'Болеет')], default='Выходной', verbose_name='Пятница')),
                ('saturday', models.CharField(choices=[('Работает', 'Работает'), ('Выходной', 'Выходной'), ('Отпуск', 'Отпуск'), ('Болеет', 'Болеет')], default='Выходной', verbose_name='Суббота')),
                ('sunday', models.CharField(choices=[('Работает', 'Работает'), ('Выходной', 'Выходной'), ('Отпуск', 'Отпуск'), ('Болеет', 'Болеет')], default='Выходной', verbose_name='Воскресенье')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executor', to='basic_elements.executor', verbose_name='Исполнитель')),
            ],
            options={
                'verbose_name': 'Рабочий график сотрудника',
                'verbose_name_plural': 'Рабочие графики сотрудников',
            },
        ),
    ]
