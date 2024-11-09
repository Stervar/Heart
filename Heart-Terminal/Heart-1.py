# Импорт необходимых библиотек для создания анимированного сердца
import numpy as np      # Математические операции и работа с массивами
import time             # Работа со временем и задержками
import os               # Работа с операционной системой

def clear_screen():
    """
    Очистка экрана с учетом операционной системы
    
    Использует системную команду cls для Windows и clear для Unix-подобных систем
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def create_heart_points(scale=10):
    """
    Генерация точек для создания 2D формы сердца
    
    Использует параметрическое уравнение сердца
    
    Args:
        scale (int): Масштаб сердца
    
    Returns:
        np.array: Массив точек сердца
    """
    # Создание параметрического массива
    t = np.linspace(0, 2*np.pi, 100)
    
    # Математические формулы для создания формы сердца
    x = scale * 16 * np.sin(t)**3
    y = scale * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
    z = np.zeros_like(x)  # Плоскость Z = 0 для 2D вращения
    
    # Преобразование координат в столбцы
    return np.column_stack((x, y, z))

def rotate_points(points, angle):
    """
    Вращение точек вокруг оси Z
    
    Args:
        points (np.array): Массив точек
        angle (float): Угол поворота
    
    Returns:
        np.array: Повернутые точки
    """
    # Матрица поворота вокруг оси Z
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    
    # Применение матрицы поворота
    return np.dot(points, rotation_matrix)

def draw_heart(points, width=60, height=30):
    """
    Отрисовка сердца с использованием эмодзи
    
    Args:
        points (np.array): Точки сердца
        width (int): Ширина экрана
        height (int): Высота экрана
    """
    # Инициализация экрана пустыми символами
    screen = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Извлечение координат X и Y
    x = points[:, 0]
    y = points[:, 1]
    
    # Масштабирование и центрирование точек
    x = (x / np.max(np.abs(x)) * (width//3)) + width//2
    y = (y / np.max(np.abs(y)) * (height//3)) + height//2
    
    # Список эмодзи сердец для разнообразия
    heart_emojis = ['❤', '💗', '💕', '💖', '💘', '💝', '💞', '💓']
    
    # Отрисовка точек
    for xi, yi in zip(x, y):
        if 0 <= int(xi) < width and 0 <= int(yi) < height:
            # Случайный выбор эмодзи сердца
            screen[int(yi)][int(xi)] = np.random.choice(heart_emojis)
    
    # Вывод экрана
    for row in screen:
        print(''.join(row))

def main():
    """
    Основная функция для запуска анимации сердца
    """
    # Генерация точек сердца
    heart_points = create_heart_points()
    
    # Начальный угол поворота
    angle = 0
    
    try:
        while True:
            # Очистка экрана
            clear_screen()
            
            # Поворот точек
            rotated_points = rotate_points(heart_points, angle)
            
            # Отрисовка сердца
            draw_heart(rotated_points)
            
            # Обновление угла поворота
            angle += 0.1
            
            # Небольшая задержка для управления скоростью анимации
            time.sleep(0.05)
    
    except KeyboardInterrupt:
        # Обработка завершения программы
        print("\nПрограмма завершена")

# Точка входа в программу
if __name__ == "__main__":
    try:
        main()  # Запуск основной функции
    except KeyboardInterrupt:
        print("\nПрограмма завершена")