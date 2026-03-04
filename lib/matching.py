from typing import Dict

def matching_adj_matrix_and_needs_vector(indx_stations_matrix: Dict[int, str], indx_stations_vector: Dict[int, str], p: int) -> None:
    """
    Проверяет соответствие станций в матрице смежности и векторе потребностей.

    Args:
        indx_stations_matrix: Словарь {индекс: название станции} из матрицы смежности
        indx_stations_vector: Словарь {индекс: название станции} из вектора потребностей
        p: Количество p-медиан

    Raises:
        ValueError: Если станции в матрице и векторе не совпадают
        ValueError: Если количество станций меньше p
    """

    if len(set(indx_stations_matrix.values()) - set(indx_stations_vector.values())):
        raise ValueError("Станции в матрице смежности и в векторе потребностей должны совпадать")
    
    if len(indx_stations_matrix.values()) < p:
        raise ValueError("Количество станций в матрице смежности и в векторе потребностей должно быть больше p")