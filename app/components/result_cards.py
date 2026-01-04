"""
Result Display Components
"""
import streamlit as st
from typing import Dict, Any
from models.predictor import PredictionResult


def display_hdi_result(result: PredictionResult):
    """Display HDI prediction result with enhanced UI"""
    
    # Category colors and icons
    category_styles = {
        "Very High": {"color": "#2E7D32", "icon": "🏆", "bg": "#E8F5E9"},
        "High": {"color": "#689F38", "icon": "🌟", "bg": "#F1F8E9"},
        "Medium": {"color": "#FFA000", "icon": "📊", "bg": "#FFF8E1"},
        "Low": {"color": "#D32F2F", "icon": "📉", "bg": "#FFEBEE"}
    }
    
    style = category_styles.get(result.category, category_styles["Medium"])
    
    # Main result card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {style['bg']} 0%, white 100%);
        border-left: 5px solid {style['color']};
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h2 style="color: {style['color']}; margin: 0;">
                    {style['icon']} HDI Prediction Result
                </h2>
                <p style="color: black; font-size: 0.9em; margin-top: 5px; font-color: black;">
                    Human Development Index Analysis
                </p>
            </div>
            <div style="text-align: right;">
                <h1 style="color: {style['color']}; margin: 0; font-size: 3em;">
                    {result.value:.3f}
                </h1>
                <span style="
                    background: {style['color']};
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                ">
                    {result.category}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interpretation
    if result.interpretation:
        st.info(f"💡 **Interpretation:** {result.interpretation}")
    
    # Recommendations based on category
    st.markdown("### 📋 Development Recommendations")
    
    recommendations = {
        "Very High": [
            "✅ Maintain current development strategies",
            "✅ Focus on sustainability and innovation",
            "✅ Consider supporting less developed nations"
        ],
        "High": [
            "📈 Continue investments in education and healthcare",
            "📈 Strengthen social safety nets",
            "📈 Promote economic diversification"
        ],
        "Medium": [
            "🎯 Prioritize education accessibility",
            "🎯 Improve healthcare infrastructure",
            "🎯 Create stable economic policies"
        ],
        "Low": [
            "⚠️ Focus on basic education and literacy",
            "⚠️ Improve access to clean water and healthcare",
            "⚠️ Develop stable governance and reduce conflict"
        ]
    }
    
    for rec in recommendations.get(result.category, []):
        st.markdown(f"- {rec}")


def display_happiness_result(result: PredictionResult):
    """Display Happiness classification result"""
    
    # Level colors
    level_colors = {
        1: "#D32F2F", 2: "#F44336", 3: "#FF5722",
        4: "#FF9800", 5: "#FFC107", 6: "#8BC34A",
        7: "#4CAF50", 8: "#2E7D32"
    }
    
    color = level_colors.get(result.value, "#1f77b4")
    
    # Emoji mapping
    level_emojis = {
        1: "😢", 2: "😔", 3: "😕",
        4: "😐", 5: "🙂", 6: "😊",
        7: "😄", 8: "🤗"
    }
    
    emoji = level_emojis.get(result.value, "📊")
    
    # Main result card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f5f5f5 0%, white 100%);
        border-left: 5px solid {color};
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <div style="text-align: center;">
            <span style="font-size: 4em;">{emoji}</span>
            <h2 style="color: {color}; margin: 10px 0;">
                Happiness Level: {result.value}
            </h2>
            <span style="
                background: {color};
                color: white;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 1.2em;
            ">
                {result.category}
            </span>
            <p style="color: black; margin-top: 15px; font-size: 1.1em;">
                Confidence: {result.confidence:.1%}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interpretation
    if result.interpretation:
        st.info(f"💡 **Analysis:** {result.interpretation}")
    
    # Confidence breakdown
    if result.probabilities:
        st.markdown("### 📊 Confidence Distribution")
        
        # Show as metrics
        cols = st.columns(min(4, len(result.probabilities)))
        sorted_probs = sorted(
            result.probabilities.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for col, (level, prob) in zip(cols, sorted_probs[:4]):
            col.metric(level, f"{prob:.1%}")


def display_prediction_comparison(
    hdi_result: PredictionResult = None,
    happiness_result: PredictionResult = None
):
    """Display side-by-side comparison of both predictions"""
    
    st.markdown("### 🔄 Prediction Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 HDI Prediction")
        if hdi_result:
            st.metric(
                "HDI Score",
                f"{hdi_result.value:.3f}",
                delta=hdi_result.category
            )
        else:
            st.info("Run HDI prediction to see results")
    
    with col2:
        st.markdown("#### 😊 Happiness Prediction")
        if happiness_result:
            st.metric(
                "Happiness Level",
                f"Level {happiness_result.value}",
                delta=f"{happiness_result.confidence:.1%} confidence"
            )
        else:
            st.info("Run Happiness prediction to see results")