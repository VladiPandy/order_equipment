from django.db import models
import uuid
from basic_elements.models import *
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class OperatorPerEquipment(models.Model):
    """
    Модель для представления связи между оператором и оборудованием
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Прибор', related_name='equipment')
    operator = models.ForeignKey(Executor, on_delete=models.CASCADE, verbose_name='Исполнитель', related_name='executor_2')
    is_priority = models.BooleanField(default=False, verbose_name='Имеет ли оператор приоритет')

    class Meta:
        verbose_name = 'Оператор по оборудованию'
        verbose_name_plural = 'Операторы по оборудованию'

    def __str__(self):
        return f"{self.operator} - {self.equipment}"


class AnalyzePerEquipment(models.Model):
    """
    Модель для представления связи между Анализом и оборудованием
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    equipment_name = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Прибор', related_name='equipment_2')
    analazy = models.ForeignKey(Analyze, on_delete=models.CASCADE, verbose_name='Анализ_1', related_name='analyze_1')
    count_samples = models.IntegerField(default=False, verbose_name='Суточный лимит проб',validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Анализы по оборудованию'
        verbose_name_plural = 'Анализы по оборудованию'

    def __str__(self):
        return f"{self.analazy} - {self.equipment_name}"


class ProjectPerAnalyze(models.Model):
    """
    Модель для представления связи между Проектом и анализом
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_n = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект_2', related_name='project_2')
    analazy_n = models.ForeignKey(Analyze, on_delete=models.CASCADE, verbose_name='Анализ_2', related_name='analyze_2')
    limit_samples = models.IntegerField(default=False, verbose_name='Ограничение по колличеству анализов',validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Проект Анализу'
        verbose_name_plural = 'Проекты Анализам'

    def __str__(self):
        return f"{self.analazy_n} - {self.project_n}"