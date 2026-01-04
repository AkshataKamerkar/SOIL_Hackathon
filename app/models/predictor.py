"""
Unified Prediction Interface
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from dataclasses import dataclass

from app.models.model_loader import LoadedModel
from app.models.feature_engineering import FeatureEngineer
from app.config import config


@dataclass
class PredictionResult:
    """Container for prediction results"""
    value: float
    category: str
    confidence: float = None
    probabilities: Dict[str, float] = None
    interpretation: str = None


class Predictor:
    """Unified prediction interface for all models"""
    
    def __init__(self, model: LoadedModel, model_type: str):
        self.model = model
        self.model_type = model_type
    
    def predict(self, input_data: Dict[str, Any]) -> PredictionResult:
        """
        Make prediction based on model type
        
        Args:
            input_data: Dictionary of input feature values
            
        Returns:
            PredictionResult with value, category, and confidence
        """
        if self.model_type == 'classification':
            return self._predict_classification(input_data)
        else:
            return self._predict_regression(input_data)
    
    def _predict_classification(self, input_data: Dict[str, Any]) -> PredictionResult:
        """Predict happiness index classification"""
        # Prepare input
        X = FeatureEngineer.prepare_input(
            input_data, 
            self.model.feature_names, 
            'classification'
        )
        
        # Scale features
        X_scaled = self.model.scaler.transform(X)
        
        # Predict
        pred = self.model.model.predict(X_scaled)[0]
        proba = self.model.model.predict_proba(X_scaled)[0]
        
        # Get class label
        class_label = self.model.label_encoder.inverse_transform([pred])[0]
        confidence = float(max(proba))
        
        # Create probability dictionary
        classes = self.model.label_encoder.classes_
        probabilities = {
            f"Level {int(c)}": float(p) 
            for c, p in zip(classes, proba)
        }
        
        # Get interpretation
        interpretation = self._get_happiness_interpretation(int(class_label))
        
        return PredictionResult(
            value=int(class_label),
            category=config.HAPPINESS_LEVELS.get(int(class_label), "Unknown"),
            confidence=confidence,
            probabilities=probabilities,
            interpretation=interpretation
        )
    
    def _predict_regression(self, input_data: Dict[str, Any]) -> PredictionResult:
        """Predict HDI value"""
        # Prepare input
        X = FeatureEngineer.prepare_input(
            input_data, 
            self.model.feature_names, 
            'regression'
        )
        
        # Predict
        pred = self.model.model.predict(X)[0]
        pred = np.clip(pred, 0, 1)  # Ensure valid HDI range
        
        # Categorize
        category = self._categorize_hdi(pred)
        
        # Get interpretation
        interpretation = self._get_hdi_interpretation(pred, category)
        
        return PredictionResult(
            value=float(pred),
            category=category,
            confidence=None,  # Regression doesn't have confidence
            interpretation=interpretation
        )
    
    @staticmethod
    def _categorize_hdi(hdi_value: float) -> str:
        """Categorize HDI value"""
        for category, (low, high) in config.HDI_THRESHOLDS.items():
            if low <= hdi_value <= high:
                return category
        return "Unknown"
    
    @staticmethod
    def _get_hdi_interpretation(value: float, category: str) -> str:
        """Generate interpretation for HDI prediction"""
        interpretations = {
            "Very High": f"With an HDI of {value:.3f}, this represents very high human development. "
                        "Countries at this level typically have excellent healthcare, education, and living standards.",
            "High": f"An HDI of {value:.3f} indicates high human development. "
                   "There's good access to education and healthcare with a decent standard of living.",
            "Medium": f"An HDI of {value:.3f} suggests medium human development. "
                     "There are opportunities for growth in education, healthcare, and economic development.",
            "Low": f"An HDI of {value:.3f} indicates low human development. "
                  "Significant investments in education, healthcare, and economic development are needed."
        }
        return interpretations.get(category, "")
    
    @staticmethod
    def _get_happiness_interpretation(level: int) -> str:
        """Generate interpretation for happiness prediction"""
        if level >= 7:
            return "Excellent happiness levels indicating strong social support, economic stability, and quality of life."
        elif level >= 5:
            return "Above average happiness with good overall well-being indicators."
        elif level >= 3:
            return "Moderate happiness levels with room for improvement in various areas."
        else:
            return "Lower happiness levels suggesting challenges in economic, social, or political factors."