import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

class TreatmentPredictor:
    def __init__(self):
        self.model_loaded = False
        self.model = None
        self.label_encoders = {}
        
        try:
            model_path = Path(__file__).resolve().parent.parent / 'ml_model.joblib'
            print(f"Looking for model at: {model_path}")
            
            if model_path.exists():
                loaded_data = joblib.load(model_path)
                print(f"Loaded data type: {type(loaded_data)}")
                
                # Если это словарь, извлекаем модель и энкодеры
                if isinstance(loaded_data, dict):
                    # Ищем модель
                    if 'model' in loaded_data:
                        self.model = loaded_data['model']
                    elif 'rf_model' in loaded_data:
                        self.model = loaded_data['rf_model']
                    else:
                        for key, value in loaded_data.items():
                            if hasattr(value, 'predict'):
                                self.model = value
                                print(f"Found model in key: {key}")
                                break
                    
                    # Ищем энкодеры если есть
                    for key, value in loaded_data.items():
                        if isinstance(value, LabelEncoder):
                            # Определяем какая колонка кодируется
                            if 'treatment' in key.lower():
                                self.label_encoders['treatment'] = value
                            elif 'menopausal' in key.lower():
                                self.label_encoders['menopausal_status'] = value
                            # Добавьте другие энкодеры по необходимости
                    
                    if self.model and hasattr(self.model, 'predict'):
                        self.model_loaded = True
                        print("✅ ML model extracted from dictionary successfully")
                        print(f"Model type: {type(self.model)}")
                        if hasattr(self.model, 'n_features_in_'):
                            print(f"Model features: {self.model.n_features_in_}")
                    else:
                        self.model_loaded = False
                        print("❌ No valid model found in dictionary")
                else:
                    self.model = loaded_data
                    if hasattr(self.model, 'predict'):
                        self.model_loaded = True
                        print("✅ ML model loaded successfully")
                        print(f"Model type: {type(self.model)}")
                        if hasattr(self.model, 'n_features_in_'):
                            print(f"Model features: {self.model.n_features_in_}")
                    else:
                        self.model_loaded = False
                        print(f"❌ Loaded object is not a model: {type(self.model)}")
            else:
                self.model_loaded = False
                print("❌ ML model file not found")
                
        except Exception as e:
            self.model = None
            self.model_loaded = False
            print(f"❌ Error loading ML model: {e}")
        
        # Варианты лечения
        self.treatment_options = {
            'surgery_only': 'Хирургическое лечение',
            'surgery_chemo': 'Хирургия + Химиотерапия', 
            'surgery_target': 'Хирургия + Таргетная терапия',
            'chemotherapy': 'Химиотерапия',
            'hormone_therapy': 'Гормональная терапия'
        }
        
        # Категориальные колонки для кодирования
        self.categorical_columns = [
            'menopausal_status', 'molecular_subtype', 'er_status',
            'pr_status', 'her2_status', 'brca_mutation', 'surgery_type',
            'treatment', 'lymph_node_status'
        ]
        
        # Фичи в порядке как при обучении
        self.feature_columns = [
            'age', 'menopausal_status_encoded', 'family_history',
            'molecular_subtype_encoded', 'er_status_encoded', 'pr_status_encoded',
            'her2_status_encoded', 'brca_mutation_encoded', 'ki67_level',
            'treatment_encoded', 'surgery_type_encoded', 'tumor_size_before',
            'performance_status', 'tumor_grade', 'lymph_node_status_encoded',
            'positive_lymph_nodes'
        ]
    
    def prepare_features(self, patient_data):
        """Подготовка признаков из текстовых данных с кодированием"""
        try:
            # Создаем словарь с исходными данными
            raw_features = {
                'age': getattr(patient_data, 'age', 35),
                'menopausal_status': getattr(patient_data, 'menopausal_status', 'premenopausal'),
                'family_history': 1 if getattr(patient_data, 'family_history', 'no') == 'yes' else 0,
                'molecular_subtype': getattr(patient_data, 'molecular_subtype', 'HR+HER2-'),
                'er_status': getattr(patient_data, 'er_status', 'positive'),
                'pr_status': getattr(patient_data, 'pr_status', 'positive'),
                'her2_status': getattr(patient_data, 'her2_status', 'negative'),
                'brca_mutation': getattr(patient_data, 'brca_mutation', 'no'),
                'ki67_level': getattr(patient_data, 'ki67_level', 15.0),
                'treatment': 'surgery_only',  # Будет меняться для каждого лечения
                'surgery_type': getattr(patient_data, 'surgery_type', 'lumpectomy'),
                'tumor_size_before': getattr(patient_data, 'tumor_size_before', 3.0),
                'performance_status': getattr(patient_data, 'performance_status', 1),
                'tumor_grade': getattr(patient_data, 'tumor_grade', 'G1'),
                'lymph_node_status': getattr(patient_data, 'lymph_node_status', 'negative'),
                'positive_lymph_nodes': getattr(patient_data, 'positive_lymph_nodes', 0)
            }
            
            print(f"Raw features from form: {raw_features}")
            
            # Кодируем категориальные переменные
            encoded_features = self._encode_categorical_features(raw_features)
            
            # Создаем фичи в правильном порядке
            ordered_features = [
                encoded_features['age'],
                encoded_features['menopausal_status_encoded'],
                encoded_features['family_history'],
                encoded_features['molecular_subtype_encoded'],
                encoded_features['er_status_encoded'],
                encoded_features['pr_status_encoded'],
                encoded_features['her2_status_encoded'],
                encoded_features['brca_mutation_encoded'],
                encoded_features['ki67_level'],
                encoded_features['treatment_encoded'],  # Будет меняться
                encoded_features['surgery_type_encoded'],
                encoded_features['tumor_size_before'],
                encoded_features['performance_status'],
                int(encoded_features['tumor_grade'][1]),  # G1 -> 1, G2 -> 2, G3 -> 3
                encoded_features['lymph_node_status_encoded'],
                encoded_features['positive_lymph_nodes']
            ]
            
            print(f"Encoded features: {ordered_features}")
            return ordered_features
            
        except Exception as e:
            print(f"Error preparing features: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _encode_categorical_features(self, raw_features):
        """Кодирование категориальных переменных как при обучении"""
        encoded = raw_features.copy()
        
        # Создаем временные энкодеры если нет сохраненных
        for col in self.categorical_columns:
            if col + '_encoded' not in encoded:
                if col in ['er_status', 'pr_status', 'her2_status', 'brca_mutation', 'family_history', 'lymph_node_status']:
                    # Бинарное кодирование
                    if col in ['er_status', 'pr_status', 'her2_status']:
                        encoded[col + '_encoded'] = 1 if encoded[col] == 'positive' else 0
                    elif col == 'brca_mutation':
                        encoded[col + '_encoded'] = 1 if encoded[col] == 'yes' else 0
                    elif col == 'family_history':
                        encoded[col + '_encoded'] = encoded[col]  # Уже закодировано
                    elif col == 'lymph_node_status':
                        encoded[col + '_encoded'] = 1 if encoded[col] == 'positive' else 0
                else:
                    # Категориальное кодирование
                    if col == 'menopausal_status':
                        encoding = {'premenopausal': 0, 'perimenopausal': 1, 'postmenopausal': 2}
                        encoded[col + '_encoded'] = encoding.get(encoded[col], 0)
                    elif col == 'molecular_subtype':
                        encoding = {'HR+HER2-': 0, 'HR+HER2+': 1, 'HR-HER2+': 2, 'Triple Negative': 3}
                        encoded[col + '_encoded'] = encoding.get(encoded[col], 0)
                    elif col == 'surgery_type':
                        encoding = {'lumpectomy': 0, 'mastectomy': 1}
                        encoded[col + '_encoded'] = encoding.get(encoded[col], 0)
                    elif col == 'treatment':
                        # treatment будет кодироваться отдельно для каждого варианта
                        encoding = {
                            'surgery_only': 0, 'surgery_chemo': 1, 'surgery_target': 2,
                            'chemotherapy': 3, 'hormone_therapy': 4
                        }
                        encoded[col + '_encoded'] = encoding.get(encoded[col], 0)
                    else:
                        # По умолчанию используем простую нумерацию
                        unique_vals = list(set([encoded[col]]))
                        encoding = {val: i for i, val in enumerate(unique_vals)}
                        encoded[col + '_encoded'] = encoding.get(encoded[col], 0)
        
        return encoded
    
    def predict_best_treatment(self, patient_data):
        """Предсказание лучшего лечения (аналог predict_treatment_effectiveness)"""
        try:
            if not self.model_loaded or self.model is None:
                raise Exception("ML model not loaded")
            
            # Подготавливаем базовые фичи (с treatment='surgery_only' по умолчанию)
            base_features = self.prepare_features(patient_data)
            if base_features is None:
                raise Exception("Failed to prepare features")
            
            predictions = {}
            
            # Предсказываем для каждого метода лечения
            for treatment_code in self.treatment_options.keys():
                try:
                    # Создаем копию фичей с текущим лечением
                    treatment_features = base_features.copy()
                    
                    # Находим индекс treatment_encoded и обновляем его
                    treatment_idx = self.feature_columns.index('treatment_encoded')
                    
                    # Кодируем лечение
                    treatment_encoding = {
                        'surgery_only': 0, 'surgery_chemo': 1, 'surgery_target': 2,
                        'chemotherapy': 3, 'hormone_therapy': 4
                    }
                    treatment_encoded = treatment_encoding.get(treatment_code, 0)
                    treatment_features[treatment_idx] = treatment_encoded
                    
                    # Преобразуем в DataFrame в правильном порядке
                    feature_df = pd.DataFrame([treatment_features], columns=self.feature_columns)
                    
                    # Предсказываем уменьшение опухоли
                    tumor_reduction = self.model.predict(feature_df)[0]
                    
                    # Ограничиваем значения разумными пределами
                    tumor_reduction = max(0, min(100, round(float(tumor_reduction), 1)))
                    
                    predictions[treatment_code] = {
                        'name': self.treatment_options[treatment_code],
                        'tumor_reduction': tumor_reduction,
                        'success_probability': self._calculate_success_probability(tumor_reduction)
                    }
                    
                    print(f"Prediction for {treatment_code}: {tumor_reduction}%")
                    
                except Exception as e:
                    print(f"Error predicting for {treatment_code}: {e}")
                    continue
            
            if not predictions:
                raise Exception("No successful predictions")
                
            # Находим лучшее лечение
            best_treatment_code = max(predictions.keys(), 
                                    key=lambda x: predictions[x]['tumor_reduction'])
            
            result = {
                'best_treatment': predictions[best_treatment_code],
                'best_treatment_code': best_treatment_code,
                'all_treatments': predictions,
                'patient_suitability': self._assess_patient_suitability(patient_data, best_treatment_code),
                'model_used': True,
                'demo_mode': False
            }
            
            print(f"Best treatment: {result['best_treatment']}")
            return result
            
        except Exception as e:
            print(f"Error in predict_best_treatment: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"ML prediction failed: {str(e)}")
    
    def _calculate_success_probability(self, reduction):
        """Вероятность успеха"""
        reduction = float(reduction)
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
        
        ki67 = getattr(patient_data, 'ki67_level', 20)
        her2_status = getattr(patient_data, 'her2_status', 'negative')
        er_status = getattr(patient_data, 'er_status', 'positive')
        brca_status = getattr(patient_data, 'brca_mutation', 'no')
        molecular_subtype = getattr(patient_data, 'molecular_subtype', 'HR+HER2-')
        
        # Анализ на основе характеристик пациента
        if ki67 > 20 and 'chemo' in best_treatment:
            factors.append("Высокий Ki-67 (>20%) благоприятствует химиотерапии")
        
        if her2_status == 'positive' and 'target' in best_treatment:
            factors.append("HER2+ статус оптимален для таргетной терапии")
            
        if er_status == 'positive' and 'hormone' in best_treatment:
            factors.append("ER+ статус идеален для гормональной терапии")
            
        if brca_status == 'yes' and 'target' in best_treatment:
            factors.append("Мутация BRCA повышает эффективность таргетной терапии")
            
        if molecular_subtype == 'Triple Negative' and 'chemo' in best_treatment:
            factors.append("Трижды негативный РМЖ лучше отвечает на химиотерапию")
            
        if not factors:
            factors.append("Выбранный метод оптимален для данного профиля пациента")
            
        return factors

# Создаем глобальный инстанс
try:
    predictor = TreatmentPredictor()
except Exception as e:
    print(f"Failed to create predictor: {e}")
    predictor = None