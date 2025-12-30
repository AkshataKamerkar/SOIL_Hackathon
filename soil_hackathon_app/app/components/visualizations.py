"""
Visualization Components
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path


def load_dataset() -> Optional[pd.DataFrame]:
    """Load the sample dataset"""
    try:
        data_path = Path("data/sample_dataset.csv")
        if data_path.exists():
            return pd.read_csv(data_path)
        return None
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None


def create_hdi_gauge(value: float, category: str) -> go.Figure:
    """Create HDI gauge chart"""
    
    colors = {
        "Very High": "#2E7D32",
        "High": "#689F38",
        "Medium": "#FFA000",
        "Low": "#D32F2F"
    }
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "HDI Score", 'font': {'size': 24}},
        delta={'reference': 0.7, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': colors.get(category, "#1f77b4")},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.55], 'color': '#FFCDD2'},
                {'range': [0.55, 0.70], 'color': '#FFE0B2'},
                {'range': [0.70, 0.80], 'color': '#C8E6C9'},
                {'range': [0.80, 1.0], 'color': '#A5D6A7'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkblue", 'family': "Arial"},
        height=300
    )
    
    return fig


def create_happiness_probability_chart(probabilities: Dict[str, float]) -> go.Figure:
    """Create bar chart for happiness probabilities"""
    
    levels = list(probabilities.keys())
    probs = list(probabilities.values())
    
    colors = ['#1f77b4' if p == max(probs) else '#ccc' for p in probs]
    
    fig = go.Figure(data=[
        go.Bar(
            x=levels,
            y=probs,
            marker_color=colors,
            text=[f'{p:.1%}' for p in probs],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Prediction Confidence by Level",
        xaxis_title="Happiness Level",
        yaxis_title="Probability",
        yaxis_range=[0, 1],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350
    )
    
    return fig


def display_dataset_overview(df: pd.DataFrame):
    """Display basic dataset overview metrics"""
    
    st.markdown("###  Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with col2:
        st.metric("Features", f"{len(df.columns):,}")
    
    with col3:
        if 'HDI_Index' in df.columns:
            st.metric("Avg HDI", f"{df['HDI_Index'].mean():.3f}")
        else:
            st.metric("Avg HDI", "N/A")
    
    with col4:
        if 'GDP_per_Capita_USD' in df.columns:
            st.metric("Avg GDP", f"${df['GDP_per_Capita_USD'].mean():,.0f}")
        else:
            st.metric("Avg GDP", "N/A")


def display_hdi_distribution(df: pd.DataFrame):
    """Display HDI distribution chart"""
    
    if 'HDI_Index' not in df.columns:
        st.warning("HDI_Index column not found in dataset")
        return
    
    fig = go.Figure()
    
    # Histogram
    fig.add_trace(go.Histogram(
        x=df['HDI_Index'],
        nbinsx=30,
        name='Distribution',
        marker_color='#1f77b4',
        opacity=0.7
    ))
    
    # Add category regions
    fig.add_vrect(x0=0, x1=0.55, fillcolor="red", opacity=0.1, 
                  annotation_text="Low", annotation_position="top left")
    fig.add_vrect(x0=0.55, x1=0.70, fillcolor="orange", opacity=0.1,
                  annotation_text="Medium", annotation_position="top left")
    fig.add_vrect(x0=0.70, x1=0.80, fillcolor="lightgreen", opacity=0.1,
                  annotation_text="High", annotation_position="top left")
    fig.add_vrect(x0=0.80, x1=1.0, fillcolor="green", opacity=0.1,
                  annotation_text="Very High", annotation_position="top left")
    
    fig.update_layout(
        title="HDI Distribution by Category",
        xaxis_title="HDI Index",
        yaxis_title="Count",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_gdp_vs_hdi(df: pd.DataFrame):
    """Display GDP vs HDI scatter plot"""
    
    if 'GDP_per_Capita_USD' not in df.columns or 'HDI_Index' not in df.columns:
        st.warning("Required columns not found")
        return
    
    fig = px.scatter(
        df,
        x='GDP_per_Capita_USD',
        y='HDI_Index',
        trendline="ols",
        title="GDP per Capita vs HDI Index",
        labels={
            'GDP_per_Capita_USD': 'GDP per Capita (USD)',
            'HDI_Index': 'HDI Index'
        },
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def display_correlation_matrix(df: pd.DataFrame, top_n: int = 12):
    """Display correlation matrix for top features"""
    
    # Select numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Select top N columns by variance (or specific important ones)
    important_cols = [
        'HDI_Index', 'GDP_per_Capita_USD', 'Life_Expectancy_years',
        'Literacy_Rate_pct', 'Internet_Access_pct', 'Unemployment_Rate_pct',
        'Higher_Education_Rate', 'Medical_Doctors_per_1000',
        'Gender_Equality_Index', 'R_and_D_Expenditure_pct_GDP',
        'Days_engaged_in_warfare_per_year', 'Trade_Partners_Count'
    ]
    
    available_cols = [col for col in important_cols if col in numeric_df.columns][:top_n]
    
    if len(available_cols) < 2:
        st.warning("Not enough numeric columns for correlation matrix")
        return
    
    corr = numeric_df[available_cols].corr()
    
    fig = px.imshow(
        corr,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation Matrix"
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def display_feature_distributions(df: pd.DataFrame):
    """Display distribution of key features"""
    
    features = {
        'Life_Expectancy_years': 'Life Expectancy',
        'Literacy_Rate_pct': 'Literacy Rate',
        'GDP_per_Capita_USD': 'GDP per Capita',
        'Unemployment_Rate_pct': 'Unemployment Rate'
    }
    
    available_features = {k: v for k, v in features.items() if k in df.columns}
    
    if not available_features:
        st.warning("No key features found for distribution plots")
        return
    
    cols = st.columns(2)
    
    for idx, (col_name, display_name) in enumerate(available_features.items()):
        with cols[idx % 2]:
            fig = px.histogram(
                df,
                x=col_name,
                nbins=25,
                title=f"{display_name} Distribution",
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(
                height=300,
                showlegend=False,
                xaxis_title=display_name,
                yaxis_title="Count"
            )
            st.plotly_chart(fig, use_container_width=True)


def display_box_plots(df: pd.DataFrame):
    """Display box plots for key numeric features"""
    
    features = ['HDI_Index', 'Life_Expectancy_years', 'Literacy_Rate_pct', 
                'Internet_Access_pct', 'Unemployment_Rate_pct']
    
    available_features = [f for f in features if f in df.columns]
    
    if not available_features:
        st.warning("No features available for box plots")
        return
    
    fig = go.Figure()
    
    for feat in available_features:
        fig.add_trace(go.Box(
            y=df[feat],
            name=feat.replace('_', ' ').replace(' pct', ' %'),
            boxmean=True
        ))
    
    fig.update_layout(
        title="Feature Distribution Box Plots",
        yaxis_title="Value",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_hdi_by_category_stats(df: pd.DataFrame):
    """Display statistics grouped by HDI category"""
    
    if 'HDI_Index' not in df.columns:
        return
    
    # Create HDI category
    df_copy = df.copy()
    df_copy['HDI_Category'] = pd.cut(
        df_copy['HDI_Index'],
        bins=[0, 0.55, 0.70, 0.80, 1.0],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Count by category
    category_counts = df_copy['HDI_Category'].value_counts().sort_index()
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Distribution by HDI Category",
        color_discrete_sequence=['#D32F2F', '#FFA000', '#689F38', '#2E7D32']
    )
    
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)


def display_top_correlations_with_hdi(df: pd.DataFrame, top_n: int = 10):
    """Display features most correlated with HDI"""
    
    if 'HDI_Index' not in df.columns:
        st.warning("HDI_Index not found in dataset")
        return
    
    numeric_df = df.select_dtypes(include=[np.number])
    correlations = numeric_df.corr()['HDI_Index'].drop('HDI_Index').abs().sort_values(ascending=False)
    
    top_corr = correlations.head(top_n)
    
    fig = go.Figure(data=[
        go.Bar(
            x=top_corr.values,
            y=top_corr.index,
            orientation='h',
            marker_color='#1f77b4'
        )
    ])
    
    fig.update_layout(
        title=f"Top {top_n} Features Correlated with HDI",
        xaxis_title="Absolute Correlation",
        yaxis_title="Feature",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_scatter_matrix(df: pd.DataFrame):
    """Display scatter matrix for key features"""
    
    features = ['HDI_Index', 'GDP_per_Capita_USD', 'Life_Expectancy_years', 'Literacy_Rate_pct']
    available = [f for f in features if f in df.columns]
    
    if len(available) < 2:
        return
    
    fig = px.scatter_matrix(
        df[available],
        dimensions=available,
        title="Scatter Matrix of Key Features",
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.update_layout(height=600)
    fig.update_traces(diagonal_visible=False, showupperhalf=False)
    
    st.plotly_chart(fig, use_container_width=True)


def display_comprehensive_analysis(df: pd.DataFrame):
    """Display comprehensive dataset analysis"""
    
    st.markdown("---")
    
    # Overview metrics
    display_dataset_overview(df)
    
    st.markdown("---")
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distributions", 
        "🔗 Correlations", 
        "📈 Relationships",
        "📋 Data Summary"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            display_hdi_distribution(df)
        with col2:
            display_hdi_by_category_stats(df)
        
        st.markdown("#### Feature Distributions")
        display_feature_distributions(df)
        display_box_plots(df)
    
    with tab2:
        display_correlation_matrix(df)
        display_top_correlations_with_hdi(df)
    
    with tab3:
        display_gdp_vs_hdi(df)
        display_scatter_matrix(df)
    
    with tab4:
        st.markdown("#### 📋 Dataset Statistics")
        
        # Basic stats
        st.markdown("**Numeric Features Summary:**")
        st.dataframe(df.describe().round(2), use_container_width=True)
        
        # Missing values
        st.markdown("**Missing Values:**")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) > 0:
            st.dataframe(missing.to_frame('Missing Count'), use_container_width=True)
        else:
            st.success("No missing values in the dataset!")
        
        # Data types
        st.markdown("**Data Types:**")
        dtypes_df = pd.DataFrame({
            'Column': df.dtypes.index,
            'Type': df.dtypes.values.astype(str)
        })
        st.dataframe(dtypes_df, use_container_width=True, hide_index=True)
        
        # Sample data
        st.markdown("**Sample Data (First 10 rows):**")
        st.dataframe(df.head(10), use_container_width=True)