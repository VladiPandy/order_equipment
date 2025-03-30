from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from datetime import datetime, timedelta
from basic_elements.models import *


def get_week_period_choices():
    """
    Функция возвращает список кортежей с выбором периода недели с понедельника по воскресенье
    на 12 недель вперед. Каждый кортеж имеет вид (значение, отображаемое значение).

    :return: Список кортежей с периодами недели в формате 'dd.mm.yyyy-dd.mm.yyyy'
    """
    today = datetime.today()
    # Определяем понедельник текущей недели.
    current_monday = today - timedelta(days=today.weekday())
    choices = [
        (
            (current_monday + timedelta(days=i * 7)).strftime('%d.%m.%Y') + '-' +
            (current_monday + timedelta(days=i * 7 + 6)).strftime('%d.%m.%Y'),
            (current_monday + timedelta(days=i * 7)).strftime('%d.%m.%Y') + '-' +
            (current_monday + timedelta(days=i * 7 + 6)).strftime('%d.%m.%Y')
        )
        for i in range(12)
    ]
    return choices


class WorkingDayOfWeek(UUIDMixin,TimeStampedMixin):
    """
    Модель для представления рабочих дней недели
    """
    monday = models.BooleanField(default=False, verbose_name='Понедельник')
    tuesday = models.BooleanField(default=False, verbose_name='Вторник')
    wednesday = models.BooleanField(default=False, verbose_name='Среда')
    thursday = models.BooleanField(default=False, verbose_name='Четверг')
    friday = models.BooleanField(default=False, verbose_name='Пятница')
    saturday = models.BooleanField(default=False, verbose_name='Суббота')
    sunday = models.BooleanField(default=False, verbose_name='Воскресенье')

    class Meta:
        verbose_name = 'Рабочий день недели'
        verbose_name_plural = 'Рабочие дни недели'

    def clean(self):
        if WorkingDayOfWeek.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Можно создать только одну запись рабочего дня недели. Пожалуйста, отредактируйте существующую запись.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return self.formatted_working_days()

    def formatted_working_days(self):
        days = [
            ('Пн   ', self.monday),
            ('Вт   ', self.tuesday),
            ('Ср   ', self.wednesday),
            ('Чт   ', self.thursday),
            ('Пт   ', self.friday),
            ('Сб    ', self.saturday),
            ('Вс    ', self.sunday),
        ]

        return format_html(
            '<span style="font-size: 32px;line-height: 3;">{}</span>'.format(
                '   '.join(
                    [f"<span style='color: green;'>{day}</span>" if is_working else f"<span style='color: gray;'>{day}</span>" for day, is_working in days]
                )
            )
        )

    formatted_working_days.short_description = 'Рабочие дни'


class OpenWindowForOrdering(UUIDMixin, TimeStampedMixin):
    """
    Модель для представления окна открытого заказа
    """
    START_DATE_CHOICES = [
        ((datetime.today() + timedelta(days=i)).strftime('%d.%m.%Y'),
         (datetime.today() + timedelta(days=i)).strftime('%d.%m.%Y'))
        for i in range(0, 21)
    ]
    start_date = models.CharField(max_length=200, choices=START_DATE_CHOICES, verbose_name='Дата открытия записи')
    TIME_CHOICES = [
        (f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(0, 25)
    ]
    start_time = models.CharField(max_length=50, choices=TIME_CHOICES,
                                verbose_name='Время открытия бонирования')
    end_time = models.CharField(max_length=50, choices=TIME_CHOICES, verbose_name='Время закрытия бронирования')
    for_priority = models.BooleanField(default=False, verbose_name='Для приоритетных')

    week_period = models.CharField(
        max_length=50,
        choices=get_week_period_choices(),
        verbose_name='Период недели (с понедельника по воскресенье)'
    )

    class Meta:
        verbose_name = 'Окно для заказа'
        verbose_name_plural = 'Окна для заказа'

    def __str__(self):
        return (
            f"Окно бронирования на {self.start_date} с {self.start_time} до {self.end_time}, "
            f"период недели: {self.week_period}")


class IsOpenRegistration(UUIDMixin, TimeStampedMixin):
    """
    Модель для представления статуса открытой регистрации
    """
    is_open = models.BooleanField(default=False, verbose_name='Открыть регистрацию')

    week_period = models.CharField(
        max_length=50,
        choices=get_week_period_choices(),
        verbose_name='Период недели (с понедельника по воскресенье)'
    )

    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если is_open установлен в True, то в базе не должно быть другой записи с is_open = True.

        :raises ValidationError: Если уже существует другая открытая регистрация.
        """
        if self.is_open:
            # Исключаем текущую запись, если она уже существует (например, при обновлении)
            if IsOpenRegistration.objects.filter(is_open=True).exclude(
                    pk=self.pk).exists():
                raise ValidationError(
                    "Открытая регистрация уже существует. Должна быть только одна открытая регистрация."
                )

    def save(self, *args: any, **kwargs: any) -> None:
        """
        Переопределение метода save для вызова проверки clean перед сохранением.
        Это гарантирует, что правило о единственности открытой регистрации соблюдается.
        """
        self.full_clean()  # вызывает clean() и проводит валидацию модели
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статус открытой регистрации'
        verbose_name_plural = 'Статусы открытой регистрации'

    def __str__(self):
        return ("Открыта" if self.is_open else "Закрыта") + f" период недели: {self.week_period}"


class WorkerWeekStatus(UUIDMixin,TimeStampedMixin):
    """
    Модель для представления рабочих дней недели
    """
    STATUS_WORKING = [
        ('Работает', 'Работает'),
        ('Выходной', 'Выходной'),
        ('Отпуск', 'Отпуск'),
        ('Болеет', 'Болеет'),
    ]

    executor = models.ForeignKey(Executor, on_delete=models.CASCADE, verbose_name='Исполнитель', related_name='executor')
    monday = models.CharField(default='Работает', verbose_name='Понедельник', choices=STATUS_WORKING)
    tuesday = models.CharField(default='Работает', verbose_name='Вторник', choices=STATUS_WORKING)
    wednesday = models.CharField(default='Работает', verbose_name='Среда', choices=STATUS_WORKING)
    thursday = models.CharField(default='Работает', verbose_name='Четверг', choices=STATUS_WORKING)
    friday = models.CharField(default='Выходной', verbose_name='Пятница', choices=STATUS_WORKING)
    saturday = models.CharField(default='Выходной', verbose_name='Суббота', choices=STATUS_WORKING)
    sunday = models.CharField(default='Выходной', verbose_name='Воскресенье', choices=STATUS_WORKING)

    class Meta:
        verbose_name = 'Рабочий график сотрудника'
        verbose_name_plural = 'Рабочие графики сотрудников'

    def __str__(self):
        return format_html(f"{self.executor} | {self.monday} | {self.tuesday} | {self.wednesday} | {self.thursday} | {self.friday} | {self.sunday} | {self.saturday} ")