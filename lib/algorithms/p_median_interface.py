import igraph as ig # type: ignore
import pandas as pd
from typing import List, Protocol, Tuple


class PMedianAlgorithm(Protocol):
    """
    Протокол, определяющий интерфейс для алгоритмов решения задачи о p-медиане.

    Классы, реализующие этот протокол, должны предоставлять метод search для поиска
    оптимального размещения p-медианных вершин на графе с учетом вектора потребностей.

    Methods:
        search: Выполняет поиск p-медиан на графе
    """
    def search(self, graph: ig.Graph, p: int, needs_vector_df: pd.DataFrame, adjacency_matrix_df: pd.DataFrame) -> Tuple[List[int], float]:
        """
        Выполняет поиск p-медианных вершин.

        Args:
            graph (ig.Graph): Взвешенный граф, на котором производится поиск
            p (int): Количество медиан для размещения (должно быть > 0)
            needs_vector_df (pd.DataFrame): DataFrame с вектором потребностей для каждой вершины
            adjacency_matrix_df (pd.DataFrame): Матрица смежности графа

        Returns:
            Tuple[List[int], float]:
                - List[int]: Список индексов вершин, выбранных в качестве медиан
                - float: Суммарное расстояние
        """
        ...