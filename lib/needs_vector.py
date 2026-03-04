import pandas as pd
from typing import Dict, Tuple

def create_numeric_id_for_vector(needs_vector_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[int, str]]:
    """
    Преобразование названий станций в числовые индексы

    Args:
        needs_vector_df (DataFrame): вектор потребностей с индексом в виде названий станций

    Returns:
        (needs_vector_df, indx_station) (Tuple[pd.DataFrame, Dict[int, str]]): вектор потребностей с числовым индексом и словарь {id: "Название станции"}.
    """

    stations_indx: Dict[str, int] = dict(zip(needs_vector_df.index, range(len(needs_vector_df.index))))
    indx_station: Dict[int, str] = dict(zip(range(len(needs_vector_df.index)), needs_vector_df.index))
    
    needs_vector_df.index = needs_vector_df.index.map(stations_indx)

    return needs_vector_df, indx_station

def read_needs_vector_excel(file_path: str) -> Tuple[pd.DataFrame, Dict[int, str]]:
    """
    Считывание и валидация вектора потребностей

    Args:
        file_path (str): путь к файлу

    Returns:
        (needs_vector_df, indx_station) (Tuple[pd.DataFrame, Dict[int, str]]): вектор потребностей и словарь {id: "Название станции"}
    
    Raises:
        FileNotFoundError: Если файл по указанному пути не существует
        ValueError: В следующих случаях:
            - Файл содержит NaN значения (нужно заменить на 0)
            - Индексы (названия станций) не уникальны
            - Вектор содержит нечисловые значения
            - Вектор содержит отрицательные значения
        Exception: При ошибках чтения Excel-файла (некорректный формат, поврежденный файл и т.д.)
    """
    needs_vector_df: pd.DataFrame = pd.read_excel(file_path, index_col=0) # type: ignore

    if needs_vector_df.isna().any().any():
        raise ValueError("Вектор не должнен содержать NaN. Замените пропущенные значения на 0")
    
    if len(set(needs_vector_df.index)) != len(needs_vector_df.index):
        raise ValueError(f"Каждый населенный пункт должен иметь уникальное название. Населенные пункты не должны повторяться")

    try:
        needs_vector_df = needs_vector_df.apply(pd.to_numeric)
    except Exception:
        raise ValueError(f"Вектор должен содержать исключительно числовые значения")
    
    negative_mask = needs_vector_df < 0
    if negative_mask.any().any():
        raise ValueError(f"Вектор не должен содержать отрицательные значения")
    
    needs_vector_df, indx_station = create_numeric_id_for_vector(needs_vector_df)


    return needs_vector_df, indx_station