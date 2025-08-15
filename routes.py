from flask import render_template, request, flash, redirect, url_for
from app import app
from disease_predictor import DiseasePredictor
import logging

# Initialize disease predictor
predictor = DiseasePredictor()

@app.route('/')
def index():
    """Main page with symptom selection form"""
    symptoms = predictor.get_available_symptoms()
    # Convert snake_case to readable format
    readable_symptoms = []
    for symptom in symptoms:
        readable = symptom.replace('_', ' ').title()
        readable_symptoms.append((symptom, readable))
    
    return render_template('index.html', symptoms=readable_symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    """Process form submission and predict disease"""
    try:
        # Get selected symptoms from form
        selected_symptoms = request.form.getlist('symptoms')
        
        if not selected_symptoms:
            flash('Please select at least one symptom.', 'error')
            return redirect(url_for('index'))
        
        logging.debug(f"Selected symptoms: {selected_symptoms}")
        
        # Predict disease
        predicted_disease, confidence = predictor.predict_disease(selected_symptoms)
        
        if predicted_disease is None:
            flash('Unable to make a prediction. Please try again.', 'error')
            return redirect(url_for('index'))
        
        # Get disease information
        disease_info = predictor.get_disease_info(predicted_disease)
        
        # Convert selected symptoms to readable format
        readable_selected = [symptom.replace('_', ' ').title() for symptom in selected_symptoms]
        
        return render_template('results.html', 
                             predicted_disease=predicted_disease,
                             confidence=confidence,
                             selected_symptoms=readable_selected,
                             disease_info=disease_info)
        
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        flash('An error occurred during prediction. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/about')
def about():
    """About page with medical disclaimer"""
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logging.error(f"Internal error: {error}")
    return render_template('500.html'), 500
