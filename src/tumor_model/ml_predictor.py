import joblib
import pandas as pd
from pathlib import Path

class TreatmentPredictor:
    def __init__(self):
        self.model_loaded = False
        try:
            # ПРАВИЛЬНЫЙ путь к модели
            model_path = Path(__file__).resolve().parent.parent / 'ml_model.joblib'
            print(f"Looking for model at: {model_path}")
            
            if model_path.exists():
                self.model = joblib.load(model_path)
                self.model_loaded = True
                print("✅ ML model loaded successfully")
            else:
                self.model = None
                self.model_loaded = False
                print("❌ ML model file not found")
                
        except Exception as e:
            self.model = None
            self.model_loaded = False
            print(f"❌ Error loading ML model: {e}")
        
        # Варианты лечения
        self.treatment_options = {
            'surgery': 'Хирургическое лечение',
            'surgery_chemotherapy': 'Хирургия + Химиотерапия', 
            'surgery_targeted': 'Хирургия + Таргетная терапия',
            'chemotherapy': 'Химиотерапия',
            'hormone_therapy': 'Гормональная терапия'
        }
    
    def prepare_features(self, patient_data):
        """Подготовка признаков для модели"""
        try:
            features = {
                'age': getattr(patient_data, 'age', 50),
                'stage': getattr(patient_data, 'stage', 2),
                'ki67_level': getattr(patient_data, 'ki67_level', 20.0),
                'tumor_size_before': getattr(patient_data, 'tumor_size_before', 3.0),
                'er_status': 1 if getattr(patient_data, 'er_status', 'positive') == 'positive' else 0,
                'pr_status': 1 if getattr(patient_data, 'pr_status', 'positive') == 'positive' else 0,
                'her2_status': 1 if getattr(patient_data, 'her2_status', 'negative') == 'positive' else 0,
                'positive_lymph_nodes': getattr(patient_data, 'positive_lymph_nodes', 0),
                'tumor_grade': int(getattr(patient_data, 'tumor_grade', 'G2')[1]),  # G1 -> 1, G2 -> 2, G3 -> 3
                'brca_mutation': 1 if getattr(patient_data, 'brca_mutation', 'no') == 'yes' else 0,
                'family_history': 1 if getattr(patient_data, 'family_history', 'no') == 'yes' else 0
            }
            
            # Менопаузальные статусы
            menopausal_status = getattr(patient_data, 'menopausal_status', 'postmenopausal')
            features['menopausal_status_pre'] = 1 if menopausal_status == 'premenopausal' else 0
            features['menopausal_status_post'] = 1 if menopausal_status == 'postmenopausal' else 0
            features['menopausal_status_peri'] = 1 if menopausal_status == 'perimenopausal' else 0
            
            print(f"Prepared features: {features}")
            return pd.DataFrame([features])
            
        except Exception as e:
            print(f"Error preparing features: {e}")
            return self._get_default_features()
    
    def _get_default_features(self):
        """Фичи по умолчанию"""
        features = {
            'age': 50, 'stage': 2, 'ki67_level': 20.0, 'tumor_size_before': 3.0,
            'er_status': 1, 'pr_status': 1, 'her2_status': 0, 'positive_lymph_nodes': 0,
            'tumor_grade': 2, 'brca_mutation': 0, 'family_history': 0,
            'menopausal_status_pre': 0, 'menopausal_status_post': 1, 'menopausal_status_peri': 0
        }
        return pd.DataFrame([features])
    
    def predict_best_treatment(self, patient_data):
        """Предсказание лучшего лечения"""
        try:
            if not self.model_loaded:
                print("Using demo predictions - model not loaded")
                return self._get_demo_predictions(patient_data)
            
            features = self.prepare_features(patient_data)
            predictions = {}
            
            for treatment in self.treatment_options.keys():
                try:
                    # Добавляем код лечения
                    features_with_treatment = features.copy()
                    treatment_code = self._encode_treatment(treatment)
                    features_with_treatment['treatment_code'] = treatment_code
                    
                    # Предсказываем
                    tumor_reduction = self.model.predict(features_with_treatment)[0]
                    tumor_reduction = max(10, min(95, round(tumor_reduction, 1)))
                    
                    predictions[treatment] = {
                        'name': self.treatment_options[treatment],
                        'tumor_reduction': tumor_reduction,
                        'success_probability': self._calculate_success_probability(tumor_reduction)
                    }
                    
                except Exception as e:
                    print(f"Error predicting for {treatment}: {e}")
                    continue
            
            if not predictions:
                return self._get_demo_predictions(patient_data)
                
            # Сортируем по эффективности
            sorted_predictions = sorted(
                predictions.items(), 
                key=lambda x: x[1]['tumor_reduction'], 
                reverse=True
            )
            
            best_treatment_code = sorted_predictions[0][0]
            
            result = {
                'best_treatment': sorted_predictions[0][1],
                'best_treatment_code': best_treatment_code,
                'all_treatments': {k: v for k, v in sorted_predictions},
                'patient_suitability': self._assess_patient_suitability(patient_data, best_treatment_code),
                'model_used': True
            }
            
            print(f"Predictions ready: {result['best_treatment']}")
            return result
            
        except Exception as e:
            print(f"Error in predict_best_treatment: {e}")
            return self._get_demo_predictions(patient_data)
    
    def _encode_treatment(self, treatment):
        """Кодирование лечения"""
        encoding = {
            'surgery': 1,
            'surgery_chemotherapy': 2,
            'surgery_targeted': 3, 
            'chemotherapy': 4,
            'hormone_therapy': 5
        }
        return encoding.get(treatment, 0)
    
    def _calculate_success_probability(self, reduction):
        """Вероятность успеха"""
        if reduction > 70:
            return "Очень высокая"
        elif reduction > 50:
            return "Высокая" 
        elif reduction > 30:
            return "Средняя"
        else:
            return "Низкая"
    
    def _assess_patient_suitability(self, patient_data, best_treatment):
        """Оценка подходящести"""
        factors = []
        
        if not patient_data:
            return ["Демо-режим: используются стандартные рекомендации"]
        
        ki67 = getattr(patient_data, 'ki67_level', 20)
        her2_status = getattr(patient_data, 'her2_status', 'negative')
        er_status = getattr(patient_data, 'er_status', 'positive')
        brca_status = getattr(patient_data, 'brca_mutation', 'no')
        
        if ki67 > 20 and 'chemotherapy' in best_treatment:
            factors.append("Высокий Ki-67 (>20%) благоприятствует химиотерапии")
        
        if her2_status == 'positive' and 'targeted' in best_treatment:
            factors.append("HER2+ статус оптимален для таргетной терапии")
            
        if er_status == 'positive' and 'hormone' in best_treatment:
            factors.append("ER+ статус идеален для гормональной терапии")
            
        if brca_status == 'yes' and 'targeted' in best_treatment:
            factors.append("Мутация BRCA повышает эффективность таргетной терапии")
            
        if not factors:
            factors.append("Пациент подходит для выбранного метода лечения")
            
        return factors
    
    def _get_demo_predictions(self, patient_data=None):
        """Демо-предсказания"""
        print("Using demo predictions")
        
        return {
            'best_treatment': {
                'name': 'Хирургия + Таргетная терапия',
                'tumor_reduction': 78.5,
                'success_probability': 'Очень высокая'
            },
            'best_treatment_code': 'surgery_targeted',
            'all_treatments': {
                'surgery_targeted': {'name': 'Хирургия + Таргетная терапия', 'tumor_reduction': 78.5, 'success_probability': 'Очень высокая'},
                'surgery_chemotherapy': {'name': 'Хирургия + Химиотерапия', 'tumor_reduction': 65.2, 'success_probability': 'Высокая'},
                'surgery': {'name': 'Хирургическое лечение', 'tumor_reduction': 45.8, 'success_probability': 'Средняя'},
                'chemotherapy': {'name': 'Химиотерапия', 'tumor_reduction': 35.3, 'success_probability': 'Средняя'},
                'hormone_therapy': {'name': 'Гормональная терапия', 'tumor_reduction': 28.1, 'success_probability': 'Низкая'}
            },
            'patient_suitability': ["HER2+ статус оптимален для таргетной терапии", "Высокий Ki-67 благоприятствует комбинированному лечению"],
            'model_used': False
        }

# Создаем глобальный инстанс
try:
    predictor = TreatmentPredictor()
except Exception as e:
    print(f"Failed to create predictor: {e}")
    predictor = None