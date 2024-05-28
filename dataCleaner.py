import os
import shutil
from datetime import datetime

class DirectoryCleaner:
    """
    Clase para explorar y limpiar directorios basados en su tiempo de modificación.

    Esta clase proporciona métodos para explorar directorios, calcular la edad de los directorios
    y eliminar aquellos que superan un umbral de tiempo especificado.
    """

    def __init__(self, base_path: str, subdirectory: str = "tempUserData", age_threshold: int = 10):
        """
        Inicializa una instancia de DirectoryCleaner.

        Args:
            base_path (str): La ruta base donde se encuentra el script.
            subdirectory (str, optional): El subdirectorio que se explorará. Por defecto es "tempUserData".
            age_threshold (int, optional): El umbral de edad en minutos para eliminar directorios. Por defecto es 10 minutos.
        """
        self.base_path = base_path
        self.directory_path = os.path.join(base_path, subdirectory)
        self.age_threshold = age_threshold

    def explore_and_clean_directories(self):
        """
        Explora el subdirectorio especificado, imprime información sobre cada directorio y elimina aquellos
        que superen el umbral de tiempo de modificación.
        """
        print("Explorando directorios en:", self.directory_path)

        # Itera sobre los elementos en el directorio
        for item in os.listdir(self.directory_path):
            # Construye la ruta completa del elemento
            item_path = os.path.join(self.directory_path, item)
            # Verifica si es un directorio
            if os.path.isdir(item_path):
                # Obtiene la fecha de la última modificación
                mod_time = os.path.getmtime(item_path)
                # Convierte la fecha de modificación en un formato legible
                mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                # Calcula la antigüedad del directorio en minutos
                age_minutes = int((datetime.now() - datetime.fromtimestamp(mod_time)).total_seconds() / 60)
                # Verifica si la antigüedad es mayor que el umbral especificado
                if age_minutes > self.age_threshold:
                    # Elimina el directorio y su contenido
                    shutil.rmtree(item_path)
                print(f"Directorio: {item}, Última Modificación: {mod_time_str}, Antigüedad: {age_minutes} minutos")

if __name__ == "__main__":
    # Obtiene la ruta absoluta del script actual
    parent_directory_path = os.path.dirname(os.path.abspath(__file__))
    # Crea una instancia de DirectoryCleaner
    cleaner = DirectoryCleaner(parent_directory_path)
    # Explora y limpia los directorios según el umbral de tiempo especificado
    cleaner.explore_and_clean_directories()
