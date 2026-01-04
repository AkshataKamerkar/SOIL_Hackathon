"""
Reusable Input Form Components
"""
import streamlit as st
from typing import Dict, Any, List
from app.config import config


class InputFormBuilder:
    """Builder for creating input forms"""
    
    def __init__(self, prefix: str = ""):
        self.values = {}
        self.prefix = prefix
    
    def add_slider(
        self, 
        key: str, 
        label: str, 
        help_text: str = None,
        feature_key: str = None
    ):
        """Add a slider input based on config"""
        feature_key = feature_key or key
        feat_config = config.FEATURE_RANGES.get(feature_key, {})
        
        self.values[key] = st.slider(
            label=label,
            min_value=feat_config.get('min', 0),
            max_value=feat_config.get('max', 100),
            value=feat_config.get('default', 50),
            step=feat_config.get('step', 1),
            help=help_text,
            key=f"{self.prefix}_{key}"
        )
        return self
    
    def add_number_input(
        self, 
        key: str, 
        label: str, 
        help_text: str = None,
        feature_key: str = None
    ):
        """Add a number input based on config"""
        feature_key = feature_key or key
        feat_config = config.FEATURE_RANGES.get(feature_key, {})
        
        self.values[key] = st.number_input(
            label=label,
            min_value=float(feat_config.get('min', 0)),
            max_value=float(feat_config.get('max', 100000)),
            value=float(feat_config.get('default', 0)),
            step=float(feat_config.get('step', 1)),
            help=help_text,
            key=f"{self.prefix}_{key}"
        )
        return self
    
    def get_values(self) -> Dict[str, Any]:
        """Get all collected values"""
        return self.values


