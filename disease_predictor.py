import joblib
import numpy as np
import os
from collections import Counter

class DiseasePredictor:
    def __init__(self):
        self.models = {}
        self.symptoms = []
        self.load_models()
        
        # Disease information and prevention tips
        self.disease_info = {
            'Common Cold': {
                'description': 'A viral infection of the upper respiratory tract, commonly affecting the nose and throat.',
                'prevention': [
                    'Wash hands frequently with soap and water',
                    'Avoid close contact with sick individuals',
                    'Avoid touching your face with unwashed hands',
                    'Get adequate sleep and maintain a healthy diet',
                    'Stay hydrated'
                ],
                'treatment': [
                    'Get plenty of rest',
                    'Stay hydrated with fluids',
                    'Use over-the-counter pain relievers if needed',
                    'Consider throat lozenges for sore throat',
                    'Use a humidifier to ease congestion'
                ]
            },
            'Influenza': {
                'description': 'A highly contagious viral infection that affects the respiratory system.',
                'prevention': [
                    'Get an annual flu vaccination',
                    'Wash hands frequently',
                    'Avoid close contact with infected people',
                    'Maintain a strong immune system',
                    'Clean and disinfect surfaces regularly'
                ],
                'treatment': [
                    'Rest and stay home to avoid spreading infection',
                    'Drink plenty of fluids',
                    'Take antiviral medications if prescribed',
                    'Use fever reducers and pain relievers as needed',
                    'Seek medical attention if symptoms worsen'
                ]
            },
            'COVID-19': {
                'description': 'A contagious disease caused by the SARS-CoV-2 virus, affecting primarily the respiratory system.',
                'prevention': [
                    'Get vaccinated and stay up to date with boosters',
                    'Wear masks in crowded or indoor spaces',
                    'Maintain physical distance from others',
                    'Wash hands frequently or use hand sanitizer',
                    'Improve ventilation in indoor spaces'
                ],
                'treatment': [
                    'Isolate to prevent spreading the virus',
                    'Monitor symptoms and seek medical care if severe',
                    'Rest and stay hydrated',
                    'Take medications as prescribed by healthcare provider',
                    'Use pulse oximeter to monitor oxygen levels if available'
                ]
            },
            'Pneumonia': {
                'description': 'An infection that inflames air sacs in one or both lungs, which may fill with fluid.',
                'prevention': [
                    'Get pneumonia and flu vaccines',
                    'Practice good hygiene',
                    'Don\'t smoke and avoid secondhand smoke',
                    'Maintain a healthy lifestyle',
                    'Manage chronic conditions properly'
                ],
                'treatment': [
                    'Take prescribed antibiotics if bacterial',
                    'Get plenty of rest',
                    'Drink fluids to help loosen secretions',
                    'Use fever reducers and pain relievers',
                    'Seek immediate medical attention for severe symptoms'
                ]
            },
            'Bronchitis': {
                'description': 'Inflammation of the lining of the bronchial tubes, causing cough and mucus production.',
                'prevention': [
                    'Avoid smoking and secondhand smoke',
                    'Get annual flu shots',
                    'Wash hands frequently',
                    'Wear a mask in polluted environments',
                    'Avoid respiratory irritants'
                ],
                'treatment': [
                    'Rest and avoid strenuous activities',
                    'Drink plenty of fluids',
                    'Use a humidifier',
                    'Take cough suppressants if recommended',
                    'Avoid smoking and irritants'
                ]
            },
            'Gastroenteritis': {
                'description': 'Inflammation of the stomach and intestines, typically caused by viral or bacterial infection.',
                'prevention': [
                    'Wash hands thoroughly and frequently',
                    'Avoid contaminated food and water',
                    'Practice safe food handling',
                    'Get rotavirus vaccine for infants',
                    'Avoid close contact with infected individuals'
                ],
                'treatment': [
                    'Stay hydrated with clear fluids',
                    'Follow the BRAT diet (bananas, rice, applesauce, toast)',
                    'Avoid dairy, caffeine, and fatty foods',
                    'Rest and avoid solid foods initially',
                    'Seek medical care if dehydration occurs'
                ]
            },
            'Migraine': {
                'description': 'A recurring headache disorder characterized by severe, throbbing pain often on one side of the head.',
                'prevention': [
                    'Identify and avoid personal triggers',
                    'Maintain regular sleep schedule',
                    'Stay hydrated and eat regular meals',
                    'Manage stress through relaxation techniques',
                    'Limit alcohol and caffeine intake'
                ],
                'treatment': [
                    'Take prescribed migraine medications early',
                    'Rest in a dark, quiet room',
                    'Apply cold or warm compress to head/neck',
                    'Practice relaxation techniques',
                    'Stay hydrated'
                ]
            },
            'Sinusitis': {
                'description': 'Inflammation of the sinuses, causing blocked nasal passages and facial pain.',
                'prevention': [
                    'Avoid allergens and irritants',
                    'Use a humidifier',
                    'Practice good hand hygiene',
                    'Manage allergies effectively',
                    'Avoid smoking'
                ],
                'treatment': [
                    'Use saline nasal rinses',
                    'Apply warm compresses to face',
                    'Stay hydrated',
                    'Use decongestants as directed',
                    'Take antibiotics if prescribed for bacterial infection'
                ]
            },
            'Allergic Rhinitis': {
                'description': 'An allergic reaction causing sneezing, congestion, runny nose, and sore throat.',
                'prevention': [
                    'Identify and avoid allergens',
                    'Keep windows closed during high pollen seasons',
                    'Use air purifiers',
                    'Wash bedding in hot water weekly',
                    'Shower after outdoor activities'
                ],
                'treatment': [
                    'Take antihistamines as directed',
                    'Use nasal corticosteroid sprays',
                    'Try saline nasal rinses',
                    'Consider immunotherapy for severe cases',
                    'Avoid known allergens'
                ]
            },
            'Strep Throat': {
                'description': 'A bacterial infection of the throat and tonsils caused by group A Streptococcus.',
                'prevention': [
                    'Wash hands frequently',
                    'Avoid sharing personal items',
                    'Avoid close contact with infected individuals',
                    'Maintain good oral hygiene',
                    'Replace toothbrush after infection clears'
                ],
                'treatment': [
                    'Take prescribed antibiotics completely',
                    'Rest and drink plenty of fluids',
                    'Use throat lozenges or warm salt water gargles',
                    'Take pain relievers as needed',
                    'Stay home until fever-free for 24 hours'
                ]
            }
        }
    
    def load_models(self):
        """Load trained models and symptoms list"""
        try:
            if os.path.exists("models/symptoms.joblib"):
                self.symptoms = joblib.load("models/symptoms.joblib")
            
            model_files = ['random_forest.joblib', 'naive_bayes.joblib', 'logistic_regression.joblib']
            
            for model_file in model_files:
                model_path = f"models/{model_file}"
                if os.path.exists(model_path):
                    model_name = model_file.replace('.joblib', '')
                    self.models[model_name] = joblib.load(model_path)
            
            if not self.models:
                print("No models found. Training new models...")
                from data_generator import train_models
                train_models()
                self.load_models()
                
        except Exception as e:
            print(f"Error loading models: {e}")
            # If models don't exist, train them
            from data_generator import train_models
            train_models()
            self.load_models()
    
    def predict_disease(self, selected_symptoms):
        """Predict disease based on selected symptoms"""
        if not self.models or not self.symptoms:
            return None, 0.0
        
        # Create feature vector
        feature_vector = [1 if symptom in selected_symptoms else 0 for symptom in self.symptoms]
        feature_array = np.array(feature_vector).reshape(1, -1)
        
        # Get predictions from all models
        predictions = []
        confidences = []
        
        for model_name, model in self.models.items():
            try:
                pred = model.predict(feature_array)[0]
                
                # Get prediction probability/confidence
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(feature_array)[0]
                    confidence = max(proba)
                else:
                    confidence = 0.8  # Default confidence for models without probability
                
                predictions.append(pred)
                confidences.append(confidence)
                
            except Exception as e:
                print(f"Error with model {model_name}: {e}")
                continue
        
        if not predictions:
            return None, 0.0
        
        # Use majority voting or highest confidence prediction
        if len(predictions) == 1:
            return predictions[0], confidences[0]
        
        # Find most common prediction
        prediction_counts = Counter(predictions)
        most_common_pred = prediction_counts.most_common(1)[0][0]
        
        # Calculate average confidence for the most common prediction
        avg_confidence = np.mean([conf for pred, conf in zip(predictions, confidences) 
                                 if pred == most_common_pred])
        
        return most_common_pred, avg_confidence
    
    def get_disease_info(self, disease_name):
        """Get disease information, prevention tips, and treatment"""
        return self.disease_info.get(disease_name, {
            'description': 'Information not available for this condition.',
            'prevention': ['Consult with a healthcare professional'],
            'treatment': ['Seek medical advice for proper diagnosis and treatment']
        })
    
    def get_available_symptoms(self):
        """Get list of available symptoms"""
        return self.symptoms
