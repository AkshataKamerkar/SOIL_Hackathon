"""
Unified Feature Engineering for Both Models
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List


class FeatureEngineer:
    """Handles feature engineering for predictions"""
    
    @staticmethod
    def engineer_classification_features(df: pd.DataFrame) -> pd.DataFrame:
        """Apply feature engineering for classification model"""
        df = df.copy()
        
        # Interaction features
        df['HDI_GDP_interaction'] = df['HDI_Index'] * df['GDP_per_Capita_USD'] / 10000
        df['Life_Literacy_interaction'] = df['Life_Expectancy_years'] * df['Literacy_Rate_pct'] / 100
        
        # Composite indices
        df['Economic_Health'] = (
            (df['GDP_per_Capita_USD'] / 65000) * 
            (1 - df['Unemployment_Rate_pct'] / 100)
        )
        df['Social_Development'] = (
            df['Literacy_Rate_pct'] + 
            df['Internet_Access_pct'] + 
            df['Higher_Education_Rate']
        ) / 3
        df['Stability_Index'] = (
            (100 - df['Unemployment_Rate_pct']) * 
            (365 - df['Days_engaged_in_warfare_per_year']) / 365
        )
        df['Healthcare_Quality'] = df['Life_Expectancy_years'] * df['Medical_Doctors_per_1000']
        df['Innovation_Score'] = (
            df['R_and_D_Expenditure_pct_GDP'] + 
            df['Number_of_Startups'] / 5000 * 10
        ) / 2
        df['Trade_Openness'] = df['Trade_Partners_Count'] / (
            df['Import_Rank_Global'] + df['Export_Rank_Global'] + 1
        )
        df['Wellbeing_Score'] = df['HDI_Index'] * df['Life_Expectancy_years'] / 80
        df['Education_Quality'] = df['Literacy_Rate_pct'] * df['Higher_Education_Rate'] / 100
        df['Digital_Progress'] = df['Internet_Access_pct'] * df['Number_of_Patents'] / 50001
        df['Economic_Stability'] = df['GDP_per_Capita_USD'] / (df['Unemployment_Rate_pct'] + 1)
        df['Peace_Index'] = (
            (365 - df['Days_engaged_in_warfare_per_year']) / 365 * 
            (1 - df['Defence_expenditure_on_GDP'] / 10)
        )
        df['Human_Capital'] = df['Number_of_PhD_holders_per_million'] * df['Literacy_Rate_pct'] / 100
        df['Gender_Development'] = df['Gender_Equality_Index'] * df['Higher_Education_Rate']
        df['Migration_Balance'] = df['Immigration_Rate'] - df['Migration_Rate']
        
        return df
    
    @staticmethod
    def engineer_regression_features(df: pd.DataFrame) -> pd.DataFrame:
        """Apply feature engineering for regression model"""
        df = df.copy()
        
        # Log transformations
        if 'Population' in df.columns:
            df['Population_log'] = np.log1p(df['Population'])
        if 'GDP_per_Capita_USD' in df.columns:
            df['GDP_per_Capita_USD_log'] = np.log1p(df['GDP_per_Capita_USD'])
        if 'Olympic_Medals_Count' in df.columns:
            df['Olympic_Medals_Count_log'] = np.log1p(df['Olympic_Medals_Count'])
        if 'Carbon_Footprint' in df.columns:
            df['Carbon_Footprint_log'] = np.log1p(df['Carbon_Footprint'])
        
        # Computed indices
        df['Peace_Index'] = (
            365 - df.get('Days_engaged_in_warfare_per_year', 0)
        ) / 365
        df['Is_Conflict_Free'] = (
            df.get('Days_engaged_in_warfare_per_year', 0) == 0
        ).astype(int)
        df['Digital_Index'] = df.get('Internet_Access_pct', 50) / 100
        df['Healthcare_Index'] = (
            df.get('Life_Expectancy_years', 70) - 40
        ) / 50
        df['Medical_Doctors_norm'] = df.get('Medical_Doctors_per_1000', 2) / 5
        df['Gender_Index'] = df.get('Gender_Equality_Index', 50) / 100
        df['Trade_Openness'] = df.get('Trade_Partners_Count', 100) / 250
        df['Innovation_Index'] = (
            df.get('R_and_D_Expenditure_pct_GDP', 1) + 
            df.get('Number_of_Patents', 1000) / 100000
        ) / 2
        df['Happiness_Norm'] = df.get('Happiness_Index_Ordinal', 5) / 8
        
        return df
    
    @staticmethod
    def prepare_input(
        input_data: Dict[str, Any], 
        required_features: List[str], 
        model_type: str
    ) -> pd.DataFrame:
        """
        Prepare input data for prediction
        
        Args:
            input_data: Dictionary of input values
            required_features: List of features required by model
            model_type: 'classification' or 'regression'
        
        Returns:
            DataFrame ready for prediction
        """
        df = pd.DataFrame([input_data])
        
        # Apply appropriate feature engineering
        if model_type == 'classification':
            df = FeatureEngineer.engineer_classification_features(df)
        else:
            df = FeatureEngineer.engineer_regression_features(df)
        
        # Ensure all required features exist
        for feat in required_features:
            if feat not in df.columns:
                df[feat] = 0
        
        # Select and order features
        df = df[required_features]
        
        # Handle any NaN or inf values
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)
        
        return df