def create_hdi_input_form() -> Dict[str, Any]:
    """Create input form for HDI prediction with ALL required features"""
    st.subheader("📝 Enter Country Indicators")
    
    # Create tabs for organized inputs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Economic", "🏥 Health & Social", "🎓 Education", "🌐 Technology & Trade", "📊 Other"
    ])
    
    inputs = {}
    
    # ==================== ECONOMIC TAB ====================
    with tab1:
        st.markdown("#### 💰 Economic Indicators")
        col1, col2 = st.columns(2)
        
        with col1:
            inputs['Population'] = st.number_input(
                "Population",
                min_value=100000,
                max_value=1500000000,
                value=50000000,
                step=1000000,
                help="Total population of the country",
                key="hdi_population"
            )
            inputs['GDP_per_Capita_USD'] = st.number_input(
                "GDP per Capita (USD)",
                min_value=500,
                max_value=150000,
                value=25000,
                step=500,
                help="Gross Domestic Product per person in US Dollars",
                key="hdi_gdp"
            )
            inputs['Unemployment_Rate_pct'] = st.slider(
                "Unemployment Rate (%)",
                min_value=0.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
                help="Percentage of labor force that is unemployed",
                key="hdi_unemployment"
            )
        
        with col2:
            inputs['Trade_Partners_Count'] = st.number_input(
                "Number of Trade Partners",
                min_value=0,
                max_value=250,
                value=100,
                step=5,
                help="Number of countries with trade agreements",
                key="hdi_trade_partners"
            )
            inputs['Import_Rank_Global'] = st.number_input(
                "Import Rank (Global)",
                min_value=1,
                max_value=200,
                value=50,
                step=1,
                help="Country's rank in global imports",
                key="hdi_import_rank"
            )
            inputs['Export_Rank_Global'] = st.number_input(
                "Export Rank (Global)",
                min_value=1,
                max_value=200,
                value=50,
                step=1,
                help="Country's rank in global exports",
                key="hdi_export_rank"
            )
    
    # ==================== HEALTH & SOCIAL TAB ====================
    with tab2:
        st.markdown("#### 🏥 Health & Social Indicators")
        col1, col2 = st.columns(2)
        
        with col1:
            inputs['Life_Expectancy_years'] = st.slider(
                "Life Expectancy (Years)",
                min_value=40.0,
                max_value=90.0,
                value=75.0,
                step=0.5,
                help="Average life expectancy at birth",
                key="hdi_life_exp"
            )
            inputs['Medical_Doctors_per_1000'] = st.slider(
                "Medical Doctors (per 1,000)",
                min_value=0.0,
                max_value=10.0,
                value=2.5,
                step=0.1,
                help="Number of doctors per 1,000 people",
                key="hdi_doctors"
            )
            inputs['Gender_Equality_Index'] = st.slider(
                "Gender Equality Index",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=1.0,
                help="Index measuring gender equality (0-100)",
                key="hdi_gender_eq"
            )
        
        with col2:
            inputs['Days_engaged_in_warfare_per_year'] = st.slider(
                "Days in Conflict (per year)",
                min_value=0,
                max_value=365,
                value=0,
                step=1,
                help="Number of days engaged in warfare",
                key="hdi_conflict_days"
            )
            inputs['Immigration_Rate'] = st.slider(
                "Immigration Rate",
                min_value=0.0,
                max_value=30.0,
                value=3.0,
                step=0.5,
                help="Rate of immigration into the country",
                key="hdi_immigration"
            )
            inputs['Migration_Rate'] = st.slider(
                "Migration Rate",
                min_value=-10.0,
                max_value=30.0,
                value=2.0,
                step=0.5,
                help="Net migration rate",
                key="hdi_migration"
            )
    
    # ==================== EDUCATION TAB ====================
    with tab3:
        st.markdown("#### 🎓 Education Indicators")
        col1, col2 = st.columns(2)
        
        with col1:
            inputs['Literacy_Rate_pct'] = st.slider(
                "Literacy Rate (%)",
                min_value=20.0,
                max_value=100.0,
                value=85.0,
                step=1.0,
                help="Percentage of population that can read and write",
                key="hdi_literacy"
            )
            inputs['Higher_Education_Rate'] = st.slider(
                "Higher Education Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=40.0,
                step=1.0,
                help="Percentage with higher education",
                key="hdi_higher_ed"
            )
        
        with col2:
            inputs['Number_of_PhD_holders_per_million'] = st.number_input(
                "PhD Holders (per million)",
                min_value=0,
                max_value=1500,
                value=200,
                step=10,
                help="Number of PhD holders per million people",
                key="hdi_phd"
            )
            inputs['Govt_Education_Expenditure_pct_GDP'] = st.slider(
                "Education Expenditure (% of GDP)",
                min_value=0.0,
                max_value=15.0,
                value=5.0,
                step=0.1,
                help="Government spending on education as % of GDP",
                key="hdi_edu_exp"
            )
    
    # ==================== TECHNOLOGY & TRADE TAB ====================
    with tab4:
        st.markdown("#### 🌐 Technology & Innovation")
        col1, col2 = st.columns(2)
        
        with col1:
            inputs['Internet_Access_pct'] = st.slider(
                "Internet Access (%)",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=1.0,
                help="Percentage of population with internet access",
                key="hdi_internet"
            )
            inputs['Number_of_Patents'] = st.number_input(
                "Number of Patents",
                min_value=0,
                max_value=200000,
                value=10000,
                step=100,
                help="Total patents registered",
                key="hdi_patents"
            )
            inputs['Number_of_Startups'] = st.number_input(
                "Number of Startups",
                min_value=0,
                max_value=100000,
                value=5000,
                step=100,
                help="Number of startup companies",
                key="hdi_startups"
            )
        
        with col2:
            inputs['R_and_D_Expenditure_pct_GDP'] = st.slider(
                "R&D Expenditure (% of GDP)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.1,
                help="Research & Development spending as % of GDP",
                key="hdi_rnd"
            )
            inputs['Space_Tech_Level_Ordinal'] = st.selectbox(
                "Space Technology Level",
                options=[0, 1, 2, 3, 4],
                index=2,
                format_func=lambda x: {
                    0: "None",
                    1: "Basic",
                    2: "Intermediate", 
                    3: "Advanced",
                    4: "Leading"
                }[x],
                help="Level of space technology capability",
                key="hdi_space_tech"
            )
    
    # ==================== OTHER TAB ====================
    with tab5:
        st.markdown("#### 📊 Other Indicators")
        col1, col2 = st.columns(2)
        
        with col1:
            inputs['Carbon_Footprint'] = st.slider(
                "Carbon Footprint (tons per capita)",
                min_value=0.0,
                max_value=25.0,
                value=5.0,
                step=0.1,
                help="CO2 emissions per capita in metric tons",
                key="hdi_carbon"
            )
            inputs['Defence_expenditure_on_GDP'] = st.slider(
                "Defence Expenditure (% of GDP)",
                min_value=0.0,
                max_value=15.0,
                value=2.0,
                step=0.1,
                help="Military spending as % of GDP",
                key="hdi_defence"
            )
            inputs['Nuclear_Power_Status'] = st.selectbox(
                "Nuclear Power Status",
                options=[0, 1],
                index=0,
                format_func=lambda x: "No" if x == 0 else "Yes",
                help="Does the country have nuclear power?",
                key="hdi_nuclear"
            )
        
        with col2:
            inputs['Olympic_Medals_Count'] = st.number_input(
                "Olympic Medals Count",
                min_value=0,
                max_value=3000,
                value=50,
                step=5,
                help="Total Olympic medals won historically",
                key="hdi_olympics"
            )
            inputs['Number_of_Religion'] = st.slider(
                "Number of Major Religions",
                min_value=1,
                max_value=10,
                value=4,
                step=1,
                help="Number of major religions practiced",
                key="hdi_religion"
            )
            inputs['Regulation_Strictness_Ordinal'] = st.selectbox(
                "Regulation Strictness",
                options=[1, 2, 3, 4, 5],
                index=2,
                format_func=lambda x: {
                    1: "Very Low",
                    2: "Low",
                    3: "Moderate",
                    4: "High",
                    5: "Very High"
                }[x],
                help="Level of government regulation",
                key="hdi_regulation"
            )
        
        # Happiness Index (needed for regression)
        inputs['Happiness_Index_Ordinal'] = st.slider(
            "Current Happiness Index (1-8)",
            min_value=1,
            max_value=8,
            value=5,
            step=1,
            help="Current happiness level (used as input for HDI prediction)",
            key="hdi_happiness_input"
        )
    
    return inputs


