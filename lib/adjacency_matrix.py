import pandas as pd
from typing import Dict, Tuple


def create_numeric_id_for_matrix(adjacency_matrix_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[int, str]]:
    """
    Преобразует строковые индексы и названия столбцов матрицы смежности в числовые идентификаторы.

    Функция создает отображение между исходными названиями станций и числовыми индексами,
    заменяет строковые индексы и названия столбцов на числовые.

    Args:
        adjacency_matrix_df (pd.DataFrame): Исходная матрица смежности со строковыми индексами

    Returns:
        Tuple[pd.DataFrame, Dict[int, str]]:
            - adjacency_matrix_df: Матрица смежности с числовыми индексами
            - indx_stations: Словарь {числовой_id: "название станции"}
    """
    stations_indx: Dict[str, int] = dict(zip(adjacency_matrix_df.index, range(len(adjacency_matrix_df.index))))
    indx_stations: Dict[int, str] = dict(zip(range(len(adjacency_matrix_df.index)), adjacency_matrix_df.index))

    adjacency_matrix_df.index = adjacency_matrix_df.index.map(stations_indx)
    adjacency_matrix_df.columns = adjacency_matrix_df.columns.map(stations_indx)

    return adjacency_matrix_df, indx_stations


def read_adjacency_matrix_excel(file_path: str) -> Tuple[pd.DataFrame, Dict[int, str]]:
    """
    Считывает и выполняет валидацию матрицы смежности из Excel-файла.

    Функция загружает матрицу смежности, проверяет её корректность (квадратность,
    уникальность названий, отсутствие NaN и отрицательных значений, соответствие индексов и столбцов),
    преобразует данные в числовой формат и заменяет строковые индексы на числовые.

    Args:
        file_path (str): Путь к Excel-файлу с матрицей смежности

    Returns:
        Tuple[pd.DataFrame, Dict[int, str]]:
            - adjacency_matrix_df: Валидированная матрица смежности с числовыми индексами
            - indx_stations: Словарь {числовой_id: "название станции"}

    Raises:
        FileNotFoundError: Если файл по указанному пути не существует
        ValueError: В следующих случаях:
            - Матрица не является квадратной
            - Названия отправных пунктов не соответствуют названиям пунктов прибытия
            - Названия населенных пунктов не уникальны
            - Матрица содержит NaN значения
            - Матрица содержит нечисловые значения
            - Матрица содержит отрицательные значения
        Exception: При ошибках чтения Excel-файла
    """
    adjacency_matrix_df: pd.DataFrame = pd.read_excel(file_path, index_col=0)  # type: ignore

    if adjacency_matrix_df.shape[0] != adjacency_matrix_df.shape[1]:
        raise ValueError(f"Матрица должна быть квадратной. Текущая размерность {adjacency_matrix_df.shape[0]}*{adjacency_matrix_df.shape[1]}")
    
    if len(set(adjacency_matrix_df.index) - set(adjacency_matrix_df.columns))!=0:
        raise ValueError(f"Название отправного пункта должно соответствовать названию пункта прибытия")
    
    if len(set(adjacency_matrix_df.index)) != len(adjacency_matrix_df.index):
        raise ValueError(f"Каждый населенный пункт должен иметь уникальное название. Населенные пункты не должны повторяться")
    
    if adjacency_matrix_df.isna().any().any():
        raise ValueError("Матрица не должна содержать NaN. Замените пропущенные значения на 0")

    try:
        adjacency_matrix_df = adjacency_matrix_df.apply(pd.to_numeric)
    except Exception:
        raise ValueError(f"Матрица должна содержать исключительно числовые значения")
    
    negative_mask = adjacency_matrix_df < 0
    if negative_mask.any().any():
        raise ValueError(f"Матрица не должна содержать отрицательные значения")

    adjacency_matrix_df, indx_stations = create_numeric_id_for_matrix(adjacency_matrix_df)

    return adjacency_matrix_df, indx_stations



