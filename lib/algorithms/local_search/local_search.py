from ..p_median_interface import PMedianAlgorithm
import igraph as ig # type: ignore
import pandas as pd
from typing import List, Dict, Any, Tuple
from random import sample, choice
from .target_function import get_target_func_value
from ...setup_logging import logger


class PMedianLocalSearch(PMedianAlgorithm):
    """
    Реализация алгоритма локального поиска для решения задачи о p-медиане.

    Алгоритм начинает со случайного выбора p вершин в качестве медиан, затем итеративно
    пытается улучшить решение, заменяя одну из текущих медиан на случайную вершину
    из множества неиспользуемых. Замена производится, если она приводит к улучшению
    целевой функции (уменьшению взвешенной суммы расстояний).

    Attributes:
        Наследует атрибуты от PMedianAlgorithm
    """
    def search(self, graph: ig.Graph, p: int, needs_vector_df: pd.DataFrame, adjacency_matrix_df: pd.DataFrame) -> Tuple[List[int], float]:
        """
        Выполняет локальный поиск оптимального размещения p медиан.

        Args:
            graph (ig.Graph): Взвешенный граф, на котором производится поиск
            p (int): Количество медиан для размещения (должно быть > 0 и <= числа вершин)
            needs_vector_df (pd.DataFrame): DataFrame с вектором потребностей для каждой вершины
            adjacency_matrix_df (pd.DataFrame): Матрица смежности с весами ребер

        Returns:
            Tuple[List[int], float]:
                - List[int]: Список индексов вершин, выбранных в качестве медиан
                - float: Суммарное расстояние (пробег) полученного решения
        """
        all_nodes: List[int] = graph.vs["name"] # type: ignore
        logger.info("Стартовые значения")
        logger.info(f"Все узлы: {all_nodes}") # type: ignore

        subsampling_nodes: List[int] = sample(all_nodes, k=p) # type: ignore
        current_target_func_value, current_distance_sum = get_target_func_value(graph, subsampling_nodes, needs_vector_df, adjacency_matrix_df)
        logger.info(f"Подвыборка узлов: {subsampling_nodes}, значение целевой функции: {current_target_func_value}, пробег, км: {current_distance_sum}")

        use_nodes: List[int] = subsampling_nodes.copy()
        logger.info(f"Использованные узлы: {use_nodes}")

        not_use_nodes = list(set(all_nodes) - set(use_nodes)) # type: ignore
        logger.info(f"Неиспользованные узлы: {not_use_nodes}\n\n")
        
        i = 0
        while len(not_use_nodes)!=0: # type: ignore
            i+=1
            logger.info(f"Итерация: {i}")
        
            random_node = choice(not_use_nodes) # type: ignore
            logger.info(f"Случайный узел: {random_node}")

            delta_list: List[Dict[str, Any]] = []
            for j in range(len(subsampling_nodes)):
                logger.info(f"Вложенная итерация: {j}")
                new_subsampling_nodes = subsampling_nodes.copy()
                new_subsampling_nodes[j] = random_node
                new_target_func_value, new_distance_sum = get_target_func_value(graph, new_subsampling_nodes, needs_vector_df, adjacency_matrix_df)
                delta_target_func_values = current_target_func_value - new_target_func_value # type: ignore
                delta_distance_sum = current_distance_sum - new_distance_sum # type: ignore
                logger.info(f"Новая подвыборка узлов: {new_subsampling_nodes}, новое значение целевой функции: {new_target_func_value}, новый пробег, км: {new_distance_sum}")
                logger.info(f"Разность значений целевых функциий: {delta_target_func_values}, разность значений пробега, км: {delta_distance_sum}")
                delta_list.append({"subsampling_nodes":new_subsampling_nodes, 
                                   "delta_target_func_values":delta_target_func_values,
                                   "delta_distance_sum":delta_distance_sum, 
                                   "new_distance_sum": new_distance_sum, 
                                   "new_target_func_value": new_target_func_value})
            
            max_delta = max(delta_list, key=lambda x: x["delta_target_func_values"])

            if max_delta["delta_target_func_values"]>0:
                subsampling_nodes = max_delta["subsampling_nodes"]
                current_distance_sum = max_delta["new_distance_sum"]
                current_target_func_value = max_delta["new_target_func_value"]
                use_nodes.append(random_node)
            else:
                use_nodes.append(random_node)
            
            not_use_nodes = list(set(all_nodes) - set(use_nodes)) # type: ignore
            logger.info(f"Неиспользованные узлы: {not_use_nodes}")
            logger.info(f"***** Итог на итерации {i}: новая подвыборка узлов: {subsampling_nodes}, новое значение целевой функции: {current_target_func_value}, новый пробег, км: {current_distance_sum}\n\n")
        return subsampling_nodes, current_distance_sum