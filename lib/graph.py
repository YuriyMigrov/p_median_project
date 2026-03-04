import igraph as ig # type: ignore
import pandas as pd

def create_graph(adjacency_matrix_df: pd.DataFrame) -> ig.Graph.Weighted_Adjacency: # type: ignore
    """
    Создает взвешенный неориентированный граф на основе матрицы смежности.

    Функция преобразует DataFrame с матрицей смежности в объект графа библиотеки igraph.
    Веса ребер берутся из значений матрицы смежности, вершинам присваиваются названия
    станций из индексов DataFrame.

    Args:
        adjacency_matrix_df (pd.DataFrame): Матрица смежности с числовыми значениями весов.
                                           Индексы DataFrame используются как названия вершин.

    Returns:
        ig.Graph.Weighted_Adjacency: Взвешенный неориентированный граф, где:
            - Вершины имеют атрибут 'name' с названиями станций
            - Ребра имеют атрибут 'weight' с значениями из матрицы смежности
    """

    adj_matrix = adjacency_matrix_df.values

    graph = ig.Graph.Weighted_Adjacency( # type: ignore
        adj_matrix.tolist(),
        mode=ig.ADJ_UNDIRECTED, # type: ignore
        attr="weight"
    )

    graph.vs["name"] = adjacency_matrix_df.index.tolist() # type: ignore

    return graph # type: ignore