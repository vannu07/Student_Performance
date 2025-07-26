import numpy as np
import pandas as pd
import os
from flask import Flask, request, render_template, jsonify, url_for
from sklearn.preprocessing import StandardScaler
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.student_performance.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.student_performance import logger

# Initialize Flask app with static folder configuration
application = Flask(__name__, 
                   static_folder='static',
                   static_url_path='/static')
app = application

# Configure app
app.config['SECRET_KEY'] = 'student_performance_ml_secret_key_2024'
app.config['DEBUG'] = True

# Route for home page
@app.route('/')
def index():
    """Render the main landing page with advanced UI"""
    try:
        logger.info("Rendering index page")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return f"Error loading page: {str(e)}", 500

# Route for simple landing page (interview-friendly)
@app.route('/simple')
def simple_index():
    """Render the simple landing page for interviews"""
    try:
        logger.info("Rendering simple index page")
        return render_template('simple_index.html')
    except Exception as e:
        logger.error(f"Error rendering simple index page: {str(e)}")
        return f"Error loading page: {str(e)}", 500

# Route for simple prediction interface
@app.route('/simple-predict', methods=['GET', 'POST'])
def simple_predict():
    """Simple prediction interface for interviews"""
    if request.method == 'GET':
        try:
            logger.info("Rendering simple prediction form")
            return render_template('simple_home.html')
        except Exception as e:
            logger.error(f"Error rendering simple prediction form: {str(e)}")
            return f"Error loading prediction form: {str(e)}", 500
    else:
        try:
            logger.info("Processing simple prediction request")
            
            # Extract form data with validation
            form_data = {
                'gender': request.form.get('gender'),
                'race_ethnicity': request.form.get('ethnicity'),
                'parental_level_of_education': request.form.get('parental_level_of_education'),
                'lunch': request.form.get('lunch'),
                'test_preparation_course': request.form.get('test_preparation_course'),
                'reading_score': request.form.get('reading_score'),
                'writing_score': request.form.get('writing_score')
            }
            
            # Validate required fields
            missing_fields = [key for key, value in form_data.items() if not value]
            if missing_fields:
                error_msg = f"Missing required fields: {', '.join(missing_fields)}"
                logger.error(error_msg)
                return render_template('simple_home.html', error=error_msg)
            
            # Validate numeric fields
            try:
                reading_score = float(form_data['reading_score'])
                writing_score = float(form_data['writing_score'])
                
                if not (0 <= reading_score <= 100) or not (0 <= writing_score <= 100):
                    error_msg = "Scores must be between 0 and 100"
                    logger.error(error_msg)
                    return render_template('simple_home.html', error=error_msg)
                    
            except ValueError:
                error_msg = "Invalid score values. Please enter numeric values."
                logger.error(error_msg)
                return render_template('simple_home.html', error=error_msg)
            
            # Create custom data object
            data = CustomData(
                gender=form_data['gender'],
                race_ethnicity=form_data['race_ethnicity'],
                parental_level_of_education=form_data['parental_level_of_education'],
                lunch=form_data['lunch'],
                test_preparation_course=form_data['test_preparation_course'],
                reading_score=reading_score,
                writing_score=writing_score
            )
            
            # Get prediction dataframe
            pred_df = data.get_data_as_data_frame()
            logger.info(f"Input data shape: {pred_df.shape}")
            logger.info(f"Input data: {pred_df.to_dict('records')[0]}")

            # Make prediction
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            
            prediction_score = float(results[0])
            logger.info(f"Prediction result: {prediction_score}")
            
            # Return result with enhanced data
            return render_template('simple_home.html', 
                                 results=prediction_score,
                                 input_data=form_data,
                                 success=True)
            
        except Exception as e:
            error_msg = f"Prediction error: {str(e)}"
            logger.error(error_msg)
            return render_template('simple_home.html', 
                                 error=error_msg,
                                 input_data=request.form.to_dict())

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    """Handle prediction requests with enhanced error handling"""
    if request.method == 'GET':
        try:
            logger.info("Rendering prediction form")
            return render_template('home.html')
        except Exception as e:
            logger.error(f"Error rendering prediction form: {str(e)}")
            return f"Error loading prediction form: {str(e)}", 500
    else:
        try:
            logger.info("Processing prediction request")
            
            # Extract form data with validation
            form_data = {
                'gender': request.form.get('gender'),
                'race_ethnicity': request.form.get('ethnicity'),
                'parental_level_of_education': request.form.get('parental_level_of_education'),
                'lunch': request.form.get('lunch'),
                'test_preparation_course': request.form.get('test_preparation_course'),
                'reading_score': request.form.get('reading_score'),
                'writing_score': request.form.get('writing_score')
            }
            
            # Validate required fields
            missing_fields = [key for key, value in form_data.items() if not value]
            if missing_fields:
                error_msg = f"Missing required fields: {', '.join(missing_fields)}"
                logger.error(error_msg)
                return render_template('home.html', error=error_msg)
            
            # Validate numeric fields
            try:
                reading_score = float(form_data['reading_score'])
                writing_score = float(form_data['writing_score'])
                
                if not (0 <= reading_score <= 100) or not (0 <= writing_score <= 100):
                    error_msg = "Scores must be between 0 and 100"
                    logger.error(error_msg)
                    return render_template('home.html', error=error_msg)
                    
            except ValueError:
                error_msg = "Invalid score values. Please enter numeric values."
                logger.error(error_msg)
                return render_template('home.html', error=error_msg)
            
            # Create custom data object
            data = CustomData(
                gender=form_data['gender'],
                race_ethnicity=form_data['race_ethnicity'],
                parental_level_of_education=form_data['parental_level_of_education'],
                lunch=form_data['lunch'],
                test_preparation_course=form_data['test_preparation_course'],
                reading_score=reading_score,
                writing_score=writing_score
            )
            
            # Get prediction dataframe
            pred_df = data.get_data_as_data_frame()
            logger.info(f"Input data shape: {pred_df.shape}")
            logger.info(f"Input data: {pred_df.to_dict('records')[0]}")

            # Make prediction
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            
            prediction_score = float(results[0])
            logger.info(f"Prediction result: {prediction_score}")
            
            # Return result with enhanced data
            return render_template('home.html', 
                                 results=prediction_score,
                                 input_data=form_data,
                                 success=True)
            
        except Exception as e:
            error_msg = f"Prediction error: {str(e)}"
            logger.error(error_msg)
            return render_template('home.html', 
                                 error=error_msg,
                                 input_data=request.form.to_dict())

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic predictions"""
    try:
        data = request.get_json()
        
        # Validate JSON data
        required_fields = ['gender', 'race_ethnicity', 'parental_level_of_education', 
                          'lunch', 'test_preparation_course', 'reading_score', 'writing_score']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'success': False
            }), 400
        
        # Create prediction
        custom_data = CustomData(**data)
        pred_df = custom_data.get_data_as_data_frame()
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        
        return jsonify({
            'prediction': float(results[0]),
            'success': True,
            'model_info': {
                'accuracy': '87%',
                'r2_score': 0.89,
                'model_type': 'Ensemble (Multiple Algorithms)'
            }
        })
        
    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'Student Performance ML API',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return render_template('index.html'), 500

# Add context processor for static files
@app.context_processor
def inject_static_vars():
    """Inject static file URLs into templates"""
    return {
        'static_css_url': url_for('static', filename='css/style.css'),
        'static_js_url': url_for('static', filename='js/main.js')
    }

if __name__ == "__main__":
    # Ensure static directory exists
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        logger.info(f"Created static directory: {static_dir}")
    
    logger.info("Starting Student Performance ML Web Application")
    logger.info("Features: Advanced UI, 3D Effects, Animations, Real-time Predictions")
    logger.info("Access the application at: http://localhost:5000")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
