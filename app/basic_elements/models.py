import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import Any

class UUIDMixin(models.Model):
    """UUID"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class TimeStampedMixin(models.Model):
    """Модель. Атрибуты создания и редактирования"""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Модель Прибора
class Equipment(UUIDMixin,TimeStampedMixin):
    name = models.CharField(max_length=255, verbose_name='Название прибора')

    STATUS_CHOICES = [
        ('active', 'Активное'),
        ('inactive', 'Неактивное'),
        ('maintenance', 'Техническое обслуживание'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Статус работы')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "public\".\"equipment"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Прибор'
        verbose_name_plural = 'Приборы'

    def __str__(self):
        return f"{self.name}"


# Модель Анализа
class AnalyzeType(UUIDMixin, TimeStampedMixin):
    type = models.CharField(max_length=255, verbose_name='Тип анализа')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "public\".\"analyze_type"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Тип анализа'
        verbose_name_plural = 'Типы анализа'

    def __str__(self):
        return f"{self.type}"


# Модель Анализа
class Analyze(UUIDMixin, TimeStampedMixin):
    analyze_name = models.CharField(max_length=255, verbose_name='Название анализа')
    analyze_type = models.ForeignKey(AnalyzeType, on_delete=models.CASCADE, verbose_name='Тип анализа', related_name='analyze_type')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "public\".\"analyze"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Анализ'
        verbose_name_plural = 'Анализы'

    def __str__(self):
        return f"{self.analyze_name}  типа  {self.analyze_type}"

# Модель Исполнителя
class Executor(UUIDMixin, TimeStampedMixin):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "public\".\"executor"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return f"{self.first_name}  {self.last_name}  {self.patronymic}"

# Модель Проекта
class Project(UUIDMixin, TimeStampedMixin):
    project_name = models.CharField(max_length=255, verbose_name='Проект')
    is_priority = models.BooleanField(verbose_name='Имеет приоритет')
    responsible_person = models.CharField(max_length=255,
                                          verbose_name='Ответственный за проект')
    project_password = models.CharField(max_length=128,
                                        verbose_name='Пароль для входа')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "public\".\"project"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return f"{self.project_name}  {self.is_priority}  {self.responsible_person}"


@receiver(post_save, sender=Project)
def create_user_for_project(sender: type, instance: Project, created: bool,
                            **kwargs: Any) -> None:
    """
    Сигнал, который срабатывает после сохранения экземпляра Project.

    Входные параметры:
    - sender: класс модели (Project)
    - instance: объект Project, который был сохранен
    - created: флаг, указывающий, что объект был создан (True), а не обновлен (False)
    - kwargs: дополнительные аргументы

    Логика:
    Если проект был только что создан, создаем пользователя:
    - Имя пользователя берём из поля responsible_person (приводим к нижнему регистру и заменяем пробелы).
    - Пароль берем из поля project_password.
    - Если is_priority=True, то пользователь будет администратором.
    """
    if created:
        # Формируем имя пользователя на основе responsible_person
        username = instance.project_name

        # Создаем пользователя с указанным паролем
        new_user = User.objects.create_user(username=username,
                                            password=instance.project_password)

        # Если проект приоритетный - делаем пользователя администратором
        if instance.is_priority:
            new_user.is_staff = True
            new_user.is_superuser = True
            new_user.save()