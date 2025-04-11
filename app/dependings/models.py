from django.db import models
import uuid
from basic_elements.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.


class OperatorPerEquipment(models.Model):
    """
    Модель для представления связи между оператором и оборудованием
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Прибор', related_name='equipment')
    operator = models.ForeignKey(Executor, on_delete=models.CASCADE, verbose_name='Исполнитель', related_name='executor_2')
    is_priority = models.BooleanField(default=False, verbose_name='Имеет ли оператор приоритет')

    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если оператор уже связан с оборудованием, выбрасывается ошибка.

        :raises ValidationError: Если уже существует другая запись с такой же связью.
        """
        # Исключаем текущую запись, если она уже существует (например, при обновлении)
        if OperatorPerEquipment.objects.exclude(pk=self.pk).filter(
                operator=self.operator, equipment=self.equipment).exists():
            raise ValidationError(
                f"Оператор {self.operator} уже связан с оборудованием {self.equipment}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.operator} - {self.equipment}"


class AnalyzePerEquipment(models.Model):
    """
    Модель для представления связи между Анализом и оборудованием
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    equipment_name = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Прибор', related_name='equipment_2')
    analazy = models.ForeignKey(Analyze, on_delete=models.CASCADE, verbose_name='Анализ', related_name='analyze_1')
    count_samples = models.IntegerField(default=False, verbose_name='Суточный лимит проб',validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Анализы по оборудованию'
        verbose_name_plural = 'Анализы по оборудованию'

    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если уже существует запись с таким же анализом и оборудованием, выбрасывается ошибка.

        :raises ValidationError: Если уже существует другая запись с такой же связью.
        """
        if AnalyzePerEquipment.objects.exclude(pk=self.pk).filter(
                equipment_name=self.equipment_name, analazy=self.analazy).exists():
            raise ValidationError(
                f"Запись с анализом {self.analazy} и прибором {self.equipment_name} уже существует."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.analazy} - {self.equipment_name}"


class ProjectPerAnalyze(models.Model):
    """
    Модель для представления связи между Проектом и анализом
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_n = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект', related_name='project_2')
    analazy_n = models.ForeignKey(Analyze, on_delete=models.CASCADE, verbose_name='Анализ', related_name='analyze_2')
    limit_samples = models.IntegerField(default=False, verbose_name='Ограничение по колличеству анализов',validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    def clean(self) -> None:
        """
        Проверка перед сохранением записи.
        Если уже существует запись с таким же проектом и анализом, выбрасывается ошибка.

        :raises ValidationError: Если уже существует другая запись с такой же связью.
        """
        if ProjectPerAnalyze.objects.exclude(pk=self.pk).filter(
                project_n=self.project_n, analazy_n=self.analazy_n).exists():
            raise ValidationError(
                f"Запись с проектом {self.project_n} и анализом {self.analazy_n} уже существует."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов clean() перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Проект Анализу'
        verbose_name_plural = 'Проекты Анализам'

    def __str__(self):
        return f"{self.analazy_n} - {self.project_n}"