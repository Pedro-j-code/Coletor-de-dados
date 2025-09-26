import pandas as pd
from src.scraper import MovieScraper
from src.utils import setup_logging
import logging
import os

def main():
    """Função principal do coletor de filmes"""
   
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Iniciando coleta de dados de filmes...")
        
     
        scraper = MovieScraper()
        
  
        movies_data = scraper.scrape_popular_movies()
        
        if movies_data:
         
            df = pd.DataFrame(movies_data)
            
            
            os.makedirs('data', exist_ok=True)
            
          
            csv_path = 'data/movies.csv'
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            logger.info(f"Dados salvos com sucesso em {csv_path}")
            logger.info(f"Total de filmes coletados: {len(df)}")
            
           
            print("\nPreview dos dados coletados:")
            print(df.head())
            
        else:
            logger.warning("Nenhum dado foi coletado")
            
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    main()