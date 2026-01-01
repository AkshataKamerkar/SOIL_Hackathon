"""
Main Streamlit Application
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config must be first Streamlit command
st.set_page_config(
    page_title="Global Development Predictor",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23FF6B35' stroke-width='2'><circle cx='12' cy='12' r='10'/><path d='M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z'/><path d='M2 12h20'/></svg>",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LUCIDE ICONS - SVG DEFINITIONS
# ============================================================
def lucide_icon(name: str, size: int = 24, color: str = "currentColor", stroke_width: float = 2) -> str:
    """Return Lucide icon as inline SVG HTML"""
    icons = {
        "globe": '<path d="M21.54 15H17a2 2 0 0 0-2 2v4.54"/><path d="M7 3.34V5a3 3 0 0 0 3 3a2 2 0 0 1 2 2c0 1.1.9 2 2 2a2 2 0 0 0 2-2c0-1.1.9-2 2-2h3.17"/><path d="M11 21.95V18a2 2 0 0 0-2-2a2 2 0 0 1-2-2v-1a2 2 0 0 0-2-2H2.05"/><circle cx="12" cy="12" r="10"/>',
        "navigation": '<polygon points="3 11 22 2 13 21 11 13 3 11"/>',
        "book-open": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
        "bar-chart-2": '<line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/>',
        "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
        "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/>',
        "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
        "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
        "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
        "settings": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
        "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
        "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
        "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
        "arrow-down": '<line x1="12" x2="12" y1="5" y2="19"/><polyline points="19 12 12 19 5 12"/>',
        "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
        "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        "dollar-sign": '<line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
        "briefcase": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
        "graduation-cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
        "hospital": '<path d="M12 6v4"/><path d="M14 14h-4"/><path d="M14 18h-4"/><path d="M14 8h-4"/><path d="M18 12h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 22V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v18"/>',
        "flask": '<path d="M10 2v7.31"/><path d="M14 9.3V2"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/>',
        "sparkles": '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>',
        "clipboard": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>',
        "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
        "info": '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/>',
        "frown": '<circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
        "meh": '<circle cx="12" cy="12" r="10"/><line x1="8" x2="16" y1="15" y2="15"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
        "laugh": '<circle cx="12" cy="12" r="10"/><path d="M18 13a6 6 0 0 1-6 5 6 6 0 0 1-6-5h12Z"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
        "party-popper": '<path d="M5.8 11.3 2 22l10.7-3.79"/><path d="M4 3h.01"/><path d="M22 8h.01"/><path d="M15 2h.01"/><path d="M22 20h.01"/><path d="m22 2-2.24.75a2.9 2.9 0 0 0-1.96 3.12c.1.86-.57 1.63-1.45 1.63h-.38c-.86 0-1.6.6-1.76 1.44L14 10"/><path d="m22 13-.82-.33c-.86-.34-1.82.2-1.98 1.11c-.11.63-.69 1.22-1.3 1.22H17c-.76 0-1.38.58-1.44 1.34l-.69 8.66"/>',
        "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
        "book-text": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/><path d="M8 11h8"/><path d="M8 7h6"/>',
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
        "shield": '<path d="M20 13c0 5-3.5 7.5-8 8.5-4.5-1-8-3.5-8-8.5V6c0-1.1.4-2.1 1.2-2.8.7-.8 1.7-1.2 2.8-1.2h8c1.1 0 2 .4 2.8 1.2.8.7 1.2 1.7 1.2 2.8Z"/>',
        "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
        "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "pie-chart": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
        "wifi": '<path d="M12 20h.01"/><path d="M2 8.82a15 15 0 0 1 20 0"/><path d="M5 12.859a10 10 0 0 1 14 0"/><path d="M8.5 16.429a5 5 0 0 1 7 0"/>',
        "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
        "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>'
    }
    
    svg_content = icons.get(name, icons["info"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle;">{svg_content}</svg>'''


def icon_text(icon_name: str, text: str, size: int = 20, color: str = "currentColor") -> str:
    """Return icon with text as HTML"""
    return f'{lucide_icon(icon_name, size, color)} <span style="vertical-align: middle; margin-left: 8px;">{text}</span>'


# ============================================================
# CUSTOM CSS - WHITE & ORANGE THEME
# ============================================================
st.markdown("""
<style>
    /* Hide Streamlit header/toolbar */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    .stDeployButton {
        display: none !important;
    }
    
    /* Base Theme - Light Background */
    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF8F3 50%, #FFFFFF 100%);
        color: #2D3748;
    }
    
    /* Enhanced Header - Orange Gradient */
    .main-header {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 50%, #FFB347 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        padding: 1rem 0;
        font-family: 'Inter', 'SF Pro Display', -apple-system, sans-serif;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
        text-shadow: 0 4px 20px rgba(255, 107, 53, 0.3);
    }
    
    .sub-header {
        color: #718096;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
        background: linear-gradient(90deg, #718096, #A0AEC0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Ultra Premium Card - Light Theme */
    .ultra-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 32px;
        border: 1px solid rgba(255, 107, 53, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 6px -1px rgba(255, 107, 53, 0.1),
            0 10px 15px -3px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
        position: relative;
        overflow: hidden;
    }
    
    .ultra-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.5), transparent);
    }
    
    .ultra-card:hover {
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(255, 107, 53, 0.4);
        box-shadow: 
            0 20px 25px -5px rgba(255, 107, 53, 0.15),
            0 35px 60px -15px rgba(255, 107, 53, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }
    
    /* Glass Morphism Effect - Light */
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 28px;
        border: 1px solid rgba(255, 107, 53, 0.1);
        box-shadow: 
            0 8px 32px rgba(255, 107, 53, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    
    /* Modern Gradient Border - Orange */
    .gradient-border-card {
        position: relative;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 248, 243, 0.98));
        border-radius: 24px;
        padding: 32px;
    }
    
    .gradient-border-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            #FF6B35, 
            #F7931E, 
            #FFB347,
            #FF6B35);
        border-radius: 26px;
        z-index: -1;
        animation: rotate 4s linear infinite;
        background-size: 400% 400%;
    }
    
    @keyframes rotate {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Premium Button - Orange */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 16px 36px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(255, 107, 53, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(255, 107, 53, 0.6);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Secondary Button */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 107, 53, 0.1);
        border: 1px solid rgba(255, 107, 53, 0.3);
        color: #FF6B35;
    }
    
    /* Enhanced Tabs - Light Theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.95);
        padding: 8px; 
        border-radius: 16px;
        border: 1px solid rgba(255, 107, 53, 0.15);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 14px 28px;
        color: #718096;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 107, 53, 0.1);
        color: #FF6B35;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    }
    
    /* Premium Metric Cards - Light */
    .stMetric {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 107, 53, 0.15) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar Enhancement - Light */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(255, 248, 243, 0.98)) !important;
        border-right: 1px solid rgba(255, 107, 53, 0.15);
    }
    
    section[data-testid="stSidebar"] * {
        color: #2D3748 !important;
    }
    
    /* Form Elements Styling - Light */
    .stNumberInput > div > div, 
    .stSelectbox > div > div,
    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255, 107, 53, 0.2) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px);
    }
    
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 16px !important;
    }
    
    /* Input Labels - Make text visible */
    .stNumberInput label,
    .stSlider label,
    .stSelectbox label,
    .stTextInput label,
    .stNumberInput p,
    .stSlider p,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] span {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Footer Enhancement - Light */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(90deg, rgba(255, 255, 255, 0.98), rgba(255, 248, 243, 0.98));
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(255, 107, 53, 0.15);
        padding: 20px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(255, 107, 53, 0.1);
    }
    
    /* Badges */
    /* Badges - Light Theme */
    .badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 4px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 107, 53, 0.15);
    }
    
    .badge-success {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.15), rgba(56, 161, 105, 0.15));
        color: #38A169;
        border-color: rgba(72, 187, 120, 0.3);
    }
    
    .badge-warning {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(247, 147, 30, 0.15));
        color: #FF6B35;
        border-color: rgba(255, 107, 53, 0.3);
    }
    
    .badge-primary {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(247, 147, 30, 0.15));
        color: #FF6B35;
        border-color: rgba(255, 107, 53, 0.3);
    }
    
    /* Progress Bar - Light Theme */
    .progress-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 107, 53, 0.15);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .progress-bar {
        height: 12px;
        background: rgba(255, 107, 53, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 15px 0;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        border-radius: 10px;
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Confidence Meter - Light Theme */
    .confidence-meter {
        width: 100%;
        height: 120px;
        position: relative;
        margin: 30px 0;
    }
    
    .confidence-fill {
        position: absolute;
        height: 100%;
        background: linear-gradient(180deg, 
            rgba(255, 107, 53, 0.1), 
            rgba(247, 147, 30, 0.15));
        border-radius: 20px;
        transition: width 1.5s ease-in-out;
    }
    
    .confidence-value {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(255, 107, 53, 0.3);
    }
    
    .confidence-label {
        position: absolute;
        top: -25px;
        left: 0;
        color: #718096;
        font-size: 1rem;
        font-weight: 600;
    }
    
    /* Custom Scrollbar - Light Theme */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 107, 53, 0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FF6B35, #F7931E);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #F7931E, #FF6B35);
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
        # Premium Title (same as original but with gradient)
        
        
        st.markdown("<div style='height: 1px; background: linear-gradient(90deg, transparent, #FF6B35, transparent); margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # Navigation - YOUR EXACT CONTENT with premium colors
        st.markdown(f'## {lucide_icon("navigation", 24, "#FF6B35")} Navigation', unsafe_allow_html=True)
        
       
        st.markdown("<div style='height: 1px; background: linear-gradient(90deg, transparent, #F7931E, transparent); margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # About - YOUR EXACT CONTENT with premium colors
        st.markdown(f'### {lucide_icon("book-open", 20, "#FF6B35")} About', unsafe_allow_html=True)
        st.markdown("""
        This application predicts:
        
       - **HDI** (Human Development Index)
        - **Happiness Index**
       
        
        Using Machine Learning models.
        """)    
        
        
        st.markdown("<div style='height: 1px; background: linear-gradient(90deg, transparent, #FFB347, transparent); margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # Model Status - YOUR EXACT CONTENT with premium colors
        st.markdown(f'### {lucide_icon("bar-chart-2", 20, "#FF6B35")} Model Status', unsafe_allow_html=True)
        
        # Check if models exist - YOUR EXACT LOGIC
        models_dir = Path("saved_models")
        
        clf_exists = (models_dir / "classification" / "model.joblib").exists()
        reg_exists = (models_dir / "regression" / "hdi_model_v51.joblib").exists()
        
        if clf_exists:
            st.markdown(f'{lucide_icon("check-circle", 18, "#38A169")} Classification Model', unsafe_allow_html=True)
        else:
            st.markdown(f'{lucide_icon("alert-triangle", 18, "#FF6B35")} Classification Missing', unsafe_allow_html=True)
        
        if reg_exists:
            st.markdown(f'{lucide_icon("check-circle", 18, "#38A169")} Regression Model', unsafe_allow_html=True)
        else:
            st.markdown(f'{lucide_icon("alert-triangle", 18, "#FF6B35")} Regression Missing', unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1px; background: linear-gradient(90deg, transparent, #FF6B35, transparent); margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # Footer - YOUR EXACT CONTENT with premium colors
        st.markdown(f'<div style="text-align: center; padding: 20px 0;">v1.0.0 | Built with {lucide_icon("heart", 16, "#FF6B35")} by Team DATA WIZARDS!</div>', unsafe_allow_html=True)

# ============================================================
# LANDING PAGE
# ============================================================
# ============================================================
# LANDING PAGE - ENHANCED VERSION
# ============================================================
def render_landing_page():
    """Render landing page with dataset analysis"""
    st.markdown(f'<h1 class="main-header">{lucide_icon("globe", 40, "#FF6B35")} Global Development Predictor</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Predict HDI & Happiness Index using Machine Learning</p>', 
                unsafe_allow_html=True)
    
    # Feature cards using Streamlit containers
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown(f'### {lucide_icon("trending-up", 24, "#FF6B35")} HDI Prediction', unsafe_allow_html=True)
            st.markdown("Predict Human Development Index based on socioeconomic indicators.")
            st.markdown("---")
            st.markdown(f'{lucide_icon("wrench", 16, "#718096")} **Model Type:** Regression', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("target", 16, "#718096")} **Output:** HDI Score (0-1)', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("bar-chart-2", 16, "#718096")} **Features:** 25+ indicators', unsafe_allow_html=True)
    
    with col2:
        with st.container(border=True):
            st.markdown(f'### {lucide_icon("smile", 24, "#FF6B35")} Happiness Classification', unsafe_allow_html=True)
            st.markdown("Classify happiness levels based on country indicators.")
            st.markdown("---")
            st.markdown(f'{lucide_icon("wrench", 16, "#718096")} **Model Type:** Classification', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("target", 16, "#718096")} **Output:** Happiness Level (1-8)', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("bar-chart-2", 16, "#718096")} **Features:** 20+ indicators', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick reference
    st.markdown(f'## {lucide_icon("book-text", 28, "#FF6B35")} Quick Reference', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### HDI Categories")
        hdi_col1, hdi_col2 = st.columns(2)
        with hdi_col1:
            st.markdown(f'{lucide_icon("trophy", 18, "#28a745")} **Very High:** 0.800+', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("star", 18, "#17a2b8")} **High:** 0.700-0.799', unsafe_allow_html=True)
        with hdi_col2:
            st.markdown(f'{lucide_icon("activity", 18, "#ffc107")} **Medium:** 0.550-0.699', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("arrow-down", 18, "#dc3545")} **Low:** Below 0.550', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Happiness Levels")
        happy_col1, happy_col2 = st.columns(2)
        with happy_col1:
            st.markdown(f'{lucide_icon("party-popper", 18, "#28a745")} **Level 7-8:** Excellent', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("smile", 18, "#17a2b8")} **Level 5-6:** High', unsafe_allow_html=True)
        with happy_col2:
            st.markdown(f'{lucide_icon("meh", 18, "#ffc107")} **Level 3-4:** Average', unsafe_allow_html=True)
            st.markdown(f'{lucide_icon("frown", 18, "#dc3545")} **Level 1-2:** Low', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ==================== DATA ANALYSIS SECTION ====================
    st.markdown(f'## {lucide_icon("pie-chart", 28, "#FF6B35")} Dataset Analysis', unsafe_allow_html=True)
    
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
            st.markdown(f"""
            <div style="
                background: #f0f2f6;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin: 10px 0;
            ">
                <p style="color: #333; margin-bottom: 15px;">
                    {lucide_icon("trending-up", 20, "#FF6B35")} Explore comprehensive analysis of the dataset including:
                </p>
                <p style="color: #666; font-size: 0.9em;">
                    {lucide_icon("bar-chart-2", 14, "#718096")} Distribution Charts {lucide_icon("activity", 14, "#718096")} Correlation Matrix {lucide_icon("file-text", 14, "#718096")} Statistical Summary
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(
                "View Data Analysis", 
                type="primary", 
                use_container_width=True,
                key="show_analysis_btn"
            ):
                st.session_state.show_data_analysis = True
                st.rerun()
        else:
            if st.button(
                "Hide Data Analysis", 
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
            with st.spinner("Loading dataset and generating visualizations..."):
                import time
                time.sleep(0.5)  # Brief pause for UX
                st.session_state.data_loaded = True
        
        df = load_dataset()
        
        if df is not None:
            # Quick stats at the top
            st.markdown(f'### {lucide_icon("trending-up", 22, "#FF6B35")} Quick Stats', unsafe_allow_html=True)
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
            st.warning("No dataset found. Please add `sample_dataset.csv` to the `data/` folder.")
            
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
    st.markdown(f'## {lucide_icon("trending-up", 28, "#FF6B35")} Human Development Index Prediction', unsafe_allow_html=True)
    st.markdown("Enter country indicators to predict the HDI score.")
    
    st.markdown("---")
    
    inputs = {}
    
    # ==================== CORE INDICATORS ====================
    st.markdown(f'### {lucide_icon("bar-chart-2", 22, "#FF6B35")} Core Indicators', unsafe_allow_html=True)
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
    with st.expander("Economic & Trade Indicators", expanded=True):
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
    with st.expander("Health & Social Indicators", expanded=True):
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
    with st.expander("Education & Research Indicators", expanded=True):
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
    with st.expander("Technology & Other Indicators", expanded=True):
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
            st.markdown(f'{lucide_icon("lightbulb", 18, "#17a2b8")} These indicators help capture technology advancement and governance quality.', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show summary of inputs
    with st.expander("View All Input Values", expanded=False):
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
    if st.button("Predict HDI", type="primary", use_container_width=True, key="hdi_predict_btn"):
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
                result_icon = lucide_icon("trophy", 48, "#2E7D32")
            elif mock_hdi >= 0.7:
                category = "High"
                color = "#689F38"
                result_icon = lucide_icon("star", 48, "#689F38")
            elif mock_hdi >= 0.55:
                category = "Medium"
                color = "#FFA000"
                result_icon = lucide_icon("activity", 48, "#FFA000")
            else:
                category = "Low"
                color = "#D32F2F"
                result_icon = lucide_icon("arrow-down", 48, "#D32F2F")
        
        # Display result
        st.markdown("---")
        st.markdown("##  Prediction Result")
        
        result_col1, result_col2, result_col3 = st.columns([1, 2, 1])
        
        with result_col2:
            st.markdown(f"""
            <div style="
                position: relative;
                background: rgba(15, 23, 42, 0.78);
                border-radius: 18px;
                padding: 32px;
                text-align: center;
                box-shadow:
                    0 0 0 1px rgba(255,255,255,0.08),
                    0 20px 40px rgba(0,0,0,0.5),
                    0 0 40px rgba(102,126,234,0.35);
                backdrop-filter: blur(16px);
            ">
                <div style="margin-bottom: 10px;">{result_icon}</div>
                <h1 style="color: #FF6B35; margin: 10px 0;">{mock_hdi:.3f}</h1>
                <span style="
                    background: #FF6B35;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-weight: bold;
                ">{category} Human Development</span>
            </div>
            """, unsafe_allow_html=True)

            

        st.markdown("<br>", unsafe_allow_html=True)

        # Interpretation
        interpretations = {
            "Very High": f"With an HDI of {mock_hdi:.3f}, this represents very high human development. Countries at this level typically have excellent healthcare, education, and living standards.",
            "High": f"An HDI of {mock_hdi:.3f} indicates high human development. There's good access to education and healthcare with a decent standard of living.",
            "Medium": f"An HDI of {mock_hdi:.3f} suggests medium human development. There are opportunities for growth in education, healthcare, and economic development.",
            "Low": f"An HDI of {mock_hdi:.3f} indicates low human development. Significant investments in education, healthcare, and economic development are needed."
        }
        
        st.markdown(f'{lucide_icon("lightbulb", 18, "#17a2b8")} **Interpretation:** {interpretations[category]}', unsafe_allow_html=True)
        
        # Feature contribution chart
        st.markdown(f'### {lucide_icon("bar-chart-2", 22, "#FF6B35")} Feature Contributions', unsafe_allow_html=True)
        
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
                marker_color='#FF6B35',
                text=[f'{v:.3f}' for v in contributions.values()],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=dict(text="Contribution to HDI Score", font=dict(color='#000000', size=18)),
            xaxis_title=dict(text="Contribution", font=dict(color='#000000', size=14)),
            yaxis_title=dict(text="Feature", font=dict(color='#000000', size=14)),
            height=450,
            yaxis={'categoryorder': 'total ascending'},
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            xaxis=dict(gridcolor='#E2E8F0', zerolinecolor='#E2E8F0', tickfont=dict(color='#000000', size=12)),
            yaxis_tickfont=dict(color='#000000', size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown(f'### {lucide_icon("clipboard", 22, "#FF6B35")} Development Recommendations', unsafe_allow_html=True)
        
        recommendations = []
        
        if inputs['Literacy_Rate_pct'] < 80:
            recommendations.append(f"{lucide_icon('book-open', 16, '#FF6B35')} **Education:** Improve literacy rates through expanded education programs")
        if inputs['Life_Expectancy_years'] < 70:
            recommendations.append(f"{lucide_icon('hospital', 16, '#FF6B35')} **Healthcare:** Invest in healthcare infrastructure to improve life expectancy")
        if inputs['Internet_Access_pct'] < 60:
            recommendations.append(f"{lucide_icon('wifi', 16, '#FF6B35')} **Digital:** Expand internet infrastructure for better connectivity")
        if inputs['Unemployment_Rate_pct'] > 10:
            recommendations.append(f"{lucide_icon('briefcase', 16, '#FF6B35')} **Employment:** Implement job creation programs to reduce unemployment")
        if inputs['Gender_Equality_Index'] < 60:
            recommendations.append(f"{lucide_icon('scale', 16, '#FF6B35')} **Equality:** Strengthen gender equality policies and programs")
        if inputs['Days_engaged_in_warfare_per_year'] > 0:
            recommendations.append(f"{lucide_icon('shield', 16, '#FF6B35')} **Peace:** Prioritize conflict resolution and peacekeeping efforts")
        if inputs['R_and_D_Expenditure_pct_GDP'] < 1.5:
            recommendations.append(f"{lucide_icon('flask', 16, '#FF6B35')} **Innovation:** Increase R&D investment for technological advancement")
        
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}", unsafe_allow_html=True)
        else:
            st.markdown(f'{lucide_icon("check-circle", 18, "#28a745")} All key indicators are at healthy levels! Focus on maintaining current standards.', unsafe_allow_html=True)


# ============================================================
# HAPPINESS PREDICTION PAGE - ALL FIELDS
# ============================================================
def render_happiness_page():
    """Render happiness prediction page with ALL required fields"""
    st.markdown(f'## {lucide_icon("smile", 28, "#FF6B35")} Happiness Index Classification', unsafe_allow_html=True)
    st.markdown("Enter country indicators to classify happiness levels.")
    
    st.markdown("---")
    
    inputs = {}
    
    # ==================== CORE INDICATORS ====================
    st.markdown(f'### {lucide_icon("bar-chart-2", 22, "#FF6B35")} Core Indicators', unsafe_allow_html=True)
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
    with st.expander("Economic & Employment Indicators", expanded=True):
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
    
    with st.expander("Education & Research Indicators", expanded=True):
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
    
    with st.expander("Health & Innovation Indicators", expanded=True):
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
    
    with st.expander("Migration Indicators", expanded=True):
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
    with st.expander("View All Input Values", expanded=False):
        input_df = pd.DataFrame([inputs]).T
        input_df.columns = ['Value']
        st.dataframe(input_df, use_container_width=True)
    
    st.markdown("---")
    
    # Predict button
    if st.button("Predict Happiness Level", type="primary", use_container_width=True, key="happy_predict_btn"):
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
            
            # Icons and category
            icons_list = ["frown", "frown", "meh", "meh", "smile", "smile", "laugh", "party-popper"]
            colors_list = ["#D32F2F", "#D32F2F", "#FFA000", "#FFA000", "#689F38", "#689F38", "#2E7D32", "#2E7D32"]
            categories = ["Very Low", "Low", "Below Average", "Average", 
                         "Above Average", "High", "Very High", "Excellent"]
            
            result_icon = lucide_icon(icons_list[happiness_level - 1], 48, colors_list[happiness_level - 1])
            category = categories[happiness_level - 1]
        
        # Display result
        st.markdown("---")
        st.markdown("##  Prediction Result")
        
        result_col1, result_col2, result_col3 = st.columns([1, 2, 1])
        
        with result_col2:
            st.markdown(f"""
            <div style="
                position: relative;
                background: rgba(15, 23, 42, 0.78);
                border-radius: 18px;
                padding: 32px;
                text-align: center;
                box-shadow:
                    0 0 0 1px rgba(255,255,255,0.08),
                    0 20px 40px rgba(0,0,0,0.5),
                    0 0 40px rgba(102,126,234,0.35);
                backdrop-filter: blur(16px);
            ">
                <div style="margin-bottom: 10px;">{result_icon}</div>
                <h2 style="color: #FF6B35; margin: 10px 0;">Happiness Level: {happiness_level}</h2>
                <span style="
                    background: #FF6B35;
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
            st.markdown(
    "<div style='height: 24px;'></div>",
    unsafe_allow_html=True
)

        
        # Interpretation
        if happiness_level >= 7:
            interpretation = "Excellent happiness levels indicating strong social support, economic stability, and quality of life."
        elif happiness_level >= 5:
            interpretation = "Above average happiness with good overall well-being indicators."
        elif happiness_level >= 3:
            interpretation = "Moderate happiness levels with room for improvement in various areas."
        else:
            interpretation = "Lower happiness levels suggesting challenges in economic, social, or political factors."
        
        st.markdown(f'{lucide_icon("lightbulb", 18, "#17a2b8")} **Analysis:** {interpretation}', unsafe_allow_html=True)
        
        # Probability distribution
        st.markdown(f'### {lucide_icon("bar-chart-2", 22, "#FF6B35")} Confidence Distribution', unsafe_allow_html=True)
        
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
                marker_color=['#FF6B35' if i == happiness_level else '#ccc' 
                             for i in range(1, 9)],
                text=[f'{p:.1%}' for p in probs],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=dict(text="Prediction Probability by Level", font=dict(color='#000000', size=18)),
            xaxis_title=dict(text="Happiness Level", font=dict(color='#000000', size=14)),
            yaxis_title=dict(text="Probability", font=dict(color='#000000', size=14)),
            yaxis_range=[0, 1],
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            xaxis=dict(gridcolor='#E2E8F0', zerolinecolor='#E2E8F0', tickfont=dict(color='#000000', size=12)),
            yaxis=dict(gridcolor='#E2E8F0', zerolinecolor='#E2E8F0', tickfont=dict(color='#000000', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key factors analysis
        st.markdown(f'### {lucide_icon("zap", 22, "#FF6B35")} Key Contributing Factors', unsafe_allow_html=True)
        
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
            title=dict(text="Factor Contributions to Happiness Score", font=dict(color="#000000", size=18)),
            xaxis_title=dict(text="Contribution Score", font=dict(color='#000000', size=14)),
            yaxis_title=dict(text="Factor", font=dict(color='#000000', size=14)),
            height=350,
            yaxis={'categoryorder': 'total ascending'},
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            xaxis=dict(gridcolor='#E2E8F0', zerolinecolor='#E2E8F0', tickfont=dict(color='#000000', size=12)),
            yaxis_tickfont=dict(color='#000000', size=12)
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
        "Dashboard",
        "HDI Prediction",
        "Happiness Prediction"
    ])
    
    with tab1:
        render_landing_page()
    
    with tab2:
        render_hdi_page()
    
    with tab3:
        render_happiness_page()


if __name__ == "__main__":
    main()
