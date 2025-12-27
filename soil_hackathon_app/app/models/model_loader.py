"""
Model Loading and Management
"""
import streamlit as st
import joblib
import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LoadedModel:
    """Container for loaded model components"""
    model: Any
    scaler: Optional[Any] = None
    label_encoder: Optional[Any] = None
    feature_names: list = None
    metadata: dict = None


class ModelLoader:
    """Handles loading and caching of ML models"""
    
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir
        self._cache = {}
    
    @st.cache_resource
    def load_classification_model(_self) -> LoadedModel:
        """Load classification model with all components"""
        try:
            model_dir = _self.models_dir / "classification"
            
            model = joblib.load(model_dir / "model.joblib")
            scaler = joblib.load(model_dir / "scaler.joblib")
            label_encoder = joblib.load(model_dir / "label_encoder.joblib")
            
            with open(model_dir / "feature_names.json", 'r') as f:
                feature_names = json.load(f)
            
            metadata = {}
            metadata_path = model_dir / "model_info.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            
            logger.info("✅ Classification model loaded successfully")
            
            return LoadedModel(
                model=model,
                scaler=scaler,
                label_encoder=label_encoder,
                feature_names=feature_names,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"❌ Error loading classification model: {e}")
            raise
    
    @st.cache_resource
    def load_regression_model(_self) -> LoadedModel:
        """Load regression model"""
        try:
            model_path = _self.models_dir / "regression" / "hdi_model_v51.joblib"
            package = joblib.load(model_path)
            
            logger.info("✅ Regression model loaded successfully")
            
            return LoadedModel(
                model=package['model'],
                feature_names=package['feature_names'],
                metadata=package.get('metadata', {})
            )
        except Exception as e:
            logger.error(f"❌ Error loading regression model: {e}")
            raise