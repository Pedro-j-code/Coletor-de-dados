import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from time import sleep
import random

class MovieScraper:
    def __init__(self):
        self.base_url = "https://www.imdb.com/chart/moviemeter/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.logger = logging.getLogger(__name__)
    
    def get_page_content(self, url):
      
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Erro ao acessar {url}: {str(e)}")
            return None
    
    def parse_movie_data(self, html_content):
      
        soup = BeautifulSoup(html_content, 'html.parser')
        movies = []
        
       
        movie_list = soup.find('ul', class_='ipc-metadata-list') or soup.find('tbody', class_='lister-list')
        
        if not movie_list:
            self.logger.warning("Não foi possível encontrar a lista de filmes")
            return movies
        
        
        movie_items = movie_list.find_all('li', class_='ipc-metadata-list-summary-item') or movie_list.find_all('tr')
        
        for index, item in enumerate(movie_items[:50], 1):  
            try:
                movie_data = self.extract_movie_info(item, index)
                if movie_data:
                    movies.append(movie_data)
            except Exception as e:
                self.logger.warning(f"Erro ao extrair dados do filme {index}: {str(e)}")
                continue
        
        return movies
    
    def extract_movie_info(self, item, position):
        """Extrai informações específicas de cada filme"""
        try:
          
            title_element = item.find('h3', class_='ipc-title__text') or item.find('td', class_='titleColumn')
            if title_element:
                title = title_element.get_text(strip=True).split('. ')[-1] if '.' in title_element.get_text() else title_element.get_text(strip=True)
            else:
                return None
            
         
            year_element = item.find('span', class_='cli-title-metadata-item') or item.find('span', class_='secondaryInfo')
            year = year_element.get_text(strip=True).strip('()') if year_element else "N/A"
            
       
            rating_element = item.find('span', class_='ipc-rating-star') or item.find('td', class_='ratingColumn')
            rating = rating_element.get_text(strip=True).split()[0] if rating_element else "N/A"
            
            return {
                'position': position,
                'title': title,
                'year': year,
                'rating': rating
            }
            
        except Exception as e:
            self.logger.warning(f"Erro ao extrair informações do filme: {str(e)}")
            return None
    
    def scrape_popular_movies(self):
        """Método principal para coletar dados dos filmes populares"""
        self.logger.info("Acessando página de filmes populares...")
        
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            return None
        
        self.logger.info("Extraindo dados dos filmes...")
        movies_data = self.parse_movie_data(html_content)
        
        return movies_data


def get_sample_data():
    """Retorna dados de exemplo caso o scraping falhe"""
    return [
        {'position': 1, 'title': 'Duna: Parte Dois', 'year': '2024', 'rating': '8.7'},
        {'position': 2, 'title': 'Oppenheimer', 'year': '2023', 'rating': '8.3'},
        {'position': 3, 'title': 'Interestelar', 'year': '2014', 'rating': '8.7'},
        {'position': 4, 'title': 'O Poderoso Chefão', 'year': '1972', 'rating': '9.2'},
        {'position': 5, 'title': 'Um Sonho de Liberdade', 'year': '1994', 'rating': '9.3'}
    ]