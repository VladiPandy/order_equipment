import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import re

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

    count_samples = models.IntegerField(default=False,
                                        verbose_name='Суточный лимит прибора',
                                        validators=[MinValueValidator(0),
                                                    MaxValueValidator(100)])
    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "public\".\"equipment"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Прибор'
        verbose_name_plural = 'Приборы'

    def __str__(self):
        return f"{self.name}"

    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если is_open установлен в True, то в базе не должно быть другой записи с is_open = True.

        :raises ValidationError: Если уже существует другая открытая регистрация.
        """

        if self.name:
            # Исключаем текущую запись, если она уже существует (например, при обновлении)
            if Equipment.objects.exclude(pk=self.pk).filter(
                    name=self.name).exists():
                raise ValidationError(
                    f"Прибор с именем '{self.name}' уже существует.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)


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

    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если is_open установлен в True, то в базе не должно быть другой записи с is_open = True.

        :raises ValidationError: Если уже существует другая открытая регистрация.
        """

        if self.type:
            # Исключаем текущую запись, если она уже существует (например, при обновлении)
            if AnalyzeType.objects.exclude(pk=self.pk).filter(
                    type=self.type).exists():
                raise ValidationError(
                    f"Тип анализа с именем '{self.type}' уже существует.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)



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
        return f"{self.analyze_name} : {self.analyze_type}"


    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если is_open установлен в True, то в базе не должно быть другой записи с is_open = True.

        :raises ValidationError: Если уже существует другая открытая регистрация.
        """

        if self.analyze_name:
            # Исключаем текущую запись, если она уже существует (например, при обновлении)
            if Analyze.objects.exclude(pk=self.pk).filter(
                    analyze_name=self.analyze_name).exists():
                raise ValidationError(
                    f"Анализ с именем '{self.analyze_name}' уже существует.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)

# Модель Исполнителя
class Executor(UUIDMixin, TimeStampedMixin):
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество', blank=True, null=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "public\".\"executor"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return f"{self.last_name}  {self.first_name}  {self.patronymic}"


    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если is_open установлен в True, то в базе не должно быть другой записи с is_open = True.

        :raises ValidationError: Если уже существует другая открытая регистрация.
        """

        if self.first_name:
            # Исключаем текущую запись, если она уже существует (например, при обновлении)
            if Executor.objects.exclude(pk=self.pk).filter(
                    first_name=self.first_name, last_name=self.last_name,
                    patronymic=self.patronymic).exists():
                raise ValidationError(
                    f"Исполнитель с ФИО '{self.last_name} {self.first_name} {self.patronymic}' уже существует.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)


# Модель Администратора
class Adminstrator(UUIDMixin, TimeStampedMixin):
    admin_nick = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Логин для авторизации'
    )
    admin_person = models.CharField(
        max_length=255,
        verbose_name='Данные ответственного'
    )
    admin_password = models.CharField(
        max_length=128,
        verbose_name='Пароль для входа'
    )

    class Meta:
        db_table = 'public"."adminstrator'
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self):
        return f"Администратор {self.admin_person}"

    def clean(self):
        """
        Дополнительная валидация имени проекта.
        """
        if not self.admin_nick.isalnum():
            raise ValidationError("Никнейм проекта должен содержать буквенно-цифровые символы.")

            # Проверка project_password: минимальная длина 8 символов
        if len(self.admin_password) < 8:
            raise ValidationError(
                "Пароль для входа должен содержать не менее 8 символов.")

        # Дополнительные проверки пароля можно добавить, например:
        # Проверка на наличие хотя бы одной буквы и одной цифры:
        if not re.search(r"[A-Za-z]",
                         self.admin_password) or not re.search(r"\d",
                                                                 self.admin_password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну букву и одну цифру.")

        super().clean()


@receiver(pre_save, sender=Adminstrator)
def update_adminstrator_username(sender, instance, **kwargs):
    """
    При обновлении проекта проверяет, изменилось ли имя проекта.
    Если да, пытается найти пользователя с предыдущим именем и обновляет его username.
    """
    if instance.pk:
        try:
            old_instance = Adminstrator.objects.get(pk=instance.pk)
        except Adminstrator.DoesNotExist:
            return

            # Получаем пользователя по старому имени
        try:
            user = User.objects.get(username=old_instance.admin_nick)
        except User.DoesNotExist:
            # Если пользователь не найден, ничего не делаем
            return

            # Проверка изменения имени администратора (admin_nick)
        if old_instance.admin_nick != instance.admin_nick:
            # Проверяем, существует ли уже пользователь с новым именем
            if User.objects.filter(username=instance.admin_nick).exists():
                raise ValidationError(
                    f"Имя администратора {instance.admin_nick} уже занято.")
            # Переименовываем пользователя
            user.username = instance.admin_nick
            user.save()  # Сохраняем изменения

        # Проверка изменения пароля проекта (project_password)
        if old_instance.admin_password != instance.admin_password:
            try:
                user.set_password(instance.admin_password)
                user.save()
            except ObjectDoesNotExist:
                # Если пользователь не найден, ничего не делаем.
                pass

        user.is_staff = True
        user.is_superuser = True
        user.save()

        # if old_instance.is_admin:
        #     user.is_staff = True
        #     user.is_superuser = True
        #     user.save()
        #
        # if not old_instance.is_admin:
        #     user.is_staff = False
        #     user.is_superuser = False
        #     user.save()

@receiver(post_save, sender=Adminstrator)
def create_user_for_adminstrator(sender, instance: Adminstrator, created: bool, **kwargs) -> None:
    """
    После создания проекта:
    - Создаёт пользователя с именем, равным project_name, и указанным паролем.
    - Если проект имеет приоритет (is_priority=True), пользователь становится администратором.
    """
    if created:
        username = instance.admin_nick
        new_user = User.objects.create_user(
            username=username,
            password=instance.admin_password
        )
        new_user.is_staff = True
        new_user.is_superuser = True
        new_user.save()

@receiver(post_delete, sender=Adminstrator)
def delete_adminstrator_user(sender, instance, **kwargs):
    """
    После удаления проекта:
      - Удаляем пользователя, ассоциированного с проектом (по username, равному project_nick).
    """
    try:
        user = User.objects.get(username=instance.admin_nick)
        user.delete()
    except User.DoesNotExist:
        pass


# Модель Проекта
class Project(UUIDMixin, TimeStampedMixin):
    project_nick = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Логин для авторизации'
    )
    project_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Проект'
    )
    is_priority = models.BooleanField(verbose_name='Имеет приоритет')
    # is_admin = models.BooleanField(verbose_name='Является администратором')
    responsible_person = models.CharField(
        max_length=255,
        verbose_name='Руководитель проекта'
    )
    project_password = models.CharField(
        max_length=128,
        verbose_name='Пароль для входа'
    )

    class Meta:
        db_table = 'public"."project'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return f"{self.project_name} ({self.responsible_person}) : {'Приоритетный' if self.is_priority else 'Не приоритетный'} "

    def clean(self):
        """
        Дополнительная валидация имени проекта.
        """
        if not self.project_nick.isalnum():
            raise ValidationError("Никнейм проекта должен содержать буквенно-цифровые символы.")

            # Проверка project_password: минимальная длина 8 символов
        if len(self.project_password) < 8:
            raise ValidationError(
                "Пароль для входа должен содержать не менее 8 символов.")

        # Дополнительные проверки пароля можно добавить, например:
        # Проверка на наличие хотя бы одной буквы и одной цифры:
        if not re.search(r"[A-Za-z]",
                         self.project_password) or not re.search(r"\d",
                                                                 self.project_password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну букву и одну цифру.")

        super().clean()

@receiver(pre_save, sender=Project)
def update_project_username(sender, instance, **kwargs):
    """
    При обновлении проекта проверяет, изменилось ли имя проекта.
    Если да, пытается найти пользователя с предыдущим именем и обновляет его username.
    """
    if instance.pk:
        try:
            old_instance = Project.objects.get(pk=instance.pk)
        except Project.DoesNotExist:
            return

            # Получаем пользователя по старому имени
        try:
            user = User.objects.get(username=old_instance.project_nick)
        except User.DoesNotExist:
            # Если пользователь не найден, ничего не делаем
            return

            # Проверка изменения имени администратора (admin_nick)
        if old_instance.project_nick != instance.project_nick:
            # Проверяем, существует ли уже пользователь с новым именем
            if User.objects.filter(username=instance.project_nick).exists():
                raise ValidationError(
                    f"Имя Прибора {instance.project_nick} уже занято.")
            # Переименовываем пользователя
            user.username = instance.project_nick
            user.save()  # Сохраняем изменения


        # Проверка изменения пароля проекта (project_password)
        if old_instance.project_password != instance.project_password:
            try:
                user.set_password(instance.project_password)
                user.save()
            except ObjectDoesNotExist:
                # Если пользователь не найден, ничего не делаем.
                pass

        user.is_staff = False
        user.is_superuser = False
        user.save()

        # if old_instance.is_admin:
        #     user.is_staff = True
        #     user.is_superuser = True
        #     user.save()
        #
        # if not old_instance.is_admin:
        #     user.is_staff = False
        #     user.is_superuser = False
        #     user.save()

@receiver(post_save, sender=Project)
def create_user_for_project(sender, instance: Project, created: bool, **kwargs) -> None:
    """
    После создания проекта:
    - Создаёт пользователя с именем, равным project_name, и указанным паролем.
    - Если проект имеет приоритет (is_priority=True), пользователь становится администратором.
    """
    if created:
        username = instance.project_nick
        new_user = User.objects.create_user(
            username=username,
            password=instance.project_password
        )
        new_user.is_staff = False
        new_user.is_superuser = False
        new_user.save()

@receiver(post_delete, sender=Project)
def delete_project_user(sender, instance, **kwargs):
    """
    После удаления проекта:
      - Удаляем пользователя, ассоциированного с проектом (по username, равному project_nick).
    """
    try:
        user = User.objects.get(username=instance.project_nick)
        user.delete()
    except User.DoesNotExist:
        pass