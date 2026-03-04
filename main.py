import os

from lib.setup_logging import logging
from lib.adjacency_matrix import read_adjacency_matrix_excel
from lib.needs_vector import read_needs_vector_excel
from lib.matching import matching_adj_matrix_and_needs_vector
from lib.p_median_count import read_p_median_count
from lib.graph import create_graph # type: ignore
from lib.algorithms.p_median_interface import PMedianAlgorithm
from lib.algorithms.local_search.local_search import PMedianLocalSearch

#Название файлов
adjacency_matrix_file_name = 'adjacency_matrix.xlsx'
needs_vector_file_name = 'needs_vector.xlsx'
input_p_file_name = "input_p.json"

#Пути до файлов
CURRENT_PATH: str = os.path.dirname(__file__)
INPUT_PATH = os.path.join(CURRENT_PATH, 'input')
INPUT_ADJ_FILE_NAME = os.path.join(INPUT_PATH, adjacency_matrix_file_name)
INPUT_NV_FILE_NAME = os.path.join(INPUT_PATH, needs_vector_file_name)
INPUT_P_FILE_NAME = os.path.join(INPUT_PATH, input_p_file_name)

def main(algorithm: PMedianAlgorithm) -> None:
    try:

        logging.info(f"Начало считывания {INPUT_ADJ_FILE_NAME}")
        adjacency_matrix_df, indx_stations_matrix = read_adjacency_matrix_excel(INPUT_ADJ_FILE_NAME)
        logging.info(f"Считывание файла {INPUT_ADJ_FILE_NAME} прошло успешно!\n\n")

        logging.info(f"Начало считывания {INPUT_NV_FILE_NAME}")
        needs_vector_df, indx_station_vector = read_needs_vector_excel(INPUT_NV_FILE_NAME)
        logging.info(f"Считывание файла {INPUT_NV_FILE_NAME} прошло успешно!\n\n")

        logging.info(f"Начало считывания {INPUT_P_FILE_NAME}")
        p: int= read_p_median_count(INPUT_P_FILE_NAME)
        logging.info(f"Считывание файла {INPUT_P_FILE_NAME} прошло успешно!\n\n")

        logging.info(f"Начало проверки матрицы смежности, вектора потребностей и количества p-медиан")
        matching_adj_matrix_and_needs_vector(indx_stations_matrix, indx_station_vector, p)
        logging.info(f"Проверка матрицы смежности, вектора потребностей и количества p-медиан прошла успешно!\n\n")

        logging.info(f"Начало создания графа")
        graph = create_graph(adjacency_matrix_df) # type: ignore
        logging.info(f"Граф успешно создан!\n\n")

        logging.info(f"Начало расчета")
        list_p_median_with_ids, distance = algorithm.search(graph, p, needs_vector_df, adjacency_matrix_df) # type: ignore
        logging.info(f"Конец расчета\n\n")

        list_p_median_with_names = [indx_station_vector[p_median_id] for p_median_id in list_p_median_with_ids]

        logging.info(f"====> ИТОГ: p-median: {list_p_median_with_names}, sum distance: {distance}")
        

    except FileNotFoundError:
        logging.error(f"Файл не найден")
        return None
    except ValueError as e:
        logging.error(f"Ошибка валидации: {e}")
        return None
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")
        return None
        

if __name__ == "__main__":

    p_median_local_search_alg = PMedianLocalSearch()

    main(p_median_local_search_alg)
