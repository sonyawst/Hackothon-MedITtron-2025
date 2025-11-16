from django.db import models
import uuid
import hashlib

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Женский'),
        ('Male', 'Мужской'),
        ('Other', 'Другой'),
    ]

    MENOPAUSAL_STATUS_CHOICES = [
        ('Premenopausal', 'Пременопаузальный'),
        ('Perimenopausal', 'Перименопаузальный'),
        ('Postmenopausal', 'Постменопаузальный'),
        ('Unknown', 'Неизвестно'),
    ]
    
    patient_hash = models.CharField(max_length=32, unique=True, blank=True)

    # Основная информация
    stage = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    menopausal_status = models.CharField(max_length=20, choices=MENOPAUSAL_STATUS_CHOICES, blank=True, null=True)
    family_history = models.BooleanField(blank=True, null=True)
    
    # Молекулярные характеристики
    molecular_subtype = models.CharField(max_length=50, blank=True, null=True)
    er_status = models.CharField(max_length=10, blank=True, null=True)
    pr_status = models.CharField(max_length=10, blank=True, null=True)
    her2_status = models.CharField(max_length=10, blank=True, null=True)
    brca_mutation = models.CharField(max_length=10, blank=True, null=True)
    ki67_level = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Лечение
    treatment = models.TextField(blank=True, null=True)
    surgery_type = models.CharField(max_length=50, blank=True, null=True)
    
    # Размеры опухоли
    tumor_size_before = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tumor_size_3m = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tumor_size_6m = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tumor_size_12m = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tumor_size_24m = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    # Метастазы
    has_metastasis = models.BooleanField(default=False)
    metastasis_sites = models.TextField(blank=True, null=True)
    
    # Прогностические факторы
    survival_months = models.IntegerField(blank=True, null=True)
    performance_status = models.CharField(max_length=20, blank=True, null=True)
    tumor_grade = models.CharField(max_length=5, blank=True, null=True)
    lymph_node_status = models.CharField(max_length=10, blank=True, null=True)
    positive_lymph_nodes = models.IntegerField(blank=True, null=True)
    treatment_response = models.CharField(max_length=50, blank=True, null=True)
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.patient_hash:
            # Более короткий хэш (MD5)
            unique_string = f"{self.age}{self.gender}{self.stage}{uuid.uuid4()}"
            self.patient_hash = hashlib.md5(unique_string.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Пациент {self.id} - {self.gender}, {self.age} лет"