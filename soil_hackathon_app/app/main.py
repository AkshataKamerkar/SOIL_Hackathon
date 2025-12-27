"""
Main Streamlit Application
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Page config must be first Streamlit command
st.set_page_config(
    page_title="🌍 Global Development Predictor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .success-card {
        border-left-color: #28a745;
    }
    .warning-card {
        border-left-color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# IMPORTS FROM COMPONENTS
# ============================================================
from app.components.visualizations import (
    load_dataset,
    display_comprehensive_analysis,
    display_dataset_overview
)


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    """Render sidebar"""
    with st.sidebar:
        st.markdown("## 🌍 Navigation")
        st.markdown("---")
        
        st.markdown("### 📖 About")
        st.markdown("""
        This application predicts:
        - **HDI** (Human Development Index)
        - **Happiness Index**
        
        Using Machine Learning models.
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Model Status")
        
        # Check if models exist
        models_dir = Path("saved_models")
        
        clf_exists = (models_dir / "classification" / "model.joblib").exists()
        reg_exists = (models_dir / "regression" / "hdi_model_v51.joblib").exists()
        
        if clf_exists:
            st.success("✅ Classification Model")
        else:
            st.warning("⚠️ Classification Model Missing")
        
        if reg_exists:
            st.success("✅ Regression Model")
        else:
            st.warning("⚠️ Regression Model Missing")
        
        st.markdown("---")
        st.caption("v1.0.0 | Built with ❤️ by Team DATAGEEKS!")


