from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import BreastCancerData 

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

def model_view(request):
    """Страница ввода данных для моделирования"""
    return render(request, 'model.html')

def process_model(request):
    if request.method == 'POST':
        try:
            # Собираем данные из формы
            metastasis_sites = request.POST.getlist('metastasis_sites')
            
            patient_data = {
                'full_name': request.POST.get('full_name'),
                'stage': int(request.POST.get('stage')),
                'age': int(request.POST.get('age')),
                'gender': request.POST.get('gender'),
                'menopausal_status': request.POST.get('menopausal_status') if request.POST.get('gender') == 'female' else 'not_applicable',
                'family_history': request.POST.get('family_history'),
                'brca_mutation': request.POST.get('brca_mutation'),
                'molecular_subtype': request.POST.get('molecular_subtype'),
                'er_status': request.POST.get('er_status'),
                'pr_status': request.POST.get('pr_status'),
                'her2_status': request.POST.get('her2_status'),
                'ki67_level': float(request.POST.get('ki67_level')),
                'tumor_grade': request.POST.get('tumor_grade'),
                'tumor_size_before': float(request.POST.get('tumor_size_before')),
                'tumor_size_3m': float(request.POST.get('tumor_size_3m') or 0),
                'tumor_size_6m': float(request.POST.get('tumor_size_6m') or 0),
                'tumor_size_12m': float(request.POST.get('tumor_size_12m') or 0),
                'tumor_size_24m': float(request.POST.get('tumor_size_24m') or 0),
                'treatment': request.POST.get('treatment'),
                'surgery_type': request.POST.get('surgery_type'),
                'has_metastasis': request.POST.get('has_metastasis'),
                'metastasis_size': float(request.POST.get('metastasis_size') or 0),
                'metastasis_sites': ','.join(metastasis_sites),
                'lymph_node_status': request.POST.get('lymph_node_status'),
                'positive_lymph_nodes': int(request.POST.get('positive_lymph_nodes')),
                'performance_status': int(request.POST.get('performance_status')),
            }

            # Сохраняем в базу данных через модель Django
            patient = BreastCancerData(**patient_data)
            patient.save()

            # Перенаправляем на страницу результатов
            return redirect('response')
            
        except Exception as e:
            return render(request, 'model.html', {'error': str(e)})
    
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
            patient = BreastCancerData.objects.create(
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