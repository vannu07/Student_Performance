import sys
import pandas as pd
from src.student_performance.utils.common import load_bin
from src.student_performance import logger

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = "artifacts/model_trainer/model.pkl"
            preprocessor_path = "artifacts/data_transformation/preprocessor.pkl"
            
            logger.info("Loading model and preprocessor")
            model = load_bin(path=model_path)
            preprocessor = load_bin(path=preprocessor_path)
            
            logger.info("Scaling input features")
            data_scaled = preprocessor.transform(features)
            
            logger.info("Making prediction")
            preds = model.predict(data_scaled)
            
            return preds
        
        except Exception as e:
            logger.error(f"Error in prediction pipeline: {str(e)}")
            raise e

class CustomData:
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education: str,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int,
                 # Optional parameters with defaults for missing features
                 part_time_job: str = "No",
                 absence_days: int = 0,
                 extracurricular_activities: str = "No",
                 weekly_self_study_hours: float = 10.0,
                 career_aspiration: str = "Engineer",
                 math_score: int = None,  # Will be predicted
                 history_score: int = 75,
                 physics_score: int = 75,
                 chemistry_score: int = 75,
                 biology_score: int = 75,
                 english_score: int = 75,
                 geography_score: int = 75):
        
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score
        
        # Set defaults for missing features
        self.part_time_job = part_time_job
        self.absence_days = absence_days
        self.extracurricular_activities = extracurricular_activities
        self.weekly_self_study_hours = weekly_self_study_hours
        self.career_aspiration = career_aspiration
        self.history_score = history_score
        self.physics_score = physics_score
        self.chemistry_score = chemistry_score
        self.biology_score = biology_score
        self.english_score = english_score
        self.geography_score = geography_score

    def get_data_as_data_frame(self):
        try:
            # Create dataframe with all required columns in the correct order
            custom_data_input_dict = {
                "gender": [self.gender],
                "part_time_job": [self.part_time_job],
                "absence_days": [self.absence_days],
                "extracurricular_activities": [self.extracurricular_activities],
                "weekly_self_study_hours": [self.weekly_self_study_hours],
                "career_aspiration": [self.career_aspiration],
                "history_score": [self.history_score],
                "physics_score": [self.physics_score],
                "chemistry_score": [self.chemistry_score],
                "biology_score": [self.biology_score],
                "english_score": [self.english_score],
                "geography_score": [self.geography_score],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "writing_score": [self.writing_score],
                "reading_score": [self.reading_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            logger.error(f"Error creating dataframe: {str(e)}")
            raise e
