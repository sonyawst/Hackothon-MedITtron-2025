from django.db import models

# utils.py
def django_to_ml_format(patient):
    """Преобразует Django пациента в ML-формат"""
    
    ml_data = {
        # Основные признаки
        'age': patient.age,
        'menopausal_status': patient.menopausal_status,
        'family_history': patient.family_history_bool,
        'molecular_subtype': patient.molecular_subtype,
        'er_status': patient.er_status_bool,
        'pr_status': patient.pr_status_bool, 
        'her2_status': patient.her2_status_bool,
        'brca_mutation': patient.brca_mutation_bool,
        'ki67_level': patient.ki67_level,
        'treatment': patient.treatment,
        'surgery_type': patient.surgery_type,
        'tumor_size_before': patient.tumor_size_before,
        'performance_status': patient.performance_status,
        'tumor_grade': patient.tumor_grade,
        'lymph_node_status': patient.lymph_node_status_bool,
        'positive_lymph_nodes': patient.positive_lymph_nodes,
        'has_metastasis': patient.has_metastasis_bool,
        
        # Целевая переменная для обучения
        'tumor_change_percentage': patient.tumor_change_percentage,
        
        # Дополнительные данные
        'treatment_response': patient.treatment_response,
        'survival_months': patient.survival_months,
    }
    
    return ml_data

class BreastCancerData(models.Model):
    # Основная информация
    full_name = models.CharField(max_length=200, verbose_name="ФИО пациента")
    stage = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], verbose_name="Стадия")
    age = models.IntegerField(verbose_name="Возраст")
    gender = models.CharField(max_length=10, choices=[('male', 'Мужской'), ('female', 'Женский')], verbose_name="Пол")
    menopausal_status = models.CharField(max_length=20, choices=[
    ('premenopausal', 'Пременопауза'),
    ('perimenopausal', 'Перименопауза'), 
    ('postmenopausal', 'Постменопауза'),
    ('not_applicable', 'Не применимо')
    ], default='not_applicable', verbose_name="Менопаузальный статус")

    treatment_response = models.CharField(max_length=20, choices=[
    ('stable', 'Стабильное'),
    ('partial', 'Частичный ответ'), 
    ('complete', 'Полный ответ'),
    ('progression', 'Прогрессирование')
    ], verbose_name="Ответ на лечение")
    
    survival_months = models.FloatField(null=True, blank=True, verbose_name="Выживаемость (месяцы)")
    
    # Анамнез и генетика
    family_history = models.CharField(max_length=10, choices=[('yes', 'Да'), ('no', 'Нет')], verbose_name="Семейный анамнез")
    brca_mutation = models.CharField(max_length=10, choices=[('yes', 'Да'), ('no', 'Нет')], verbose_name="Мутация BRCA")
    
    # Характеристики опухоли
    molecular_subtype = models.CharField(max_length=20, choices=[
        ('HR+HER2-', 'HR+HER2-'),
        ('HR+HER2+', 'HR+HER2+'),
        ('HR-HER2+', 'HR-HER2+'),
        ('TNBC', 'TNBC (Трижды негативный)')
    ], verbose_name="Молекулярный подтип")
    er_status = models.CharField(max_length=10, choices=[('positive', 'Положительный'), ('negative', 'Отрицательный')], verbose_name="ER статус")
    pr_status = models.CharField(max_length=10, choices=[('positive', 'Положительный'), ('negative', 'Отрицательный')], verbose_name="PR статус")
    her2_status = models.CharField(max_length=10, choices=[('positive', 'Положительный'), ('negative', 'Отрицательный')], verbose_name="HER2 статус")
    ki67_level = models.FloatField(verbose_name="Уровень Ki-67 (%)")
    tumor_grade = models.CharField(max_length=2, choices=[('G1', 'G1'), ('G2', 'G2'), ('G3', 'G3')], verbose_name="Гистологическая градация")
    
    # Размеры опухоли
    tumor_size_before = models.FloatField(verbose_name="Размер опухоли до лечения (см)")
    tumor_size_3m = models.FloatField(null=True, blank=True, verbose_name="Размер через 3 месяца (см)")
    tumor_size_6m = models.FloatField(null=True, blank=True, verbose_name="Размер через 6 месяцев (см)")
    tumor_size_12m = models.FloatField(null=True, blank=True, verbose_name="Размер через 12 месяцев (см)")
    tumor_size_24m = models.FloatField(null=True, blank=True, verbose_name="Размер через 24 месяца (см)")
    
    # Лечение
    treatment = models.CharField(max_length=50, choices=[
        ('surgery_only', 'Только хирургия'),
        ('surgery_chemo', 'Хирургия + химиотерапия'),
        ('surgery_target', 'Хирургия + таргетная терапия'),
        ('none', 'Лечение не проводилось')
    ], verbose_name="Тип лечения")
    surgery_type = models.CharField(max_length=20, choices=[
        ('lumpectomy', 'Лампэктомия'),
        ('mastectomy', 'Мастэктомия'),
        ('none', 'Не проводилось')
    ], verbose_name="Тип операции")
    
    # Метастазы
    has_metastasis = models.CharField(max_length=10, choices=[('yes', 'Да'), ('no', 'Нет')], verbose_name="Наличие метастазов")
    metastasis_size = models.FloatField(null=True, blank=True, verbose_name="Размер метастаза (см)")
    metastasis_sites = models.CharField(max_length=100, blank=True, verbose_name="Локализация метастазов")
    
    # Лимфоузлы и общее состояние
    lymph_node_status = models.CharField(max_length=10, choices=[('positive', 'Положительный'), ('negative', 'Отрицательный')], verbose_name="Статус лимфоузлов")
    positive_lymph_nodes = models.IntegerField(verbose_name="Количество пораженных лимфоузлов")
    performance_status = models.IntegerField(choices=[
        (0, '0 - Полностью активен'),
        (1, '1 - Ограниченно активен'),
        (2, '2 - Амбулаторный'),
        (3, '3 - Ограниченно самостоятельный'),
        (4, '4 - Полностью нетрудоспособен')
    ], verbose_name="Статус по шкале ECOG")
    
    def __str__(self):
        return f"{self.full_name} - Стадия {self.stage}"






    
    class Meta:
        db_table = 'breast_cancer_data'
        verbose_name = 'Данные пациента с РМЖ'
        verbose_name_plural = 'Данные пациентов с РМЖ'
