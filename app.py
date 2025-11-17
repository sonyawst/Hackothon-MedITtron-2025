import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Настройки для Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Загружаем модель (если есть)
def load_model():
    try:
        model_path = os.path.join(BASE_DIR, 'model', 'preprocessing_data.joblib')
        model_data = joblib.load(model_path)
        print("✅ Модель загружена")
        return model_data
    except Exception as e:
        print(f"❌ Модель не загружена: {e}")
        return None

model_data = load_model()

if model_data:
    model = model_data['model']
    feature_columns = model_data['feature_columns']
    label_encoders = model_data['label_encoders']
else:
    model = None
    feature_columns = []
    label_encoders = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Модель не загружена'
            })
        
        # Получаем данные из формы
        data = request.form
        
        # Здесь будет ваша логика предсказания
        # Пока возвращаем тестовый результат
        prediction = -15.5  # Пример результата
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'interpretation': f'Прогнозируется уменьшение опухоли на {abs(prediction):.1f}%'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
