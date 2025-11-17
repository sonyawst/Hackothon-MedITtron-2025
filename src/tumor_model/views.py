from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import BreastCancerData
from .ml_predictor import predictor

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

def model_view(request):
    """Страница ввода данных"""
    return render(request, 'model.html')

def process_model(request):
    """Обработка данных формы"""
    if request.method == 'POST':
        try:
            print("=== DEBUG: Form submitted ===")
            print(f"POST data: {dict(request.POST)}")
            
            # Собираем данные из формы
            metastasis_sites = request.POST.getlist('metastasis_sites')
            print(f"Metastasis sites: {metastasis_sites}")
            
            # Определяем менопаузальный статус
            menopausal_status = 'not_applicable'
            if request.POST.get('gender') == 'female':
                menopausal_status = request.POST.get('menopausal_status', 'not_applicable')
            print(f"Menopausal status: {menopausal_status}")

            # Проверяем обязательные поля
            required_fields = ['full_name', 'stage', 'age', 'gender', 'family_history', 
                             'brca_mutation', 'molecular_subtype', 'er_status', 'pr_status',
                             'her2_status', 'ki67_level', 'tumor_grade', 'tumor_size_before',
                             'treatment', 'has_metastasis', 'lymph_node_status', 'performance_status']
            
            missing_fields = []
            for field in required_fields:
                if not request.POST.get(field):
                    missing_fields.append(field)
            
            if missing_fields:
                error_msg = f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
                print(f"ERROR: {error_msg}")
                return render(request, 'model.html', {'error': error_msg})

            # Создаем запись в базе данных
            patient = BreastCancerData(
                full_name=request.POST.get('full_name'),
                stage=int(request.POST.get('stage')),
                age=int(request.POST.get('age')),
                gender=request.POST.get('gender'),
                menopausal_status=menopausal_status,
                family_history=request.POST.get('family_history'),
                brca_mutation=request.POST.get('brca_mutation'),
                molecular_subtype=request.POST.get('molecular_subtype'),
                er_status=request.POST.get('er_status'),
                pr_status=request.POST.get('pr_status'),
                her2_status=request.POST.get('her2_status'),
                ki67_level=float(request.POST.get('ki67_level')),
                tumor_grade=request.POST.get('tumor_grade'),
                tumor_size_before=float(request.POST.get('tumor_size_before')),
                tumor_size_3m=float(request.POST.get('tumor_size_3m') or 0),
                tumor_size_6m=float(request.POST.get('tumor_size_6m') or 0),
                tumor_size_12m=float(request.POST.get('tumor_size_12m') or 0),
                tumor_size_24m=float(request.POST.get('tumor_size_24m') or 0),
                treatment=request.POST.get('treatment'),
                surgery_type=request.POST.get('surgery_type', 'none'),
                has_metastasis=request.POST.get('has_metastasis'),
                metastasis_size=float(request.POST.get('metastasis_size') or 0),
                metastasis_sites=','.join(metastasis_sites),
                lymph_node_status=request.POST.get('lymph_node_status'),
                positive_lymph_nodes=int(request.POST.get('positive_lymph_nodes', 0)),
                performance_status=int(request.POST.get('performance_status')),
            )
            
            print("=== DEBUG: Attempting to save patient ===")
            patient.save()
            print(f"=== DEBUG: Patient saved with ID: {patient.id} ===")

            # Сохраняем ID пациента в сессии для использования на странице результатов
            request.session['last_patient_id'] = patient.id
            print(f"=== DEBUG: Session set with patient ID: {patient.id} ===")

            # Получаем предсказания от ML модели          
            if predictor and predictor.model_loaded:
                print(f"=== DEBUG: Model type: {type(predictor.model)}")
                print(f"=== DEBUG: Model has predict: {hasattr(predictor.model, 'predict')}")
                ml_predictions = predictor.predict_best_treatment(patient)
                print(f"=== DEBUG: ML predictions received: {ml_predictions is not None} ===")
            else:
                raise Exception("ML модель не загружена или недоступна")
            
            # Формируем данные пациента для шаблона
            patient_data_dict = {
                'full_name': patient.full_name,
                'age': patient.age,
                'stage': patient.stage,
                'ki67_level': patient.ki67_level,
                'tumor_size_before': patient.tumor_size_before,
                'er_status': patient.er_status,
                'pr_status': patient.pr_status,
                'her2_status': patient.her2_status,
                'brca_mutation': patient.brca_mutation,
                'molecular_subtype': patient.molecular_subtype,  
                'gender': patient.gender,
                'menopausal_status': patient.menopausal_status
            }
            
            print("=== DEBUG: Redirecting to response page ===")
            return render(request, 'response.html', {
                'patient_data': patient_data_dict,
                'ml_predictions': ml_predictions
            })
        
            
        except Exception as e:
            # В случае ошибки показываем сообщение об ошибке
            error_msg = f'Ошибка при обработке данных: {str(e)}'
            print(f"=== DEBUG: ERROR: {error_msg} ===")
            import traceback
            traceback.print_exc()
            return render(request, 'model.html', {'error': error_msg})
    
    return redirect('model')

def response_view(request):
    """Страница результатов с ML предсказаниями"""
    # Получаем последнего пациента из базы данных
    try:
        patient_id = request.session.get('last_patient_id')
        if patient_id:
            patient = BreastCancerData.objects.get(id=patient_id)
        else:
            patient = BreastCancerData.objects.latest('created_at')
    except BreastCancerData.DoesNotExist:
        # Если нет записей, показываем ошибку
        return render(request, 'error.html', {
            'error_message': 'Нет данных пациента для анализа'
        })

    # Получаем предсказания от ML модели
    ml_predictions = None
    if predictor and predictor.model_loaded:
        try:
            ml_predictions = predictor.predict_best_treatment(patient)
        except Exception as e:
            return render(request, 'error.html', {
                'error_message': f'Ошибка ML предсказания: {str(e)}'
            })
    else:
        return render(request, 'error.html', {
            'error_message': 'ML модель не загружена'
        })

    # Формируем контекст для шаблона
    context = {
        'patient_data': {
            'full_name': patient.full_name,
            'age': patient.age,
            'stage': patient.stage,
            'ki67_level': patient.ki67_level,
            'tumor_size_before': patient.tumor_size_before,
            'er_status': patient.er_status,
            'her2_status': patient.her2_status,
            'brca_mutation': patient.brca_mutation
        },
        'ml_predictions': ml_predictions,
        'survival_prediction': {
            'months': 84,
            'confidence_interval': '72-96 месяцев',
            'six_month': 98,
            'one_year': 95,
            'two_year': 88
        }
    }
    
    return render(request, 'response.html', context)