# ============================================================
# LANDING PAGE
# ============================================================
# ============================================================
# LANDING PAGE - ENHANCED VERSION
# ============================================================
def render_landing_page():
    """Render landing page with dataset analysis"""
    st.markdown('<h1 class="main-header">🌍 Global Development Predictor</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Predict HDI & Happiness Index using Machine Learning</p>', 
                unsafe_allow_html=True)
    
    # Feature cards using Streamlit containers
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📈 HDI Prediction")
            st.markdown("Predict Human Development Index based on socioeconomic indicators.")
            st.markdown("---")
            st.markdown("**🔧 Model Type:** Regression")
            st.markdown("**📤 Output:** HDI Score (0-1)")
            st.markdown("**📊 Features:** 25+ indicators")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 😊 Happiness Classification")
            st.markdown("Classify happiness levels based on country indicators.")
            st.markdown("---")
            st.markdown("**🔧 Model Type:** Classification")
            st.markdown("**📤 Output:** Happiness Level (1-8)")
            st.markdown("**📊 Features:** 20+ indicators")
    
    st.markdown("---")
    
    # Quick reference
    st.markdown("## 📚 Quick Reference")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### HDI Categories")
        hdi_col1, hdi_col2 = st.columns(2)
        with hdi_col1:
            st.success("🏆 **Very High:** 0.800+")
            st.info("🌟 **High:** 0.700-0.799")
        with hdi_col2:
            st.warning("📊 **Medium:** 0.550-0.699")
            st.error("📉 **Low:** Below 0.550")
    
    with col2:
        st.markdown("### Happiness Levels")
        happy_col1, happy_col2 = st.columns(2)
        with happy_col1:
            st.success("🤗 **Level 7-8:** Excellent")
            st.info("😊 **Level 5-6:** High")
        with happy_col2:
            st.warning("😐 **Level 3-4:** Average")
            st.error("😔 **Level 1-2:** Low")
    
    st.markdown("---")
    
    # ==================== DATA ANALYSIS SECTION ====================
    st.markdown("## 📊 Dataset Analysis")
    
    # Initialize session state
    if 'show_data_analysis' not in st.session_state:
        st.session_state.show_data_analysis = False
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    # Button container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.show_data_analysis:
            # Show button to view analysis
            st.markdown("""
            <div style="
                background: #f0f2f6;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin: 10px 0;
            ">
                <p style="color: #333; margin-bottom: 15px;">
                    📈 Explore comprehensive analysis of the dataset including:
                </p>
                <p style="color: #666; font-size: 0.9em;">
                    • Distribution Charts • Correlation Matrix • Statistical Summary • Feature Relationships
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(
                "📊 View Data Analysis", 
                type="primary", 
                use_container_width=True,
                key="show_analysis_btn"
            ):
                st.session_state.show_data_analysis = True
                st.rerun()
        else:
            if st.button(
                "🔼 Hide Data Analysis", 
                type="secondary", 
                use_container_width=True,
                key="hide_analysis_btn"
            ):
                st.session_state.show_data_analysis = False
                st.session_state.data_loaded = False
                st.rerun()
    
    # Show data analysis
    if st.session_state.show_data_analysis:
        st.markdown("---")
        
        # Loading animation for first load
        if not st.session_state.data_loaded:
            with st.spinner("🔄 Loading dataset and generating visualizations..."):
                import time
                time.sleep(0.5)  # Brief pause for UX
                st.session_state.data_loaded = True
        
        df = load_dataset()
        
        if df is not None:
            # Quick stats at the top
            st.markdown("### 📈 Quick Stats")
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("Total Records", f"{len(df):,}")
            with stat_col2:
                st.metric("Features", f"{len(df.columns):,}")
            with stat_col3:
                if 'HDI_Index' in df.columns:
                    st.metric("Avg HDI", f"{df['HDI_Index'].mean():.3f}")
                else:
                    st.metric("Avg HDI", "N/A")
            with stat_col4:
                if 'GDP_per_Capita_USD' in df.columns:
                    st.metric("Avg GDP", f"${df['GDP_per_Capita_USD'].mean():,.0f}")
                else:
                    st.metric("Avg GDP", "N/A")
            
            st.markdown("---")
            
            # Full analysis
            display_comprehensive_analysis(df)
            
        else:
            st.warning("📁 No dataset found. Please add `sample_dataset.csv` to the `data/` folder.")
            
            uploaded_file = st.file_uploader(
                "Or upload a CSV file to analyze:",
                type=['csv'],
                key="landing_file_upload"
            )
            
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                display_comprehensive_analysis(df)

# ============================================================
# HDI PREDICTION PAGE - ALL FIELDS
# ============================================================

def render_hdi_page():
    """Render HDI prediction page with ALL required fields on single page"""
    st.markdown("## 📈 Human Development Index Prediction")
    st.markdown("Enter country indicators to predict the HDI score.")
    
    st.markdown("---")
    
    inputs = {}
    
    # ==================== CORE INDICATORS ====================
    st.markdown("### 📊 Core Indicators")
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
        inputs['Life_Expectancy_years'] = st.slider(
            "Life Expectancy (Years)",
            min_value=40.0,
            max_value=90.0,
            value=75.0,
            step=0.5,
            help="Average life expectancy at birth",
            key="hdi_life_exp"
        )
    
    with col2:
        inputs['Literacy_Rate_pct'] = st.slider(
            "Literacy Rate (%)",
            min_value=20.0,
            max_value=100.0,
            value=85.0,
            step=1.0,
            help="Percentage of population that can read and write",
            key="hdi_literacy"
        )
        inputs['Internet_Access_pct'] = st.slider(
            "Internet Access (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0,
            help="Percentage of population with internet access",
            key="hdi_internet"
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
    
    # ==================== ECONOMIC INDICATORS ====================
    with st.expander("💰 Economic & Trade Indicators", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Unemployment_Rate_pct'] = st.slider(
                "Unemployment Rate (%)",
                min_value=0.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
                help="Percentage of labor force that is unemployed",
                key="hdi_unemployment"
            )
            inputs['Trade_Partners_Count'] = st.number_input(
                "Trade Partners",
                min_value=0,
                max_value=250,
                value=100,
                step=5,
                help="Number of countries with trade agreements",
                key="hdi_trade_partners"
            )
        
        with col2:
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
        
        with col3:
            inputs['Defence_expenditure_on_GDP'] = st.slider(
                "Defence Expenditure (% GDP)",
                min_value=0.0,
                max_value=15.0,
                value=2.0,
                step=0.1,
                help="Military spending as % of GDP",
                key="hdi_defence"
            )
            inputs['Carbon_Footprint'] = st.slider(
                "Carbon Footprint (tons/capita)",
                min_value=0.0,
                max_value=25.0,
                value=5.0,
                step=0.1,
                help="CO2 emissions per capita in metric tons",
                key="hdi_carbon"
            )
    
    # ==================== HEALTH & SOCIAL INDICATORS ====================
    with st.expander("🏥 Health & Social Indicators", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Medical_Doctors_per_1000'] = st.slider(
                "Doctors per 1,000",
                min_value=0.0,
                max_value=10.0,
                value=2.5,
                step=0.1,
                help="Number of doctors per 1,000 people",
                key="hdi_doctors"
            )
            inputs['Days_engaged_in_warfare_per_year'] = st.slider(
                "Conflict Days/Year",
                min_value=0,
                max_value=365,
                value=0,
                step=1,
                help="Number of days engaged in warfare",
                key="hdi_conflict_days"
            )
        
        with col2:
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
        
        with col3:
            inputs['Number_of_Religion'] = st.slider(
                "Number of Major Religions",
                min_value=1,
                max_value=10,
                value=4,
                step=1,
                help="Number of major religions practiced",
                key="hdi_religion"
            )
            inputs['Olympic_Medals_Count'] = st.number_input(
                "Olympic Medals Count",
                min_value=0,
                max_value=3000,
                value=50,
                step=5,
                help="Total Olympic medals won historically",
                key="hdi_olympics"
            )
    
    # ==================== EDUCATION INDICATORS ====================
    with st.expander("🎓 Education & Research Indicators", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Higher_Education_Rate'] = st.slider(
                "Higher Education Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=40.0,
                step=1.0,
                help="Percentage with higher education",
                key="hdi_higher_ed"
            )
            inputs['Govt_Education_Expenditure_pct_GDP'] = st.slider(
                "Education Expenditure (% GDP)",
                min_value=0.0,
                max_value=15.0,
                value=5.0,
                step=0.1,
                help="Government spending on education as % of GDP",
                key="hdi_edu_exp"
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
            inputs['R_and_D_Expenditure_pct_GDP'] = st.slider(
                "R&D Expenditure (% GDP)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.1,
                help="Research & Development spending as % of GDP",
                key="hdi_rnd"
            )
        
        with col3:
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
    
    # ==================== OTHER INDICATORS ====================
    with st.expander("📊 Technology & Other Indicators", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Nuclear_Power_Status'] = st.selectbox(
                "Nuclear Power Status",
                options=[0, 1],
                index=0,
                format_func=lambda x: "No" if x == 0 else "Yes",
                help="Does the country have nuclear power?",
                key="hdi_nuclear"
            )
            inputs['Space_Tech_Level_Ordinal'] = st.selectbox(
                "Space Technology Level",
                options=[0, 1, 2, 3, 4],
                index=2,
                format_func=lambda x: ["None", "Basic", "Intermediate", "Advanced", "Leading"][x],
                help="Level of space technology capability",
                key="hdi_space_tech"
            )
        
        with col2:
            inputs['Regulation_Strictness_Ordinal'] = st.selectbox(
                "Regulation Strictness",
                options=[1, 2, 3, 4, 5],
                index=2,
                format_func=lambda x: ["", "Very Low", "Low", "Moderate", "High", "Very High"][x],
                help="Level of government regulation",
                key="hdi_regulation"
            )
            inputs['Happiness_Index_Ordinal'] = st.slider(
                "Current Happiness Index (1-8)",
                min_value=1,
                max_value=8,
                value=5,
                step=1,
                help="Current happiness level (used as input for HDI prediction)",
                key="hdi_happiness_input"
            )
        
        with col3:
            # Placeholder for alignment
            st.markdown("")
            st.markdown("")
            st.info("💡 These indicators help capture technology advancement and governance quality.")
    
    st.markdown("---")
    
    # Show summary of inputs
    with st.expander("📋 View All Input Values", expanded=False):
        # Create a nice formatted table
        col1, col2 = st.columns(2)
        
        input_items = list(inputs.items())
        mid_point = len(input_items) // 2
        
        with col1:
            st.markdown("**First Half:**")
            for key, value in input_items[:mid_point]:
                st.text(f"{key}: {value}")
        
        with col2:
            st.markdown("**Second Half:**")
            for key, value in input_items[mid_point:]:
                st.text(f"{key}: {value}")
        
        st.markdown("---")
        st.markdown(f"**Total Features:** {len(inputs)}")
    
    st.markdown("---")
    
    # Predict button
    if st.button("🔮 Predict HDI", type="primary", use_container_width=True, key="hdi_predict_btn"):
        with st.spinner("Calculating HDI prediction..."):
            import time
            time.sleep(1)
            
            # Mock prediction formula using more inputs
            mock_hdi = (
                (inputs['GDP_per_Capita_USD'] / 150000) * 0.18 +
                (inputs['Life_Expectancy_years'] / 90) * 0.18 +
                (inputs['Literacy_Rate_pct'] / 100) * 0.12 +
                (inputs['Higher_Education_Rate'] / 100) * 0.10 +
                (1 - inputs['Unemployment_Rate_pct'] / 50) * 0.08 +
                (inputs['Internet_Access_pct'] / 100) * 0.07 +
                (inputs['Medical_Doctors_per_1000'] / 10) * 0.06 +
                (inputs['Gender_Equality_Index'] / 100) * 0.05 +
                (1 - inputs['Days_engaged_in_warfare_per_year'] / 365) * 0.05 +
                (inputs['R_and_D_Expenditure_pct_GDP'] / 10) * 0.04 +
                (inputs['Trade_Partners_Count'] / 250) * 0.03 +
                (inputs['Govt_Education_Expenditure_pct_GDP'] / 15) * 0.02 +
                (inputs['Space_Tech_Level_Ordinal'] / 4) * 0.02
            )
            mock_hdi = min(max(mock_hdi, 0.25), 0.98)
            
            # Categorize
            if mock_hdi >= 0.8:
                category = "Very High"
                color = "#2E7D32"
                emoji = "🏆"
            elif mock_hdi >= 0.7:
                category = "High"
                color = "#689F38"
                emoji = "🌟"
            elif mock_hdi >= 0.55:
                category = "Medium"
                color = "#FFA000"
                emoji = "📊"
            else:
                category = "Low"
                color = "#D32F2F"
                emoji = "📉"
        
        # Display result
        st.markdown("---")
        st.markdown("## 🎯 Prediction Result")
        
        result_col1, result_col2, result_col3 = st.columns([1, 2, 1])
        
        with result_col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f5f5f5 0%, white 100%);
                border-left: 5px solid {color};
                border-radius: 10px;
                padding: 30px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <span style="font-size: 4em;">{emoji}</span>
                <h1 style="color: {color}; margin: 10px 0;">{mock_hdi:.3f}</h1>
                <span style="
                    background: {color};
                    color: white;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-weight: bold;
                ">{category} Human Development</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Interpretation
        interpretations = {
            "Very High": f"With an HDI of {mock_hdi:.3f}, this represents very high human development. Countries at this level typically have excellent healthcare, education, and living standards.",
            "High": f"An HDI of {mock_hdi:.3f} indicates high human development. There's good access to education and healthcare with a decent standard of living.",
            "Medium": f"An HDI of {mock_hdi:.3f} suggests medium human development. There are opportunities for growth in education, healthcare, and economic development.",
            "Low": f"An HDI of {mock_hdi:.3f} indicates low human development. Significant investments in education, healthcare, and economic development are needed."
        }
        
        st.info(f"💡 **Interpretation:** {interpretations[category]}")
        
        # Feature contribution chart
        st.markdown("### 📊 Feature Contributions")
        
        import plotly.graph_objects as go
        
        contributions = {
            'GDP per Capita': (inputs['GDP_per_Capita_USD'] / 150000) * 0.18,
            'Life Expectancy': (inputs['Life_Expectancy_years'] / 90) * 0.18,
            'Literacy Rate': (inputs['Literacy_Rate_pct'] / 100) * 0.12,
            'Higher Education': (inputs['Higher_Education_Rate'] / 100) * 0.10,
            'Employment': (1 - inputs['Unemployment_Rate_pct'] / 50) * 0.08,
            'Internet Access': (inputs['Internet_Access_pct'] / 100) * 0.07,
            'Healthcare': (inputs['Medical_Doctors_per_1000'] / 10) * 0.06,
            'Gender Equality': (inputs['Gender_Equality_Index'] / 100) * 0.05,
            'Peace Index': (1 - inputs['Days_engaged_in_warfare_per_year'] / 365) * 0.05,
            'R&D Investment': (inputs['R_and_D_Expenditure_pct_GDP'] / 10) * 0.04,
            'Trade Openness': (inputs['Trade_Partners_Count'] / 250) * 0.03,
            'Education Spending': (inputs['Govt_Education_Expenditure_pct_GDP'] / 15) * 0.02,
            'Space Technology': (inputs['Space_Tech_Level_Ordinal'] / 4) * 0.02,
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(contributions.values()),
                y=list(contributions.keys()),
                orientation='h',
                marker_color='#1f77b4',
                text=[f'{v:.3f}' for v in contributions.values()],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Contribution to HDI Score",
            xaxis_title="Contribution",
            yaxis_title="Feature",
            height=450,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("### 📋 Development Recommendations")
        
        recommendations = []
        
        if inputs['Literacy_Rate_pct'] < 80:
            recommendations.append("📚 **Education:** Improve literacy rates through expanded education programs")
        if inputs['Life_Expectancy_years'] < 70:
            recommendations.append("🏥 **Healthcare:** Invest in healthcare infrastructure to improve life expectancy")
        if inputs['Internet_Access_pct'] < 60:
            recommendations.append("🌐 **Digital:** Expand internet infrastructure for better connectivity")
        if inputs['Unemployment_Rate_pct'] > 10:
            recommendations.append("💼 **Employment:** Implement job creation programs to reduce unemployment")
        if inputs['Gender_Equality_Index'] < 60:
            recommendations.append("⚖️ **Equality:** Strengthen gender equality policies and programs")
        if inputs['Days_engaged_in_warfare_per_year'] > 0:
            recommendations.append("☮️ **Peace:** Prioritize conflict resolution and peacekeeping efforts")
        if inputs['R_and_D_Expenditure_pct_GDP'] < 1.5:
            recommendations.append("🔬 **Innovation:** Increase R&D investment for technological advancement")
        
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("✅ All key indicators are at healthy levels! Focus on maintaining current standards.")


# ============================================================
# HAPPINESS PREDICTION PAGE - ALL FIELDS
# ============================================================
def render_happiness_page():
    """Render happiness prediction page with ALL required fields"""
    st.markdown("## 😊 Happiness Index Classification")
    st.markdown("Enter country indicators to classify happiness levels.")
    
    st.markdown("---")
    
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
    with st.expander("🔧 Economic & Employment Indicators", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Unemployment_Rate_pct'] = st.slider(
                "Unemployment Rate (%)",
                min_value=0.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
                help="Percentage of labor force unemployed",
                key="happy_unemployment"
            )
            inputs['Trade_Partners_Count'] = st.number_input(
                "Trade Partners",
                min_value=0,
                max_value=250,
                value=100,
                step=5,
                help="Number of trade partner countries",
                key="happy_trade_partners"
            )
        
        with col2:
            inputs['Import_Rank_Global'] = st.number_input(
                "Import Rank (Global)",
                min_value=1,
                max_value=200,
                value=50,
                step=1,
                help="Country's global import ranking",
                key="happy_import_rank"
            )
            inputs['Export_Rank_Global'] = st.number_input(
                "Export Rank (Global)",
                min_value=1,
                max_value=200,
                value=50,
                step=1,
                help="Country's global export ranking",
                key="happy_export_rank"
            )
        
        with col3:
            inputs['Defence_expenditure_on_GDP'] = st.slider(
                "Defence Expenditure (% GDP)",
                min_value=0.0,
                max_value=15.0,
                value=2.0,
                step=0.1,
                help="Military spending as percentage of GDP",
                key="happy_defence"
            )
            inputs['Days_engaged_in_warfare_per_year'] = st.slider(
                "Conflict Days/Year",
                min_value=0,
                max_value=365,
                value=0,
                step=1,
                help="Days engaged in warfare per year",
                key="happy_conflict"
            )
    
    with st.expander("🎓 Education & Research Indicators", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Higher_Education_Rate'] = st.slider(
                "Higher Education Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=40.0,
                step=1.0,
                help="Percentage with higher education",
                key="happy_higher_ed"
            )
        
        with col2:
            inputs['Number_of_PhD_holders_per_million'] = st.number_input(
                "PhD Holders (per million)",
                min_value=0,
                max_value=1500,
                value=200,
                step=10,
                help="PhD holders per million population",
                key="happy_phd"
            )
        
        with col3:
            inputs['R_and_D_Expenditure_pct_GDP'] = st.slider(
                "R&D Expenditure (% GDP)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.1,
                help="Research & Development spending",
                key="happy_rnd"
            )
    
    with st.expander("🏥 Health & Innovation Indicators", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            inputs['Medical_Doctors_per_1000'] = st.slider(
                "Doctors per 1,000",
                min_value=0.0,
                max_value=10.0,
                value=2.5,
                step=0.1,
                help="Number of doctors per 1,000 people",
                key="happy_doctors"
            )
        
        with col2:
            inputs['Number_of_Startups'] = st.number_input(
                "Number of Startups",
                min_value=0,
                max_value=100000,
                value=5000,
                step=100,
                help="Total startup companies",
                key="happy_startups"
            )
        
        with col3:
            inputs['Number_of_Patents'] = st.number_input(
                "Number of Patents",
                min_value=0,
                max_value=200000,
                value=10000,
                step=100,
                help="Total registered patents",
                key="happy_patents"
            )
    
    with st.expander("🌍 Migration Indicators", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            inputs['Immigration_Rate'] = st.slider(
                "Immigration Rate",
                min_value=0.0,
                max_value=30.0,
                value=3.0,
                step=0.5,
                help="Rate of immigration into country",
                key="happy_immigration"
            )
        
        with col2:
            inputs['Migration_Rate'] = st.slider(
                "Migration Rate",
                min_value=-10.0,
                max_value=30.0,
                value=2.0,
                step=0.5,
                help="Net migration rate",
                key="happy_migration"
            )
    
    st.markdown("---")
    
    # Show summary of inputs
    with st.expander("📋 View All Input Values", expanded=False):
        input_df = pd.DataFrame([inputs]).T
        input_df.columns = ['Value']
        st.dataframe(input_df, use_container_width=True)
    
    st.markdown("---")
    
    # Predict button
    if st.button("🔮 Predict Happiness Level", type="primary", use_container_width=True, key="happy_predict_btn"):
        with st.spinner("Analyzing happiness indicators..."):
            import time
            time.sleep(1)
            
            # Mock prediction using all inputs
            score = (
                inputs['HDI_Index'] * 2.5 +
                (inputs['GDP_per_Capita_USD'] / 150000) * 1.5 +
                (inputs['Life_Expectancy_years'] / 90) * 1.2 +
                (inputs['Literacy_Rate_pct'] / 100) * 0.8 +
                (inputs['Internet_Access_pct'] / 100) * 0.5 +
                (inputs['Gender_Equality_Index'] / 100) * 0.6 +
                (1 - inputs['Unemployment_Rate_pct'] / 50) * 0.8 +
                (1 - inputs['Days_engaged_in_warfare_per_year'] / 365) * 0.6 +
                (inputs['Higher_Education_Rate'] / 100) * 0.4 +
                (inputs['Medical_Doctors_per_1000'] / 10) * 0.3
            )
            
            happiness_level = min(max(int(score), 1), 8)
            confidence = 0.65 + (score % 1) * 0.30
            confidence = min(confidence, 0.95)
            
            # Emoji and category
            emojis = ["😢", "😔", "😕", "😐", "🙂", "😊", "😄", "🤗"]
            categories = ["Very Low", "Low", "Below Average", "Average", 
                         "Above Average", "High", "Very High", "Excellent"]
            
            emoji = emojis[happiness_level - 1]
            category = categories[happiness_level - 1]
        
        # Display result
        st.markdown("---")
        st.markdown("## 🎯 Prediction Result")
        
        result_col1, result_col2, result_col3 = st.columns([1, 2, 1])
        
        with result_col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f5f5f5 0%, white 100%);
                border-left: 5px solid #1f77b4;
                border-radius: 10px;
                padding: 30px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <span style="font-size: 5em;">{emoji}</span>
                <h2 style="color: #1f77b4; margin: 10px 0;">Happiness Level: {happiness_level}</h2>
                <span style="
                    background: #1f77b4;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-weight: bold;
                ">{category}</span>
                <p style="color: gray; margin-top: 15px;">
                    Confidence: {confidence:.1%}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Interpretation
        if happiness_level >= 7:
            interpretation = "Excellent happiness levels indicating strong social support, economic stability, and quality of life."
        elif happiness_level >= 5:
            interpretation = "Above average happiness with good overall well-being indicators."
        elif happiness_level >= 3:
            interpretation = "Moderate happiness levels with room for improvement in various areas."
        else:
            interpretation = "Lower happiness levels suggesting challenges in economic, social, or political factors."
        
        st.info(f"💡 **Analysis:** {interpretation}")
        
        # Probability distribution
        st.markdown("### 📊 Confidence Distribution")
        
        import plotly.graph_objects as go
        
        # Generate probabilities centered around predicted level
        probs = []
        for i in range(1, 9):
            diff = abs(i - happiness_level)
            if diff == 0:
                probs.append(confidence)
            elif diff == 1:
                probs.append((1 - confidence) * 0.4)
            elif diff == 2:
                probs.append((1 - confidence) * 0.15)
            else:
                probs.append((1 - confidence) * 0.05 / max(diff - 2, 1))
        
        # Normalize
        total = sum(probs)
        probs = [p / total for p in probs]
        
        fig = go.Figure(data=[
            go.Bar(
                x=[f"Level {i}" for i in range(1, 9)],
                y=probs,
                marker_color=['#1f77b4' if i == happiness_level else '#ccc' 
                             for i in range(1, 9)],
                text=[f'{p:.1%}' for p in probs],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Prediction Probability by Level",
            xaxis_title="Happiness Level",
            yaxis_title="Probability",
            yaxis_range=[0, 1],
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key factors analysis
        st.markdown("### 🔑 Key Contributing Factors")
        
        factors = {
            'HDI Index': inputs['HDI_Index'] * 2.5,
            'GDP per Capita': (inputs['GDP_per_Capita_USD'] / 150000) * 1.5,
            'Life Expectancy': (inputs['Life_Expectancy_years'] / 90) * 1.2,
            'Literacy': (inputs['Literacy_Rate_pct'] / 100) * 0.8,
            'Employment': (1 - inputs['Unemployment_Rate_pct'] / 50) * 0.8,
            'Gender Equality': (inputs['Gender_Equality_Index'] / 100) * 0.6,
            'Peace': (1 - inputs['Days_engaged_in_warfare_per_year'] / 365) * 0.6,
            'Internet Access': (inputs['Internet_Access_pct'] / 100) * 0.5,
        }
        
        fig2 = go.Figure(data=[
            go.Bar(
                x=list(factors.values()),
                y=list(factors.keys()),
                orientation='h',
                marker_color='#2ca02c',
                text=[f'{v:.2f}' for v in factors.values()],
                textposition='auto'
            )
        ])
        
        fig2.update_layout(
            title="Factor Contributions to Happiness Score",
            xaxis_title="Contribution Score",
            yaxis_title="Factor",
            height=350,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# MAIN APP
# ============================================================
def main():
    """Main application"""
    
    # Render sidebar
    render_sidebar()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "🏠 Dashboard",
        "📈 HDI Prediction",
        "😊 Happiness Prediction"
    ])
    
    with tab1:
        render_landing_page()
    
    with tab2:
        render_hdi_page()
    
    with tab3:
        render_happiness_page()


if __name__ == "__main__":
    main()