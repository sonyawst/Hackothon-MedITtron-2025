from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Patient ####---добавила

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

def model_view(request):
    """Страница ввода данных для моделирования"""
    return render(request, 'model.html')

def process_model(request):
    """Обработка данных формы и отображение результатов"""
    if request.method == 'POST':
        # Получаем данные из формы
        patient_data = {
            'age': request.POST.get('patient_age'),
            'weight': request.POST.get('patient_weight'),
            'cancer_type': request.POST.get('cancer_type'),
            'tumor_size': request.POST.get('tumor_size'),
            'growth_rate': request.POST.get('growth_rate'),
            'resistance_level': request.POST.get('resistance_level'),
            'drug_name': request.POST.get('drug_name'),
            'drug_dose': request.POST.get('drug_dose'),
            'treatment_interval': request.POST.get('treatment_interval'),
            'treatment_duration': request.POST.get('treatment_duration'),
        }

        # СОХРАНЕНИЕ В БАЗУ ДАННЫХ ← ДОБАВЛЕНО
    try:
        patient = Patient.objects.create(
            age=int(patient_data['age']),
            # Заполните остальные поля по мере необходимости
            tumor_size_before=float(patient_data['tumor_size']),
            treatment=patient_data['drug_name'],
            # Добавьте другие поля из вашей формы
        )
        patient_hash = patient.patient_hash
    except Exception as e:
        patient_hash = None
        print(f"Ошибка сохранения в БД: {e}")
        
        # ВРЕМЕННЫЕ ДАННЫЕ - заглушка для модели
        # Здесь будет подключена реальная математическая модель
        
        simulation_results = {
            'final_tumor_size': round(float(patient_data['tumor_size']) * 0.65, 1),  # заглушка
            'tumor_reduction': 35,  # заглушка
            'treatment_effectiveness': 'Высокая',  # заглушка
            'patient_id': patient_hash,
        }
        
        recommendations = {
            'optimized_dose': round(float(patient_data['drug_dose']) * 0.8, 1),  # заглушка
            'optimized_interval': int(patient_data['treatment_interval']) - 1,  # заглушка
            'optimized_duration': int(patient_data['treatment_duration']) + 7,  # заглушка
            'toxicity_reduction': 25,  # заглушка
            'effectiveness_improvement': 15,  # заглушка
        }
        
        context = {
            'patient_data': patient_data,
            'simulation_results': simulation_results,
            'recommendations': recommendations,
        }
        
        return render(request, 'response.html', context)
    
    return redirect('model')

# Временный API endpoint для тестирования
def api_simulate(request):
    """API endpoint для симуляции (для будущей интеграции с фронтендом)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Здесь будет вызов математической модели
            return JsonResponse({
                'status': 'success',
                'message': 'Модель в разработке',
                'data': data
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'})


# Новый view для формы пациента
def patient_form(request):
    """Форма для ввода данных пациента"""
    if request.method == 'POST':
        # Сохранение данных пациента в БД
        try:
            patient = Patient.objects.create(
                stage=request.POST.get('stage'),
                age=int(request.POST.get('age')),
                gender=request.POST.get('gender'),
                menopausal_status=request.POST.get('menopausal_status'),
                family_history=request.POST.get('family_history'),
                molecular_subtype=request.POST.get('molecular_subtype'),
                er_status=request.POST.get('er_status'),
                pr_status=request.POST.get('pr_status'),
                her2_status=request.POST.get('her2_status'),
                brca_mutation=request.POST.get('brca_mutation'),
                ki67_level=request.POST.get('ki67_level'),
                treatment=request.POST.get('treatment'),
                surgery_type=request.POST.get('surgery_type'),
                tumor_size_before=request.POST.get('tumor_size_before'),
                tumor_size_3m=request.POST.get('tumor_size_3m'),
                tumor_size_6m=request.POST.get('tumor_size_6m'),
                tumor_size_12m=request.POST.get('tumor_size_12m'),
                tumor_size_24m=request.POST.get('tumor_size_24m'),
                has_metastasis=request.POST.get('has_metastasis'),
                metastasis_sites=request.POST.get('metastasis_sites'),
                survival_months=request.POST.get('survival_months'),
                performance_status=request.POST.get('performance_status'),
                tumor_grade=request.POST.get('tumor_grade'),
                lymph_node_status=request.POST.get('lymph_node_status'),
                positive_lymph_nodes=request.POST.get('positive_lymph_nodes'),
                treatment_response=request.POST.get('treatment_response'),
            )
            return JsonResponse({'success': True, 'patient_id': patient.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'patient_form.html')