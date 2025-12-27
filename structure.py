"""
Project Structure Generator
Creates empty files and folders for ML Streamlit Application
"""

import os
from pathlib import Path
from datetime import datetime


def create_project_structure(project_name: str = "ml_streamlit_app", base_path: str = "."):
    """
    Creates the complete project structure with empty files and folders.
    
    Args:
        project_name: Name of the project folder
        base_path: Where to create the project
    """
    
    root = Path(base_path) / project_name
    
    # ========================================
    # DIRECTORY STRUCTURE
    # ========================================
    directories = [
        # App directories
        "app",
        "app/pages",
        "app/components",
        "app/models",
        "app/utils",
        "app/assets",
        "app/assets/images",
        
        # Model storage
        "saved_models",
        "saved_models/classification",
        "saved_models/regression",
        
        # Data
        "data",
        
        # Tests
        "tests",
        
        # Notebooks
        "notebooks",
        
        # Logs
        "logs",
        
        # Streamlit config
        ".streamlit",
    ]
    
    # ========================================
    # FILE STRUCTURE
    # ========================================
    files = [
        # Root config files
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "pyproject.toml",
        "Dockerfile",
        "docker-compose.yml",
        "README.md",
        
        # Streamlit config
        ".streamlit/config.toml",
        
        # App - Main files
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        
        # App - Pages
        "app/pages/__init__.py",
        "app/pages/landing.py",
        "app/pages/hdi_prediction.py",
        "app/pages/happiness_prediction.py",
        
        # App - Components
        "app/components/__init__.py",
        "app/components/sidebar.py",
        "app/components/input_forms.py",
        "app/components/visualizations.py",
        "app/components/result_cards.py",
        "app/components/metrics.py",
        
        # App - Models
        "app/models/__init__.py",
        "app/models/model_loader.py",
        "app/models/predictor.py",
        "app/models/feature_engineering.py",
        
        # App - Utils
        "app/utils/__init__.py",
        "app/utils/validators.py",
        "app/utils/formatters.py",
        "app/utils/cache_manager.py",
        
        # App - Assets
        "app/assets/styles.css",
        
        # Saved Models - Placeholder files
        "saved_models/classification/.gitkeep",
        "saved_models/regression/.gitkeep",
        
        # Data
        "data/.gitkeep",
        "data/sample_dataset.csv",
        
        # Tests
        "tests/__init__.py",
        "tests/test_models.py",
        "tests/test_predictions.py",
        "tests/test_components.py",
        
        # Notebooks
        "notebooks/.gitkeep",
        
        # Logs
        "logs/.gitkeep",
    ]
    
    # ========================================
    # CREATE STRUCTURE
    # ========================================
    
    print(f"\n{'='*60}")
    print(f"🚀 Creating Project: {project_name}")
    print(f"📁 Location: {root.absolute()}")
    print(f"{'='*60}\n")
    
    # Create directories
    print("📁 Creating directories...")
    for dir_path in directories:
        full_path = root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {dir_path}/")
    
    print(f"\n📄 Creating files...")
    # Create files
    for file_path in files:
        full_path = root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.touch()
        print(f"   ✓ {file_path}")
    
    # ========================================
    # SUMMARY
    # ========================================
    print(f"\n{'='*60}")
    print(f"✅ Project structure created successfully!")
    print(f"{'='*60}")
    print(f"   📁 Directories: {len(directories)}")
    print(f"   📄 Files: {len(files)}")
    print(f"   📍 Location: {root.absolute()}")
    print(f"{'='*60}")
    
    print(f"""
📋 Next Steps:
   1. cd {project_name}
   2. python -m venv venv
   3. source venv/bin/activate  (or venv\\Scripts\\activate on Windows)
   4. pip install -r requirements.txt
   5. streamlit run app/main.py
""")
    
    return root


# ========================================
# RUN
# ========================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate ML Streamlit project structure")
    parser.add_argument(
        "--name", 
        type=str, 
        default="ml_streamlit_app",
        help="Project name (default: ml_streamlit_app)"
    )
    parser.add_argument(
        "--path", 
        type=str, 
        default=".",
        help="Base path for project (default: current directory)"
    )
    
    args = parser.parse_args()
    
    create_project_structure(project_name=args.name, base_path=args.path)