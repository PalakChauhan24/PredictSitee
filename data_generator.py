import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

# Common symptoms and diseases for medical prediction
SYMPTOMS = [
    'fever', 'cough', 'headache', 'fatigue', 'sore_throat', 'runny_nose',
    'shortness_of_breath', 'chest_pain', 'nausea', 'vomiting', 'diarrhea',
    'abdominal_pain', 'muscle_aches', 'joint_pain', 'skin_rash', 'dizziness',
    'loss_of_appetite', 'weight_loss', 'night_sweats', 'difficulty_swallowing'
]

DISEASES = [
    'Common Cold', 'Influenza', 'COVID-19', 'Pneumonia', 'Bronchitis',
    'Gastroenteritis', 'Migraine', 'Sinusitis', 'Allergic Rhinitis', 'Strep Throat'
]

# Disease-symptom patterns (probability of symptom occurring with disease)
DISEASE_PATTERNS = {
    'Common Cold': {
        'runny_nose': 0.9, 'sore_throat': 0.8, 'cough': 0.7, 'fatigue': 0.6,
        'headache': 0.5, 'fever': 0.3, 'muscle_aches': 0.4
    },
    'Influenza': {
        'fever': 0.9, 'muscle_aches': 0.8, 'fatigue': 0.9, 'headache': 0.8,
        'cough': 0.7, 'sore_throat': 0.6, 'runny_nose': 0.5
    },
    'COVID-19': {
        'fever': 0.8, 'cough': 0.8, 'fatigue': 0.7, 'shortness_of_breath': 0.6,
        'headache': 0.6, 'sore_throat': 0.5, 'muscle_aches': 0.6,
        'loss_of_appetite': 0.5
    },
    'Pneumonia': {
        'fever': 0.9, 'cough': 0.9, 'shortness_of_breath': 0.8, 'chest_pain': 0.7,
        'fatigue': 0.8, 'headache': 0.5, 'muscle_aches': 0.6
    },
    'Bronchitis': {
        'cough': 0.9, 'fatigue': 0.7, 'chest_pain': 0.6, 'shortness_of_breath': 0.5,
        'fever': 0.4, 'headache': 0.4
    },
    'Gastroenteritis': {
        'nausea': 0.9, 'vomiting': 0.8, 'diarrhea': 0.9, 'abdominal_pain': 0.8,
        'fever': 0.6, 'fatigue': 0.7, 'headache': 0.5
    },
    'Migraine': {
        'headache': 1.0, 'nausea': 0.7, 'dizziness': 0.6, 'fatigue': 0.5,
        'vomiting': 0.4
    },
    'Sinusitis': {
        'headache': 0.8, 'runny_nose': 0.7, 'fever': 0.5, 'fatigue': 0.6,
        'cough': 0.4, 'sore_throat': 0.4
    },
    'Allergic Rhinitis': {
        'runny_nose': 0.9, 'sore_throat': 0.6, 'cough': 0.5, 'headache': 0.4,
        'fatigue': 0.5
    },
    'Strep Throat': {
        'sore_throat': 0.95, 'fever': 0.8, 'headache': 0.7, 'fatigue': 0.6,
        'difficulty_swallowing': 0.8, 'muscle_aches': 0.5
    }
}

def generate_training_data(n_samples=1000):
    """Generate synthetic training data based on disease-symptom patterns"""
    data = []
    
    for _ in range(n_samples):
        # Randomly select a disease
        disease = np.random.choice(DISEASES)
        
        # Generate symptoms based on disease patterns
        symptoms_vector = [0] * len(SYMPTOMS)
        disease_pattern = DISEASE_PATTERNS[disease]
        
        for i, symptom in enumerate(SYMPTOMS):
            if symptom in disease_pattern:
                # Use disease-specific probability
                prob = disease_pattern[symptom]
            else:
                # Low probability for symptoms not associated with disease
                prob = 0.1
            
            # Add some noise to make it more realistic
            prob = prob * np.random.uniform(0.8, 1.2)
            prob = max(0, min(1, prob))  # Keep probability between 0 and 1
            
            symptoms_vector[i] = 1 if np.random.random() < prob else 0
        
        # Ensure at least one symptom is present
        if sum(symptoms_vector) == 0:
            symptoms_vector[np.random.randint(len(SYMPTOMS))] = 1
        
        data.append(symptoms_vector + [disease])
    
    # Create DataFrame
    columns = SYMPTOMS + ['disease']
    df = pd.DataFrame(data, columns=columns)
    
    return df

def train_models():
    """Train multiple ML models for disease prediction"""
    print("Generating training data...")
    df = generate_training_data(2000)
    
    # Prepare features and target
    X = df[SYMPTOMS]
    y = df['disease']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'naive_bayes': MultinomialNB(),
        'logistic_regression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    print("Training models...")
    trained_models = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"{name} accuracy: {accuracy:.3f}")
        
        # Save model
        model_path = f"models/{name}.joblib"
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, model_path)
        
        trained_models[name] = model
    
    # Save symptoms list for later use
    joblib.dump(SYMPTOMS, "models/symptoms.joblib")
    
    print("Models trained and saved successfully!")
    return trained_models

if __name__ == "__main__":
    train_models()
