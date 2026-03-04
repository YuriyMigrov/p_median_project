import json

def read_p_median_count(file_path: str) -> int:
    """
    Считывание и валидация количества p-медиан

    Args:
        file_path (str): путь к файлу

    Returns:
        value (int): количество p-медиан
    
    Raises:
        FileNotFoundError: Если файл по указанному пути не существует
        json.JSONDecodeError: Если файл содержит некорректный JSON
        ValueError: В следующих случаях:
            - Отсутствует поле "p_median_count" в JSON-данных
            - Значение поля "p_median_count" не является целым числом
            - Значение поля "p_median_count" меньше или равно 0
        UnicodeDecodeError: Если файл имеет кодировку, отличную от UTF-8
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "p_median_count" not in data:
        raise ValueError("Поле 'p_median_count' отсутствует")

    value = data["p_median_count"]

    if not isinstance(value, int):
        raise ValueError("'p_median_count' должен быть целым числом")

    if value <= 0:
        raise ValueError("'p_median_count' должен быть строго больше 0")

    return value