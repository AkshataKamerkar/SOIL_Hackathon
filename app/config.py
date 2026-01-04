"""
Centralized Configuration Management
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any
from pathlib import Path
import os

@dataclass
class ModelConfig:
    """Model-specific configurations"""
    name: str
    path: Path
    version: str
    feature_names: List[str] = field(default_factory=list)

@dataclass
class AppConfig:
    """Application-wide configurations"""
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    MODELS_DIR: Path = BASE_DIR / "saved_models"
    DATA_DIR: Path = BASE_DIR / "data"
    ASSETS_DIR: Path = BASE_DIR / "app" / "assets"
    
    # App Settings
    APP_TITLE: str = "🌍 Global Development Predictor"
    APP_ICON: str = "🌍"
    APP_LAYOUT: str = "wide"
    
   # Premium Color Scheme
    PRIMARY_COLOR: str = "#6366f1"  # Indigo
    SECONDARY_COLOR: str = "#8b5cf6"  # Violet
    ACCENT_COLOR: str = "#ec4899"  # Pink
    SUCCESS_COLOR: str = "#10b981"  # Emerald
    WARNING_COLOR: str = "#f59e0b"  # Amber
    DANGER_COLOR: str = "#ef4444"  # Red
    
    # Theme Colors
    BACKGROUND_DARK: str = "#0a0a0f"
    BACKGROUND_CARD: str = "rgba(30, 41, 59, 0.7)"
    TEXT_PRIMARY: str = "#ffffff"
    TEXT_SECONDARY: str = "#94a3b8"
    BORDER_COLOR: str = "rgba(255, 255, 255, 0.1)"
    
    # HDI Thresholds
    HDI_THRESHOLDS: Dict[str, tuple] = field(default_factory=lambda: {
        "Very High": (0.800, 1.000),
        "High": (0.700, 0.799),
        "Medium": (0.550, 0.699),
        "Low": (0.000, 0.549)
    })
    
    # Happiness Levels
    HAPPINESS_LEVELS: Dict[int, str] = field(default_factory=lambda: {
        1: "Very Low", 2: "Low", 3: "Below Average",
        4: "Average", 5: "Above Average", 6: "High",
        7: "Very High", 8: "Excellent"
    })
    
    # Input Feature Ranges (for sliders/validation)
    FEATURE_RANGES: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "HDI_Index": {"min": 0.0, "max": 1.0, "step": 0.01, "default": 0.7},
        "GDP_per_Capita_USD": {"min": 500, "max": 100000, "step": 500, "default": 20000},
        "Life_Expectancy_years": {"min": 40, "max": 90, "step": 0.5, "default": 75},
        "Literacy_Rate_pct": {"min": 20, "max": 100, "step": 1, "default": 85},
        "Internet_Access_pct": {"min": 0, "max": 100, "step": 1, "default": 70},
        "Gender_Equality_Index": {"min": 0, "max": 100, "step": 1, "default": 70},
        "Unemployment_Rate_pct": {"min": 0, "max": 50, "step": 0.5, "default": 5},
        "Days_engaged_in_warfare_per_year": {"min": 0, "max": 365, "step": 1, "default": 0},
        "Higher_Education_Rate": {"min": 0, "max": 100, "step": 1, "default": 40},
        "Medical_Doctors_per_1000": {"min": 0, "max": 10, "step": 0.1, "default": 2.5},
        "R_and_D_Expenditure_pct_GDP": {"min": 0, "max": 10, "step": 0.1, "default": 2},
        "Number_of_Startups": {"min": 0, "max": 100000, "step": 100, "default": 5000},
        "Trade_Partners_Count": {"min": 0, "max": 250, "step": 5, "default": 100},
        "Import_Rank_Global": {"min": 1, "max": 200, "step": 1, "default": 50},
        "Export_Rank_Global": {"min": 1, "max": 200, "step": 1, "default": 50},
        "Number_of_Patents": {"min": 0, "max": 100000, "step": 100, "default": 10000},
        "Defence_expenditure_on_GDP": {"min": 0, "max": 15, "step": 0.1, "default": 2},
        "Number_of_PhD_holders_per_million": {"min": 0, "max": 1500, "step": 10, "default": 200},
        "Immigration_Rate": {"min": 0, "max": 30, "step": 0.5, "default": 3},
        "Migration_Rate": {"min": -10, "max": 30, "step": 0.5, "default": 2},
    })

# Singleton instance
config = AppConfig()