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
            model = load_bin(file_path=model_path)
            preprocessor = load_bin(file_path=preprocessor_path)
            
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
                 writing_score: int):
        
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            logger.error(f"Error creating dataframe: {str(e)}")
            raise e
