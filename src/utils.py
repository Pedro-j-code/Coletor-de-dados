import logging
import sys
import os

def setup_logging():
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_requirements():
    """Verifica se todas as dependências estão instaladas"""
    required_packages = ['requests', 'beautifulsoup4', 'pandas', 'lxml']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            return False, f"Pacote {package} não instalado"
    
    return True, "Todos os pacotes estão instalados"