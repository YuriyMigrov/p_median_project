import igraph as ig # type: ignore
import pandas as pd
from typing import List, Optional, Tuple
from errors.errors import NullRouteError

def get_shortes_route_ids(graph: ig.Graph, from_node_id: int, to_node_id: int) -> List[List[int]]:
    """
    Получает кратчайший маршрут между двумя вершинами графа в виде списка идентификаторов вершин.

    Args:
        graph (ig.Graph): Граф, в котором ищется маршрут
        from_node_id (int): Идентификатор начальной вершины
        to_node_id (int): Идентификатор конечной вершины

    Returns:
        List[List[int]]: Список, содержащий один список с идентификаторами вершин кратчайшего маршрута.

    Raises:
        NullRouteError: Если маршрут между вершинами не существует (пустой маршрут)
    """
    shortes_route_ids: List[List[int]] = graph.get_shortest_paths(from_node_id, to=to_node_id) # type: ignore
    if len(shortes_route_ids[0])==0: # type: ignore
        raise NullRouteError("Маршрут не построился")
    else:
        return shortes_route_ids # type: ignore



def get_shortes_distance(graph: ig.Graph, from_node_id: int, to_node_id: int, adjacency_matrix_df: pd.DataFrame) -> Optional[float]:
    """
    Вычисляет длину кратчайшего пути между двумя вершинами на основе матрицы смежности.

    Args:
        graph (ig.Graph): Граф, содержащий вершины
        from_node_id (int): Идентификатор начальной вершины
        to_node_id (int): Идентификатор конечной вершины
        adjacency_matrix_df (pd.DataFrame): Матрица смежности с весами ребер

    Returns:
        Optional[float]: Длина кратчайшего пути или None, если маршрут не существует
    """
    try:
        shortes_route_ids: List[List[int]] = get_shortes_route_ids(graph, from_node_id, to_node_id)
        distance = 0
        for i in range(len(shortes_route_ids[0])-1):
            distance += float(adjacency_matrix_df.iloc[shortes_route_ids[0][i], shortes_route_ids[0][i+1]]) # type: ignore
        return distance
    except NullRouteError:
        return None



def get_set_min_distance(graph: ig.Graph, set_from_node_ids: List[int], to_node_id: int, adjacency_matrix_df: pd.DataFrame) -> Optional[float]:
    """
    Находит минимальное расстояние от заданной вершины до ближайшей вершины из множества.

    Args:
        graph (ig.Graph): Граф, содержащий вершины
        set_from_node_ids (List[int]): Список идентификаторов вершин-источников
        to_node_id (int): Идентификатор целевой вершины
        adjacency_matrix_df (pd.DataFrame): Матрица смежности с весами ребер

    Returns:
        Optional[float]: Минимальное расстояние от целевой вершины до ближайшей вершины из множества,
                        или None, если ни один маршрут не существует
    """
    distances: List[float] = []
    for from_node_id in set_from_node_ids:
        distance: Optional[float] = get_shortes_distance(graph, from_node_id, to_node_id, adjacency_matrix_df)
        if distance is not None:
            distances.append(distance)

    if distances:
        min_distance: float = min(distances)
        return min_distance
    else:
        return None




def get_target_func_value(graph: ig.Graph, subsampling_nodes: List[int], needs_vector_df: pd.DataFrame, adjacency_matrix_df: pd.DataFrame) -> Tuple[float, float]:
    """
    Вычисляет значение целевой функции для задачи о p-медиане.

    Функция рассчитывает взвешенную сумму расстояний от всех вершин графа до ближайших
    медианных вершин с учетом вектора потребностей, а также сумму всех расстояний.

    Args:
        graph (ig.Graph): Граф, содержащий все вершины
        subsampling_nodes (List[int]): Список идентификаторов вершин, выбранных в качестве медиан
        needs_vector_df (pd.DataFrame): DataFrame с вектором потребностей для каждой вершины
        adjacency_matrix_df (pd.DataFrame): Матрица смежности с весами ребер

    Returns:
        Tuple[float, float]:
            - weighted_sum: Взвешенная сумма расстояний (потребность * расстояние до ближайшей медианы)
            - distance_sum: Сумма всех расстояний от каждой вершины до ближайшей медианы
    """
    all_nodes: List[int] = graph.vs["name"] # type: ignore
    weighted_sum: float = 0.0
    distance_sum: float = 0.0
    for node in all_nodes: # type: ignore
        distance: Optional[float] = get_set_min_distance(graph, subsampling_nodes, node, adjacency_matrix_df) # type: ignore
        if distance is not None:
            weighted_sum += needs_vector_df.iloc[node].values[0]*distance # type: ignore
            distance_sum += distance
    
    else:
        return weighted_sum, distance_sum