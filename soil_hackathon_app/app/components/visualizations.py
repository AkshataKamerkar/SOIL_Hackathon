"""
Visualization Components - Enhanced with Insights and Lucide Icons
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path


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
        "trending-down": '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/>',
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
        "clipboard-list": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
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
        "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
        "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
        "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
        "folder-open": '<path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>',
        "hash": '<line x1="4" x2="20" y1="9" y2="9"/><line x1="4" x2="20" y1="15" y2="15"/><line x1="10" x2="8" y1="3" y2="21"/><line x1="16" x2="14" y1="3" y2="21"/>',
        "hard-drive": '<line x1="22" x2="2" y1="12" y2="12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/><line x1="6" x2="6.01" y1="16" y2="16"/><line x1="10" x2="10.01" y1="16" y2="16"/>',
        "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
        "link-2": '<path d="M9 17H7A5 5 0 0 1 7 7h2"/><path d="M15 7h2a5 5 0 1 1 0 10h-2"/><line x1="8" x2="16" y1="12" y2="12"/>',
        "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
        "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/>',
        "x-circle": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
        "circle-1": '<circle cx="12" cy="12" r="10"/><path d="M12 8v8"/><path d="M10 8h2"/>',
        "circle-2": '<circle cx="12" cy="12" r="10"/><path d="M10 8h3a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-2a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h3"/>',
        "circle-3": '<circle cx="12" cy="12" r="10"/><path d="M10 8h3a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-2"/><path d="M11 12h2a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-3"/>',
        "circle-4": '<circle cx="12" cy="12" r="10"/><path d="M10 8v4h4"/><path d="M14 8v8"/>',
        "circle-5": '<circle cx="12" cy="12" r="10"/><path d="M14 8h-3v3h2a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-3"/>',
        "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
        "building": '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
        "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
        "snowflake": '<line x1="2" x2="22" y1="12" y2="12"/><line x1="12" x2="12" y1="2" y2="22"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/>'
    }
    
    svg_content = icons.get(name, icons["info"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle;">{svg_content}</svg>'''


def icon_text(icon_name: str, text: str, size: int = 20, color: str = "currentColor", gap: int = 8) -> str:
    """Return icon with text as HTML"""
    return f'{lucide_icon(icon_name, size, color)} <span style="vertical-align: middle; margin-left: {gap}px;">{text}</span>'


def section_header(icon_name: str, title: str, subtitle: str = None, icon_color: str = "#6366F1") -> None:
    """Display a section header with icon"""
    header_html = f'''
    <div style="margin-bottom: 16px;">
        <h2 style="margin: 0; color: #E2E8F0; display: flex; align-items: center; gap: 12px;">
            {lucide_icon(icon_name, 28, icon_color)}
            <span>{title}</span>
        </h2>
        {f'<p style="margin: 5px 0 0 40px; color: #94A3B8; font-style: italic;">{subtitle}</p>' if subtitle else ''}
    </div>
    '''
    st.markdown(header_html, unsafe_allow_html=True)


def subsection_header(number: int, title: str, icon_color: str = "#6366F1") -> None:
    """Display a numbered subsection header"""
    # Number icons mapping
    number_icons = {
        1: "circle-1", 2: "circle-2", 3: "circle-3", 
        4: "circle-4", 5: "circle-5"
    }
    icon_name = number_icons.get(number, "info")
    
    header_html = f'''
    <h3 style="margin: 0; color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon(icon_name, 24, icon_color)}
        <span>{title}</span>
    </h3>
    '''
    st.markdown(header_html, unsafe_allow_html=True)


def insight_box(text: str, icon_name: str = "lightbulb", color: str = "#6366F1") -> None:
    """Display an insight box with icon"""
    insight_html = f'''
    <div style="background: rgba(99, 102, 241, 0.1); border-left: 4px solid {color}; 
                padding: 12px 16px; border-radius: 0 8px 8px 0; margin: 16px 0;">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            {lucide_icon(icon_name, 20, color)}
            <span style="color: #E2E8F0;">{text}</span>
        </div>
    </div>
    '''
    st.markdown(insight_html, unsafe_allow_html=True)


# ============================================================
# COLAB NOTEBOOK LINKS - UPDATE THESE
# ============================================================
HDI_COLAB_LINK = "https://colab.research.google.com/drive/1z3qH1mQVcpvkZ35dfR24UBqx5TiULa83?usp=sharing"
HAPPINESS_COLAB_LINK = "https://colab.research.google.com/drive/1z3qH1mQVcpvkZ35dfR24UBqx5TiULa83?usp=sharing"


# ============================================================
# DATA LOADING
# ============================================================
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


# ============================================================
# GAUGE CHARTS FOR PREDICTIONS
# ============================================================
def create_hdi_gauge(value: float, category: str) -> go.Figure:
    """Create HDI gauge chart"""
    
    colors = {
        "Very High": "#10B981",
        "High": "#22C55E",
        "Medium": "#F59E0B",
        "Low": "#EF4444"
    }
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "HDI Score", 'font': {'size': 24, 'color': '#E2E8F0'}},
        delta={'reference': 0.7, 'increasing': {'color': "#10B981"}},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': colors.get(category, "#6366F1")},
            'bgcolor': "rgba(30, 41, 59, 0.5)",
            'borderwidth': 2,
            'bordercolor': "#475569",
            'steps': [
                {'range': [0, 0.55], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [0.55, 0.70], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [0.70, 0.80], 'color': 'rgba(34, 197, 94, 0.3)'},
                {'range': [0.80, 1.0], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "#F43F5E", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#E2E8F0", 'family': "Inter, sans-serif"},
        height=300
    )
    
    return fig


def create_happiness_probability_chart(probabilities: Dict[str, float]) -> go.Figure:
    """Create bar chart for happiness probabilities"""
    
    levels = list(probabilities.keys())
    probs = list(probabilities.values())
    
    colors = ['#6366F1' if p == max(probs) else '#475569' for p in probs]
    
    fig = go.Figure(data=[
        go.Bar(
            x=levels,
            y=probs,
            marker_color=colors,
            text=[f'{p:.1%}' for p in probs],
            textposition='auto',
            textfont={'color': '#E2E8F0'}
        )
    ])
    
    fig.update_layout(
        title={'text': "Prediction Confidence", 'font': {'color': '#E2E8F0'}},
        xaxis_title="Happiness Level",
        yaxis_title="Probability",
        yaxis_range=[0, 1],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': '#94A3B8'},
        height=350
    )
    fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
    fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
    
    return fig


# ============================================================
# DATASET OVERVIEW
# ============================================================
def display_dataset_overview(df: pd.DataFrame):
    """Display basic dataset overview metrics with Lucide icons"""
    
    st.markdown(f"""
    <h3 style="color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon("bar-chart-2", 24, "#6366F1")}
        <span>Dataset at a Glance</span>
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); padding: 16px; border-radius: 12px; text-align: center; border-left: 3px solid #6366F1;">
            <div style="margin-bottom: 8px;">{lucide_icon("folder", 24, "#6366F1")}</div>
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Records</p>
            <h3 style="margin: 5px 0 0 0; color: #E2E8F0;">{len(df):,}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); padding: 16px; border-radius: 12px; text-align: center; border-left: 3px solid #10B981;">
            <div style="margin-bottom: 8px;">{lucide_icon("clipboard-list", 24, "#10B981")}</div>
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Features</p>
            <h3 style="margin: 5px 0 0 0; color: #E2E8F0;">{len(df.columns):,}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if 'HDI_Index' in df.columns:
            st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.1); padding: 16px; border-radius: 12px; text-align: center; border-left: 3px solid #F59E0B;">
                <div style="margin-bottom: 8px;">{lucide_icon("trending-up", 24, "#F59E0B")}</div>
                <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Avg HDI</p>
                <h3 style="margin: 5px 0 0 0; color: #E2E8F0;">{df['HDI_Index'].mean():.3f}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if 'Happiness_Index_Ordinal' in df.columns:
            st.markdown(f"""
            <div style="background: rgba(236, 72, 153, 0.1); padding: 16px; border-radius: 12px; text-align: center; border-left: 3px solid #EC4899;">
                <div style="margin-bottom: 8px;">{lucide_icon("smile", 24, "#EC4899")}</div>
                <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Avg Happiness</p>
                <h3 style="margin: 5px 0 0 0; color: #E2E8F0;">{df['Happiness_Index_Ordinal'].mean():.1f}/8</h3>
            </div>
            """, unsafe_allow_html=True)
    
    with col5:
        if 'GDP_per_Capita_USD' in df.columns:
            st.markdown(f"""
            <div style="background: rgba(139, 92, 246, 0.1); padding: 16px; border-radius: 12px; text-align: center; border-left: 3px solid #8B5CF6;">
                <div style="margin-bottom: 8px;">{lucide_icon("dollar-sign", 24, "#8B5CF6")}</div>
                <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Avg GDP</p>
                <h3 style="margin: 5px 0 0 0; color: #E2E8F0;">${df['GDP_per_Capita_USD'].mean():,.0f}</h3>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# HDI ANALYSIS SECTION
# ============================================================
def display_hdi_analysis(df: pd.DataFrame):
    """Display comprehensive HDI analysis with insights"""
    
    section_header("trending-up", "HDI (Human Development Index) Analysis", 
                   "Understanding what drives human development across nations", "#22C55E")
    st.markdown("---")
    
    if 'HDI_Index' not in df.columns:
        st.warning("HDI_Index column not found in dataset")
        return
    
    df_copy = df.copy()
    
    # Create HDI categories
    df_copy['HDI_Category'] = pd.cut(
        df_copy['HDI_Index'],
        bins=[0, 0.55, 0.70, 0.80, 1.0],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # ========== 1. HDI Distribution ==========
    subsection_header(1, "How is HDI Distributed Globally?", "#22C55E")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        fig = go.Figure()
        
        colors_map = {'Low': '#EF4444', 'Medium': '#F59E0B', 'High': '#22C55E', 'Very High': '#10B981'}
        
        for category in ['Low', 'Medium', 'High', 'Very High']:
            cat_data = df_copy[df_copy['HDI_Category'] == category]['HDI_Index']
            if len(cat_data) > 0:
                fig.add_trace(go.Histogram(
                    x=cat_data,
                    name=category,
                    marker_color=colors_map[category],
                    opacity=0.75,
                    nbinsx=20
                ))
        
        fig.update_layout(
            title="HDI Score Distribution",
            xaxis_title="HDI Index",
            yaxis_title="Number of Countries",
            barmode='stack',
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=350,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart
        category_counts = df_copy['HDI_Category'].value_counts().reindex(['Low', 'Medium', 'High', 'Very High'])
        
        fig = go.Figure(data=[go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            hole=0.45,
            marker_colors=['#EF4444', '#F59E0B', '#22C55E', '#10B981'],
            textinfo='percent+label',
            textfont={'color': '#E2E8F0', 'size': 12}
        )])
        
        fig.update_layout(
            title="Countries by Development Level",
            paper_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Calculate percentages for insight
    total = len(df_copy)
    low_pct = (df_copy['HDI_Category'] == 'Low').sum() / total * 100
    high_pct = ((df_copy['HDI_Category'] == 'High') | (df_copy['HDI_Category'] == 'Very High')).sum() / total * 100
    
    insight_box(f"<strong>Insight:</strong> {high_pct:.1f}% of countries have High or Very High HDI, while {low_pct:.1f}% still struggle with low development levels.")
    
    st.markdown("---")
    
    # ========== 2. GDP vs HDI ==========
    subsection_header(2, "Does Money Buy Development?", "#22C55E")
    
    if 'GDP_per_Capita_USD' in df.columns:
        fig = px.scatter(
            df_copy,
            x='GDP_per_Capita_USD',
            y='HDI_Index',
            color='HDI_Category',
            color_discrete_map={'Low': '#EF4444', 'Medium': '#F59E0B', 'High': '#22C55E', 'Very High': '#10B981'},
            hover_data=['Life_Expectancy_years', 'Literacy_Rate_pct'] if 'Life_Expectancy_years' in df.columns else None,
            title="GDP per Capita vs HDI Index"
        )
        
        fig.update_layout(
            xaxis_title="GDP per Capita (USD)",
            yaxis_title="HDI Index",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=400
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        corr = df['GDP_per_Capita_USD'].corr(df['HDI_Index'])
        insight_box(f"<strong>Insight:</strong> GDP and HDI correlation is <strong>{corr:.2f}</strong>. Economic wealth strongly predicts development, but notice the curve flattens at higher incomes—money alone isn't enough.")
    
    st.markdown("---")
    
    # ========== 3. Top Factors ==========
    subsection_header(3, "What Drives Human Development?", "#22C55E")
    
    # Calculate correlations with HDI
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'HDI_Index' in numeric_cols:
        numeric_cols.remove('HDI_Index')
    
    correlations = df[numeric_cols + ['HDI_Index']].corr()['HDI_Index'].drop('HDI_Index').sort_values()
    
    top_positive = correlations.tail(8).sort_values(ascending=True)
    top_negative = correlations.head(5).sort_values(ascending=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            {lucide_icon("check-circle", 20, "#22C55E")}
            <span style="color: #E2E8F0; font-weight: 600;">Positive Impact on HDI</span>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=top_positive.values,
                y=[name.replace('_', ' ')[:30] for name in top_positive.index],
                orientation='h',
                marker_color='#22C55E',
                text=[f'{v:.2f}' for v in top_positive.values],
                textposition='outside',
                textfont={'color': '#E2E8F0'}
            )
        ])
        
        fig.update_layout(
            xaxis_title="Correlation Coefficient",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=380,
            xaxis_range=[0, 1.1],
            margin=dict(l=10, r=10)
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            {lucide_icon("x-circle", 20, "#EF4444")}
            <span style="color: #E2E8F0; font-weight: 600;">Negative Impact on HDI</span>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=top_negative.values,
                y=[name.replace('_', ' ')[:30] for name in top_negative.index],
                orientation='h',
                marker_color='#EF4444',
                text=[f'{v:.2f}' for v in top_negative.values],
                textposition='outside',
                textfont={'color': '#E2E8F0'}
            )
        ])
        
        fig.update_layout(
            xaxis_title="Correlation Coefficient",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=380,
            xaxis_range=[-0.8, 0.1],
            margin=dict(l=10, r=10)
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    insight_box("<strong>Insight:</strong> Life expectancy, literacy, and internet access are the strongest predictors of HDI. Warfare and import dependency negatively impact development.")
    
    st.markdown("---")
    
    # ========== 4. Education & Health ==========
    subsection_header(4, "The Education-Health Connection", "#22C55E")
    
    if 'Life_Expectancy_years' in df.columns and 'Literacy_Rate_pct' in df.columns:
        fig = px.scatter(
            df_copy,
            x='Literacy_Rate_pct',
            y='Life_Expectancy_years',
            size='HDI_Index',
            color='HDI_Category',
            color_discrete_map={'Low': '#EF4444', 'Medium': '#F59E0B', 'High': '#22C55E', 'Very High': '#10B981'},
            title="Literacy Rate vs Life Expectancy (Bubble Size = HDI)"
        )
        
        fig.update_layout(
            xaxis_title="Literacy Rate (%)",
            yaxis_title="Life Expectancy (Years)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=400
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        corr = df['Literacy_Rate_pct'].corr(df['Life_Expectancy_years'])
        insight_box(f"<strong>Insight:</strong> Literacy and life expectancy correlation is <strong>{corr:.2f}</strong>. Educated populations live longer—they make better health choices and demand better healthcare.")
    
    st.markdown("---")
    
    # ========== 5. HDI by Key Metrics ==========
    subsection_header(5, "Development Profile by Category", "#22C55E")
    
    metrics = ['GDP_per_Capita_USD', 'Life_Expectancy_years', 'Literacy_Rate_pct', 'Internet_Access_pct', 'Medical_Doctors_per_1000']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if available_metrics:
        avg_by_category = df_copy.groupby('HDI_Category')[available_metrics].mean()
        
        # Normalize for radar chart
        normalized = avg_by_category.copy()
        for col in normalized.columns:
            normalized[col] = (normalized[col] - normalized[col].min()) / (normalized[col].max() - normalized[col].min() + 0.001)
        
        fig = go.Figure()
        
        colors = {'Low': '#EF4444', 'Medium': '#F59E0B', 'High': '#22C55E', 'Very High': '#10B981'}
        
        for category in ['Low', 'Medium', 'High', 'Very High']:
            if category in normalized.index:
                values = normalized.loc[category].tolist()
                values.append(values[0])  # Close the radar
                
                labels = [m.replace('_', ' ')[:15] for m in available_metrics]
                labels.append(labels[0])
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself',
                    name=category,
                    line_color=colors[category],
                    opacity=0.7
                ))
        
        fig.update_layout(
            title="Normalized Indicators by HDI Category",
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], gridcolor='rgba(71, 85, 105, 0.3)'),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        insight_box("<strong>Insight:</strong> Very High HDI countries excel across all dimensions. The gap between Low and Very High is most pronounced in GDP and internet access.")
    
    st.markdown("---")
    
    # Deep Dive Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <a href="{HDI_COLAB_LINK}" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); padding: 14px 24px; 
                        border-radius: 12px; text-align: center; cursor: pointer; 
                        display: flex; align-items: center; justify-content: center; gap: 10px;">
                {lucide_icon("flask", 20, "#FFFFFF")}
                <span style="color: white; font-weight: 600;">Deep Dive: HDI Model Training Notebook</span>
            </div>
        </a>
        """, unsafe_allow_html=True)