def create_happiness_input_form() -> Dict[str, Any]:
    """Create input form for Happiness classification with ALL required features"""
    st.subheader("📝 Enter Country Indicators")
    
    inputs = {}
    
    # ==================== CORE INDICATORS ====================
    st.markdown("### 📊 Core Indicators")
    col1, col2 = st.columns(2)
    
    with col1:
        inputs['HDI_Index'] = st.slider(
            "HDI Index",
            min_value=0.0,
            max_value=1.0,
            value=0.75,
            step=0.01,
            help="Human Development Index (0-1)",
            key="happy_hdi"
        )
        inputs['GDP_per_Capita_USD'] = st.number_input(
            "GDP per Capita (USD)",
            min_value=500,
            max_value=150000,
            value=25000,
            step=500,
            help="Gross Domestic Product per person",
            key="happy_gdp"
        )
        inputs['Life_Expectancy_years'] = st.slider(
            "Life Expectancy (Years)",
            min_value=40.0,
            max_value=90.0,
            value=75.0,
            step=0.5,
            help="Average life expectancy at birth",
            key="happy_life_exp"
        )
    
    with col2:
        inputs['Literacy_Rate_pct'] = st.slider(
            "Literacy Rate (%)",
            min_value=20.0,
            max_value=100.0,
            value=85.0,
            step=1.0,
            help="Percentage who can read and write",
            key="happy_literacy"
        )
        inputs['Internet_Access_pct'] = st.slider(
            "Internet Access (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0,
            help="Percentage with internet access",
            key="happy_internet"
        )
        inputs['Gender_Equality_Index'] = st.slider(
            "Gender Equality Index",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0,
            help="Index measuring gender equality",
            key="happy_gender_eq"
        )
    
    # ==================== ADVANCED INDICATORS ====================
    with st.expander("🔧 Advanced Indicators", expanded=False):
        
        st.markdown("#### 💼 Economic & Employment")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Unemployment_Rate_pct'] = st.slider(
                "Unemployment (%)",
                min_value=0.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
                key="happy_unemployment"
            )
            inputs['Trade_Partners_Count'] = st.number_input(
                "Trade Partners",
                min_value=0,
                max_value=250,
                value=100,
                step=5,
                key="happy_trade_partners"
            )
        
        with col2:
            inputs['Import_Rank_Global'] = st.number_input(
                "Import Rank",
                min_value=1,
                max_value=200,
                value=50,
                step=1,
                key="happy_import_rank"
            )
            inputs['Export_Rank_Global'] = st.number_input(
                "Export Rank",
                min_value=1,
                max_value=200,
                value=50,
                step=1,
                key="happy_export_rank"
            )
        
        with col3:
            inputs['Defence_expenditure_on_GDP'] = st.slider(
                "Defence (% GDP)",
                min_value=0.0,
                max_value=15.0,
                value=2.0,
                step=0.1,
                key="happy_defence"
            )
            inputs['Days_engaged_in_warfare_per_year'] = st.slider(
                "Conflict Days/Year",
                min_value=0,
                max_value=365,
                value=0,
                step=1,
                key="happy_conflict"
            )
        
        st.markdown("#### 🎓 Education & Research")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Higher_Education_Rate'] = st.slider(
                "Higher Education (%)",
                min_value=0.0,
                max_value=100.0,
                value=40.0,
                step=1.0,
                key="happy_higher_ed"
            )
        
        with col2:
            inputs['Number_of_PhD_holders_per_million'] = st.number_input(
                "PhD Holders (per million)",
                min_value=0,
                max_value=1500,
                value=200,
                step=10,
                key="happy_phd"
            )
        
        with col3:
            inputs['R_and_D_Expenditure_pct_GDP'] = st.slider(
                "R&D (% GDP)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.1,
                key="happy_rnd"
            )
        
        st.markdown("#### 🏥 Health & Innovation")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Medical_Doctors_per_1000'] = st.slider(
                "Doctors per 1000",
                min_value=0.0,
                max_value=10.0,
                value=2.5,
                step=0.1,
                key="happy_doctors"
            )
        
        with col2:
            inputs['Number_of_Startups'] = st.number_input(
                "Startups",
                min_value=0,
                max_value=100000,
                value=5000,
                step=100,
                key="happy_startups"
            )
        
        with col3:
            inputs['Number_of_Patents'] = st.number_input(
                "Patents",
                min_value=0,
                max_value=200000,
                value=10000,
                step=100,
                key="happy_patents"
            )
        
        st.markdown("#### 🌍 Migration")
        col1, col2 = st.columns(2)
        
        with col1:
            inputs['Immigration_Rate'] = st.slider(
                "Immigration Rate",
                min_value=0.0,
                max_value=30.0,
                value=3.0,
                step=0.5,
                key="happy_immigration"
            )
        
        with col2:
            inputs['Migration_Rate'] = st.slider(
                "Migration Rate",
                min_value=-10.0,
                max_value=30.0,
                value=2.0,
                step=0.5,
                key="happy_migration"
            )
    
    return inputs