# ============================================================
# HAPPINESS ANALYSIS SECTION
# ============================================================
def display_happiness_analysis(df: pd.DataFrame):
    """Display comprehensive Happiness Index analysis with insights"""
    
    section_header("smile", "Happiness Index Analysis", 
                   "Exploring what makes nations happy", "#EC4899")
    st.markdown("---")
    
    # Find happiness column
    happiness_col = 'Happiness_Index_Ordinal' if 'Happiness_Index_Ordinal' in df.columns else None
    
    if happiness_col is None:
        st.warning("Happiness Index column not found in dataset")
        return
    
    df_copy = df.copy()
    
    # Create happiness categories
    df_copy['Happiness_Category'] = pd.cut(
        df_copy[happiness_col],
        bins=[0, 2, 4, 6, 8],
        labels=['Unhappy (1-2)', 'Below Avg (3-4)', 'Above Avg (5-6)', 'Happy (7-8)']
    )
    
    # ========== 1. Happiness Distribution ==========
    subsection_header(1, "Global Happiness Distribution", "#EC4899")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart by level
        happiness_counts = df_copy[happiness_col].value_counts().sort_index()
        
        # Color gradient from red to green
        colors = ['#EF4444', '#F97316', '#F59E0B', '#EAB308', '#84CC16', '#22C55E', '#10B981', '#059669']
        bar_colors = [colors[int(x)-1] if int(x) <= 8 else colors[-1] for x in happiness_counts.index]
        
        fig = go.Figure(data=[
            go.Bar(
                x=[f'Level {int(x)}' for x in happiness_counts.index],
                y=happiness_counts.values,
                marker_color=bar_colors,
                text=happiness_counts.values,
                textposition='outside',
                textfont={'color': '#E2E8F0'}
            )
        ])
        
        fig.update_layout(
            title="Countries by Happiness Level",
            xaxis_title="Happiness Level",
            yaxis_title="Number of Countries",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=350
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Donut chart by category
        category_counts = df_copy['Happiness_Category'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            hole=0.45,
            marker_colors=['#EF4444', '#F59E0B', '#22C55E', '#10B981'],
            textinfo='percent+label',
            textfont={'color': '#E2E8F0', 'size': 11}
        )])
        
        fig.update_layout(
            title="Countries by Happiness Category",
            paper_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    avg_happiness = df_copy[happiness_col].mean()
    happy_pct = ((df_copy[happiness_col] >= 5).sum() / len(df_copy)) * 100
    
    insight_box(f"<strong>Insight:</strong> Average global happiness is <strong>{avg_happiness:.1f}/8</strong>. About <strong>{happy_pct:.1f}%</strong> of countries report above-average happiness (level 5+).", "smile", "#EC4899")
    
    st.markdown("---")
    
    # ========== 2. HDI vs Happiness ==========
    subsection_header(2, "Does Development Equal Happiness?", "#EC4899")
    
    if 'HDI_Index' in df.columns:
        fig = px.scatter(
            df_copy,
            x='HDI_Index',
            y=happiness_col,
            color='Happiness_Category',
            color_discrete_map={
                'Unhappy (1-2)': '#EF4444',
                'Below Avg (3-4)': '#F59E0B',
                'Above Avg (5-6)': '#22C55E',
                'Happy (7-8)': '#10B981'
            },
            trendline="ols",
            title="HDI vs Happiness Level"
        )
        
        fig.update_layout(
            xaxis_title="HDI Index",
            yaxis_title="Happiness Level",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=400
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        corr = df['HDI_Index'].corr(df[happiness_col])
        insight_box(f"<strong>Insight:</strong> HDI-Happiness correlation is <strong>{corr:.2f}</strong>. Development is necessary but not sufficient for happiness—governance, freedom, and social support also matter.", "activity", "#EC4899")
    
    st.markdown("---")
    
    # ========== 3. Happiness Drivers ==========
    subsection_header(3, "What Makes People Happy?", "#EC4899")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if happiness_col in numeric_cols:
        numeric_cols.remove(happiness_col)
    
    correlations = df[numeric_cols + [happiness_col]].corr()[happiness_col].drop(happiness_col).sort_values()
    
    top_positive = correlations.tail(8).sort_values(ascending=True)
    top_negative = correlations.head(5).sort_values(ascending=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            {lucide_icon("laugh", 20, "#22C55E")}
            <span style="color: #E2E8F0; font-weight: 600;">Happiness Boosters</span>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=top_positive.values,
                y=[name.replace('_', ' ')[:28] for name in top_positive.index],
                orientation='h',
                marker_color='#22C55E',
                text=[f'{v:.2f}' for v in top_positive.values],
                textposition='outside',
                textfont={'color': '#E2E8F0'}
            )
        ])
        
        fig.update_layout(
            xaxis_title="Correlation",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=380,
            xaxis_range=[0, 1.1],
            margin=dict(l=10, r=10)
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            {lucide_icon("frown", 20, "#EF4444")}
            <span style="color: #E2E8F0; font-weight: 600;">Happiness Detractors</span>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=top_negative.values,
                y=[name.replace('_', ' ')[:28] for name in top_negative.index],
                orientation='h',
                marker_color='#EF4444',
                text=[f'{v:.2f}' for v in top_negative.values],
                textposition='outside',
                textfont={'color': '#E2E8F0'}
            )
        ])
        
        fig.update_layout(
            xaxis_title="Correlation",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=380,
            xaxis_range=[-0.8, 0.1],
            margin=dict(l=10, r=10)
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    insight_box("<strong>Insight:</strong> Economic prosperity (GDP), health (life expectancy), and connectivity (internet) boost happiness. Conflict and high import dependency decrease it.", "zap", "#EC4899")
    
    st.markdown("---")
    
    # ========== 4. Money & Happiness ==========
    subsection_header(4, "Can Money Buy Happiness?", "#EC4899")
    
    if 'GDP_per_Capita_USD' in df.columns:
        fig = px.scatter(
            df_copy,
            x='GDP_per_Capita_USD',
            y=happiness_col,
            color='Happiness_Category',
            size='Life_Expectancy_years' if 'Life_Expectancy_years' in df.columns else None,
            color_discrete_map={
                'Unhappy (1-2)': '#EF4444',
                'Below Avg (3-4)': '#F59E0B',
                'Above Avg (5-6)': '#22C55E',
                'Happy (7-8)': '#10B981'
            },
            title="GDP per Capita vs Happiness (Size = Life Expectancy)"
        )
        
        fig.update_layout(
            xaxis_title="GDP per Capita (USD)",
            yaxis_title="Happiness Level",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=400
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate threshold insight
        high_gdp = df_copy[df_copy['GDP_per_Capita_USD'] > 40000][happiness_col].mean()
        low_gdp = df_copy[df_copy['GDP_per_Capita_USD'] < 10000][happiness_col].mean()
        
        insight_box(f"<strong>Insight:</strong> Countries with GDP > $40K average <strong>{high_gdp:.1f}</strong> happiness vs <strong>{low_gdp:.1f}</strong> for GDP < $10K. Money helps, but diminishing returns kick in after basic needs are met.", "dollar-sign", "#EC4899")
    
    st.markdown("---")
    
    # ========== 5. Happiness Heatmap ==========
    subsection_header(5, "Average Indicators by Happiness Level", "#EC4899")
    
    indicator_cols = ['GDP_per_Capita_USD', 'Life_Expectancy_years', 'Literacy_Rate_pct', 
                      'Internet_Access_pct', 'Unemployment_Rate_pct', 'Gender_Equality_Index']
    available_cols = [c for c in indicator_cols if c in df.columns]
    
    if available_cols:
        # Group by happiness level
        grouped = df_copy.groupby(happiness_col)[available_cols].mean()
        
        # Create line chart for each indicator
        fig = go.Figure()
        
        colors = ['#6366F1', '#8B5CF6', '#A855F7', '#EC4899', '#F43F5E', '#22C55E']
        
        for idx, col in enumerate(available_cols):
            # Normalize values for comparison
            values = grouped[col]
            normalized = (values - values.min()) / (values.max() - values.min() + 0.001) * 100
            
            fig.add_trace(go.Scatter(
                x=grouped.index,
                y=normalized,
                mode='lines+markers',
                name=col.replace('_', ' ')[:20],
                line=dict(color=colors[idx % len(colors)], width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="How Indicators Change with Happiness (Normalized)",
            xaxis_title="Happiness Level",
            yaxis_title="Normalized Value (%)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': '#E2E8F0'},
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        insight_box("<strong>Insight:</strong> All positive indicators rise with happiness level. Notice unemployment drops as happiness increases—job security is crucial for well-being.", "trending-up", "#EC4899")
    
    st.markdown("---")
    
    # Deep Dive Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <a href="{HAPPINESS_COLAB_LINK}" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(90deg, #EC4899, #DB2777); padding: 14px 24px; 
                        border-radius: 12px; text-align: center; cursor: pointer; 
                        display: flex; align-items: center; justify-content: center; gap: 10px;">
                {lucide_icon("flask", 20, "#FFFFFF")}
                <span style="color: white; font-weight: 600;">Deep Dive: Happiness Model Training Notebook</span>
            </div>
        </a>
        """, unsafe_allow_html=True)


# ============================================================
# ENHANCED DATA SUMMARY
# ============================================================
def display_data_summary(df: pd.DataFrame):
    """Display enhanced data summary with meaningful insights"""
    
    section_header("clipboard-list", "Data Summary & Feature Analysis for PreProcessed Data", 
                   "Deep dive into the structure, quality, and characteristics of our dataset", "#8B5CF6")
    st.markdown("---")
    
    # ========== 1. QUICK STATS OVERVIEW ==========
    st.markdown(f"""
    <h3 style="color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon("target", 22, "#8B5CF6")}
        <span>Quick Stats Overview</span>
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    missing_total = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    completeness = (1 - missing_total / total_cells) * 100
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1)); 
                    padding: 16px; border-radius: 12px; border-left: 4px solid #6366F1; text-align: center;">
            <div style="margin-bottom: 8px;">{lucide_icon("folder", 22, "#6366F1")}</div>
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Records</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0;">{len(df):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.1)); 
                    padding: 16px; border-radius: 12px; border-left: 4px solid #10B981; text-align: center;">
            <div style="margin-bottom: 8px;">{lucide_icon("bar-chart-2", 22, "#10B981")}</div>
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Features</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0;">{len(df.columns)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.1)); 
                    padding: 16px; border-radius: 12px; border-left: 4px solid #F59E0B; text-align: center;">
            <div style="margin-bottom: 8px;">{lucide_icon("hash", 22, "#F59E0B")}</div>
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Numeric</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0;">{len(numeric_cols)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.15), rgba(219, 39, 119, 0.1)); 
                    padding: 16px; border-radius: 12px; border-left: 4px solid #EC4899; text-align: center;">
            <div style="margin-bottom: 8px;">{lucide_icon("check-circle", 22, "#EC4899")}</div>
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Complete</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0;">{completeness:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(124, 58, 237, 0.1)); 
                    padding: 16px; border-radius: 12px; border-left: 4px solid #8B5CF6; text-align: center;">
            <div style="margin-bottom: 8px;">{lucide_icon("hard-drive", 22, "#8B5CF6")}</div>
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem;">Memory</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0;">{memory_mb:.2f} MB</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== 2. FEATURE CATEGORIES ==========
    st.markdown(f"""
    <h3 style="color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon("folder-open", 22, "#8B5CF6")}
        <span>Feature Categories</span>
    </h3>
    <p style="color: #94A3B8; margin-left: 32px; font-style: italic;">Features organized by their domain for better understanding</p>
    """, unsafe_allow_html=True)
    
    # Define feature categories with icons
    feature_categories = {
        "Target Variables": {
            "features": ['HDI_Index', 'Happiness_Index_Ordinal'],
            "color": "#6366F1",
            "icon": "target",
            "description": "Variables we're predicting"
        },
        "Economic Indicators": {
            "features": ['GDP_per_Capita_USD', 'Unemployment_Rate_pct', 'Inflation_Rate_pct', 
                        'Import_Percentage_of_GDP', 'Export_Percentage_of_GDP', 'Trade_Balance_USD'],
            "color": "#10B981",
            "icon": "dollar-sign",
            "description": "Financial and trade metrics"
        },
        "Health Metrics": {
            "features": ['Life_Expectancy_years', 'Infant_Mortality_per_1000', 'Medical_Doctors_per_1000',
                        'Healthcare_Expenditure_GDP_pct', 'Access_to_Clean_Water_pct'],
            "color": "#F59E0B",
            "icon": "heart",
            "description": "Population health indicators"
        },
        "Education & Knowledge": {
            "features": ['Literacy_Rate_pct', 'Mean_Years_of_Schooling', 'Expected_Years_of_Schooling',
                        'Internet_Access_pct', 'Mobile_Subscriptions_per_100'],
            "color": "#EC4899",
            "icon": "graduation-cap",
            "description": "Education and digital access"
        },
        "Social & Demographics": {
            "features": ['Population', 'Population_Density_per_km2', 'Urban_Population_pct',
                        'Gender_Equality_Index', 'Age_Dependency_Ratio'],
            "color": "#8B5CF6",
            "icon": "users",
            "description": "Population characteristics"
        },
        "Governance & Stability": {
            "features": ['Government_Expenditure_pct_GDP', 'Military_Expenditure_pct_GDP',
                        'Political_Stability_Index', 'Corruption_Perception_Index', 'Wars_Conflicts_Last_Decade'],
            "color": "#EF4444",
            "icon": "shield",
            "description": "Government and stability metrics"
        },
        "Environment & Resources": {
            "features": ['CO2_Emissions_per_Capita', 'Renewable_Energy_pct', 'Agriculture_pct_GDP',
                        'Arable_Land_pct', 'Energy_Consumption_per_Capita'],
            "color": "#22C55E",
            "icon": "leaf",
            "description": "Environmental indicators"
        }
    }
    
    # Create category cards
    cols = st.columns(3)
    col_idx = 0
    
    for category, info in feature_categories.items():
        available_features = [f for f in info['features'] if f in df.columns]
        
        if available_features:
            with cols[col_idx % 3]:
                feature_list = "<br>".join([f"• {f.replace('_', ' ')}" for f in available_features[:5]])
                more_text = f"<br><i style='color: #64748B;'>+{len(available_features) - 5} more...</i>" if len(available_features) > 5 else ""
                
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.5); padding: 16px; border-radius: 12px; 
                            border-top: 3px solid {info['color']}; margin-bottom: 16px; min-height: 220px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        {lucide_icon(info['icon'], 20, info['color'])}
                        <h4 style="margin: 0; color: #E2E8F0;">{category}</h4>
                    </div>
                    <p style="margin: 0 0 10px 0; color: #64748B; font-size: 0.8rem;">{info['description']}</p>
                    <span style="background: {info['color']}22; color: {info['color']}; padding: 2px 8px; 
                           border-radius: 10px; font-size: 0.75rem;">{len(available_features)} features</span>
                    <p style="margin: 10px 0 0 0; color: #94A3B8; font-size: 0.85rem; line-height: 1.6;">
                        {feature_list}{more_text}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                col_idx += 1
    

    st.markdown("---")
    
    # ========== 3. FEATURE STATISTICS EXPLORER ==========
    st.markdown(f"""
    <h3 style="color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon("pie-chart", 22, "#8B5CF6")}
        <span>Feature Statistics Explorer</span>
    </h3>
    """, unsafe_allow_html=True)
    
    # Numeric features detailed stats
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) > 0:
        # Create enhanced statistics
        stats_data = []
        for col in numeric_df.columns:
            col_data = numeric_df[col].dropna()
            if len(col_data) > 0:
                q1 = col_data.quantile(0.25)
                q3 = col_data.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers = ((col_data < lower_bound) | (col_data > upper_bound)).sum()
                
                stats_data.append({
                    'Feature': col.replace('_', ' ')[:25],
                    'Min': col_data.min(),
                    'Max': col_data.max(),
                    'Mean': col_data.mean(),
                    'Median': col_data.median(),
                    'Std': col_data.std(),
                    'Skewness': col_data.skew(),
                    'Outliers': outliers
                })
        
        stats_df = pd.DataFrame(stats_data)
        
        # Distribution type indicators
        st.markdown(f"""
        <h4 style="color: #E2E8F0; display: flex; align-items: center; gap: 8px; margin-top: 16px;">
            {lucide_icon("activity", 18, "#94A3B8")}
            <span>Distribution Characteristics</span>
        </h4>
        """, unsafe_allow_html=True)
        
        # Show top skewed features
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                {lucide_icon("trending-up", 18, "#F59E0B")}
                <span style="color: #E2E8F0; font-weight: 600;">Most Right-Skewed Features</span>
            </div>
            """, unsafe_allow_html=True)
            
            right_skewed = stats_df.nlargest(5, 'Skewness')[['Feature', 'Skewness']]
            for _, row in right_skewed.iterrows():
                skew_color = '#EF4444' if abs(row['Skewness']) > 2 else '#F59E0B' if abs(row['Skewness']) > 1 else '#22C55E'
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px 12px; 
                            background: rgba(30, 41, 59, 0.3); border-radius: 6px; margin: 4px 0;
                            border-left: 3px solid {skew_color};">
                    <span style="color: #E2E8F0;">{row['Feature']}</span>
                    <span style="color: {skew_color}; font-weight: 600;">{row['Skewness']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                {lucide_icon("trending-down", 18, "#6366F1")}
                <span style="color: #E2E8F0; font-weight: 600;">Most Left-Skewed Features</span>
            </div>
            """, unsafe_allow_html=True)
            
            left_skewed = stats_df.nsmallest(5, 'Skewness')[['Feature', 'Skewness']]
            for _, row in left_skewed.iterrows():
                skew_color = '#EF4444' if abs(row['Skewness']) > 2 else '#F59E0B' if abs(row['Skewness']) > 1 else '#22C55E'
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px 12px; 
                            background: rgba(30, 41, 59, 0.3); border-radius: 6px; margin: 4px 0;
                            border-left: 3px solid {skew_color};">
                    <span style="color: #E2E8F0;">{row['Feature']}</span>
                    <span style="color: {skew_color}; font-weight: 600;">{row['Skewness']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Features with most outliers
        st.markdown(f"""
        <h4 style="color: #E2E8F0; display: flex; align-items: center; gap: 8px; margin-top: 24px;">
            {lucide_icon("alert-triangle", 18, "#F59E0B")}
            <span>Features with Most Outliers</span>
        </h4>
        """, unsafe_allow_html=True)
        
        outlier_features = stats_df.nlargest(8, 'Outliers')[['Feature', 'Outliers', 'Min', 'Max', 'Mean']]
        
        if outlier_features['Outliers'].sum() > 0:
            fig = go.Figure(data=[
                go.Bar(
                    x=outlier_features['Feature'],
                    y=outlier_features['Outliers'],
                    marker_color='#F59E0B',
                    text=outlier_features['Outliers'],
                    textposition='outside',
                    textfont={'color': '#E2E8F0'}
                )
            ])
            
            fig.update_layout(
                xaxis_title="Feature",
                yaxis_title="Number of Outliers",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': '#E2E8F0'},
                height=300
            )
            fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)', tickangle=45)
            fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); padding: 16px; border-radius: 12px; 
                        display: flex; align-items: center; gap: 12px;">
                {lucide_icon("check-circle", 24, "#10B981")}
                <span style="color: #10B981;">No significant outliers detected using IQR method!</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== 5. CORRELATION HIGHLIGHTS ==========
    st.markdown(f"""
    <h3 style="color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon("link-2", 22, "#6366F1")}
        <span>Key Correlations</span>
    </h3>
    """, unsafe_allow_html=True)
    
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr()
        
        # Get top correlations (excluding self-correlations)
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Feature 1': corr_matrix.columns[i],
                    'Feature 2': corr_matrix.columns[j],
                    'Correlation': corr_matrix.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        corr_df['Abs_Corr'] = corr_df['Correlation'].abs()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                {lucide_icon("flame", 18, "#22C55E")}
                <span style="color: #E2E8F0; font-weight: 600;">Strongest Positive Correlations</span>
            </div>
            """, unsafe_allow_html=True)
            
            top_positive = corr_df.nlargest(6, 'Correlation')[['Feature 1', 'Feature 2', 'Correlation']]
            
            for _, row in top_positive.iterrows():
                f1 = row['Feature 1'].replace('_', ' ')[:20]
                f2 = row['Feature 2'].replace('_', ' ')[:20]
                corr = row['Correlation']
                width = int(abs(corr) * 100)
                
                st.markdown(f"""
                <div style="padding: 10px; background: rgba(30, 41, 59, 0.3); border-radius: 8px; margin: 6px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="color: #94A3B8; font-size: 0.85rem;">{f1} ↔ {f2}</span>
                        <span style="color: #22C55E; font-weight: 600;">{corr:.3f}</span>
                    </div>
                    <div style="background: rgba(71, 85, 105, 0.3); height: 6px; border-radius: 3px;">
                        <div style="background: linear-gradient(90deg, #22C55E, #10B981); height: 100%; 
                                    width: {width}%; border-radius: 3px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                {lucide_icon("snowflake", 18, "#EF4444")}
                <span style="color: #E2E8F0; font-weight: 600;">Strongest Negative Correlations</span>
            </div>
            """, unsafe_allow_html=True)
            
            top_negative = corr_df.nsmallest(6, 'Correlation')[['Feature 1', 'Feature 2', 'Correlation']]
            
            for _, row in top_negative.iterrows():
                f1 = row['Feature 1'].replace('_', ' ')[:20]
                f2 = row['Feature 2'].replace('_', ' ')[:20]
                corr = row['Correlation']
                width = int(abs(corr) * 100)
                
                st.markdown(f"""
                <div style="padding: 10px; background: rgba(30, 41, 59, 0.3); border-radius: 8px; margin: 6px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="color: #94A3B8; font-size: 0.85rem;">{f1} ↔ {f2}</span>
                        <span style="color: #EF4444; font-weight: 600;">{corr:.3f}</span>
                    </div>
                    <div style="background: rgba(71, 85, 105, 0.3); height: 6px; border-radius: 3px;">
                        <div style="background: linear-gradient(90deg, #EF4444, #F97316); height: 100%; 
                                    width: {width}%; border-radius: 3px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Correlation insight
        highly_correlated = len(corr_df[corr_df['Abs_Corr'] > 0.8])
        insight_box(f"<strong>Insight:</strong> Found <strong>{highly_correlated}</strong> feature pairs with correlation > 0.8. Consider removing redundant features or using regularization to handle multicollinearity.", "info", "#6366F1")
    
    st.markdown("---")
    
    # ========== 6. INTERACTIVE FEATURE EXPLORER ==========
    st.markdown(f"""
    <h3 style="color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon("search", 22, "#EC4899")}
        <span>Interactive Feature Explorer</span>
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_feature = st.selectbox(
            "Select a feature to explore:",
            options=df.columns.tolist(),
            format_func=lambda x: x.replace('_', ' ')
        )
    
    if selected_feature:
        feature_data = df[selected_feature].dropna()
        
        with col2:
            if df[selected_feature].dtype in ['int64', 'float64']:
                # Numeric feature
                fig = make_subplots(rows=1, cols=2, subplot_titles=('Distribution', 'Box Plot'))
                
                fig.add_trace(
                    go.Histogram(x=feature_data, marker_color='#6366F1', opacity=0.7, nbinsx=30),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Box(y=feature_data, marker_color='#6366F1', boxpoints='outliers'),
                    row=1, col=2
                )
                
                fig.update_layout(
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': '#E2E8F0'},
                    height=300
                )
                fig.update_xaxes(gridcolor='rgba(71, 85, 105, 0.3)')
                fig.update_yaxes(gridcolor='rgba(71, 85, 105, 0.3)')
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Categorical feature
                value_counts = feature_data.value_counts().head(10)
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=value_counts.index.astype(str),
                        y=value_counts.values,
                        marker_color='#6366F1'
                    )
                ])
                
                fig.update_layout(
                    title=f"Top 10 Values for {selected_feature.replace('_', ' ')}",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': '#E2E8F0'},
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Feature details
        st.markdown(f"""
        <h4 style="color: #E2E8F0; display: flex; align-items: center; gap: 8px; margin-top: 16px;">
            {lucide_icon("clipboard", 18, "#94A3B8")}
            <span>Feature Details</span>
        </h4>
        """, unsafe_allow_html=True)
        
        detail_cols = st.columns(4)
        
        with detail_cols[0]:
            st.metric("Data Type", str(df[selected_feature].dtype))
        with detail_cols[1]:
            st.metric("Non-Null Count", f"{feature_data.shape[0]:,}")
        with detail_cols[2]:
            st.metric("Unique Values", f"{df[selected_feature].nunique():,}")
        with detail_cols[3]:
            missing_pct = (df[selected_feature].isnull().sum() / len(df)) * 100
            st.metric("Missing %", f"{missing_pct:.2f}%")
        
        if df[selected_feature].dtype in ['int64', 'float64']:
            desc_cols = st.columns(6)
            desc = feature_data.describe()
            desc_cols[0].metric("Min", f"{desc['min']:.4g}")
            desc_cols[1].metric("Max", f"{desc['max']:.4g}")
            desc_cols[2].metric("Mean", f"{desc['mean']:.4g}")
            desc_cols[3].metric("Median", f"{desc['50%']:.4g}")
            desc_cols[4].metric("Std Dev", f"{desc['std']:.4g}")
            desc_cols[5].metric("Skewness", f"{feature_data.skew():.4g}")
    
    st.markdown("---")
    
    # ========== 7. SAMPLE DATA WITH FILTERS ==========
    st.markdown(f"""
    <h3 style="color: #E2E8F0; display: flex; align-items: center; gap: 10px;">
        {lucide_icon("file-text", 22, "#22C55E")}
        <span>Data Preview</span>
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        n_rows = st.slider("Number of rows", min_value=5, max_value=50, value=10)
    
    with col2:
        preview_type = st.radio("Preview type", ["First rows", "Random sample", "Last rows"], horizontal=True)
    
    if preview_type == "First rows":
        preview_df = df.head(n_rows)
    elif preview_type == "Random sample":
        preview_df = df.sample(min(n_rows, len(df)))
    else:
        preview_df = df.tail(n_rows)
    
    # Style the dataframe
    st.dataframe(
        preview_df.style.format(precision=3).set_properties(**{
            'background-color': 'rgba(30, 41, 59, 0.5)',
            'color': '#E2E8F0'
        }),
        use_container_width=True,
        height=min(400, (n_rows + 1) * 35)
    )
    
    # Download button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        csv = df.to_csv(index=False)
        st.markdown(f"""
        <div style="margin-top: 16px;">
        """, unsafe_allow_html=True)
        st.download_button(
            label=f"Download Full Dataset (CSV)",
            data=csv,
            file_name="dataset_export.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# MAIN COMPREHENSIVE ANALYSIS
# ============================================================
def display_comprehensive_analysis(df: pd.DataFrame):
    """Display comprehensive dataset analysis"""
    
    st.markdown("---")
    
    # Dataset Overview
    display_dataset_overview(df)
    
    st.markdown("---")
    
    # Create custom tab styling
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #94A3B8;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.2);
        color: #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs([
        "📈 HDI Analysis",
        "😊 Happiness Analysis", 
        "📋 Data Summary"
    ])
    
    with tab1:
        display_hdi_analysis(df)
    
    with tab2:
        display_happiness_analysis(df)
    
    with tab3:
        display_data_summary(df)