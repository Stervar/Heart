# Импорт необходимых библиотек
import numpy as np  # Библиотека для работы с многомерными массивами и математическими вычислениями
import time  # Модуль для работы со временем и создания задержек
import sys  # Модуль для взаимодействия с системой и терминалом
import math  # Математические функции (sin, cos и др.)
from collections import deque  # Двусторонняя очередь для эффективного подсчета FPS

def rotate_points(points, angle_x, angle_y, angle_z):
    """
    Функция поворота точек вокруг осей X, Y и Z в трехмерном пространстве
    
    Параметры:
    - points: массив трехмерных точек
    - angle_x, angle_y, angle_z: углы поворота вокруг соответствующих осей
    
    Возвращает повернутые точки
    """
    # Создание матриц поворота для каждой оси
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    
    Ry = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    
    Rz = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1]
    ])
    
    # Комбинирование матриц поворота
    R = np.dot(Rz, np.dot(Ry, Rx))
    return np.dot(points, R.T)

def calculate_fps(fps_counter):
    """
    Расчет частоты кадров (FPS)
    
    Параметр:
    - fps_counter: очередь временных меток кадров
    
    Возвращает количество кадров в секунду
    """
    if len(fps_counter) < 2:
        return 0.0
    
    time_diff = fps_counter[-1] - fps_counter[0]
    
    if time_diff <= 0:
        return 0.0
    
    return len(fps_counter) / time_diff

def get_shaded_char(char, intensity):
    """
    Создание символа с градиентом красного цвета
    
    Параметры:
    - char: символ для окрашивания
    - intensity: интенсивность цвета (0.0 - 1.0)
    
    Возвращает ANSI-последовательность для цветного символа
    """
    red_value = int(255 * intensity)
    return f"\033[38;2;{red_value};0;0m{char}\033[0m"

def create_heart_points(scale=5, num_points=3000, num_layers=70):
    """
    Создание точек для формирования 3D-сердца
    
    Параметры:
    - scale: масштаб сердца
    - num_points: количество точек на контуре
    - num_layers: количество слоев для объемности
    
    Возвращает массив точек сердца
    """
    # Параметрическое уравнение сердца
    t = np.linspace(0, 2*np.pi, num_points)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    z = np.zeros_like(x)

    points = []

    # Создание внешних слоев с переменной плотностью
    for i in range(num_layers):
        factor = 1 - (i/num_layers)**1.5
        layer_x = factor * x
        layer_y = factor * y
        layer_z = np.full_like(x, -i/1.2)
        points.extend(zip(layer_x, layer_y, layer_z))

    # Добавление внутренних точек для создания объема
    for _ in range(num_points * 2):
        r = np.random.random() * 0.95
        theta = np.random.random() * 2 * np.pi
        phi = np.random.random() * np.pi
        x = r * 16 * np.sin(theta)**3 * np.sin(phi)
        y = r * (13 * np.cos(theta) - 5 * np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)) * np.sin(phi)
        z = r * 25 * np.cos(phi)
        points.append((x, y, z))

    # Добавление дополнительных точек для центральной части
    for _ in range(num_points):
        r = np.random.random() * 0.5
        theta = np.random.random() * 2 * np.pi
        x = r * 16 * np.sin(theta)**3
        y = r * (13 * np.cos(theta) - 5 * np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta))
        z = np.random.random() * 20 - 10
        points.append((x, y, z))

    return scale * np.array(points)

def draw_heart(points, width=100, height=50):
    """
    Отрисовка сердца в терминале с использованием символов и z-буфера
    
    Параметры:
    - points: массив точек сердца
    - width: ширина терминала
    - height: высота терминала
    
    Возвращает строку для вывода в терминал
    """
    # Расширенный набор символов для передачи глубины
    shading_chars = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    # Проецирование 3D координат на 2D экран
    x = (points[:, 0] / np.max(np.abs(points[:, 0])) * (width//2) + width//2).astype(int)
    y = (points[:, 1] / np.max(np.abs(points[:, 1])) * (height//2) + height//2).astype(int)
    z = points[:, 2]
    
    # Отсечение точек за пределами экрана
    mask = (0 <= x) & (x < width) & (0 <= y) & (y < height)
    x, y, z = x[mask], y[mask], z[mask]
    
    # Создание экрана и z-буфера
    screen = np.full((height, width), ' ', dtype=object)
    z_buffer = np.full((height, width), float('-inf'))
    
    # Отрисовка точек с учетом глубины
    if len(z) > 0:
        z_min, z_max = np.min(z), np .max(z)
        if z_max > z_min:
            z_normalized = (z - z_min) / (z_max - z_min)
            intensity = (z_normalized * (len(shading_chars) - 1)).astype(int)

            # Отрисовка точек с учетом z-буфера
            for xi, yi, zi, char_index in zip(x, y, z, intensity):
                if zi > z_buffer[yi, xi]:
                    z_buffer[yi, xi] = zi
                    screen[yi, xi] = get_shaded_char(shading_chars[char_index], 0.3 + 0.7 * (zi - z_min) / (z_max - z_min))

    # Преобразование экрана в строку для вывода
    return '\n'.join(''.join(row) for row in screen)

def pulsating_effect(time):
    """
    Создание эффекта пульсации
    
    Параметр:
    - time: текущее время для вычисления пульсации
    
    Возвращает значение масштаба для эффекта пульсации
    """
    return 1 + 0.08 * math.sin(time * 1.5)

def main():
    """
    Основная функция программы, отвечающая за инициализацию и выполнение цикла отрисовки
    """
    heart_points = create_heart_points(scale=10)
    angle_x, angle_y, angle_z = 0, 0, 0

    print('\033[2J')  # Очистка экрана
    print('\033[?25l')  # Скрытие курсора
    
    fps_counter = deque(maxlen=30)
    start_time = time.time()
    
    try:
        while True:
            frame_start = time.time()
            current_time = frame_start - start_time
            
            scale = pulsating_effect(current_time)
            scaled_points = heart_points * scale
            rotated_points = rotate_points(scaled_points, angle_x, angle_y, angle_z)
            rotated_points[:, 1] *= -1  # Инвертирование Y-координат
            
            frame = draw_heart(rotated_points)
            fps_counter.append(time.time())
            fps = calculate_fps(fps_counter)
            
            status_line = f"\033[1mFPS: {fps:.1f} | Press Ctrl+C to exit\033[0m"
            frame_with_status = frame + "\n" + status_line
            
            sys.stdout.write('\033[H' + frame_with_status)  # Перемещение курсора в начало и вывод кадра
            sys.stdout.flush()  # Принудительный вывод буфера
            
            # Обновление углов поворота для анимации
            angle_y += 0.04
            angle_x = 0.2 * math.sin(current_time * 0.5)
            angle_z = 0.1 * math.cos(current_time * 0.3)

            # Ограничение частоты кадров
            frame_time = time.time() - frame_start
            if frame_time < 0.033:
                time.sleep(0.033 - frame_time)
            
    except KeyboardInterrupt:
        print('\033[?25h')  # Показать курсор
        print("\nProgram terminated")

if __name__ == "__main__":
    try:
        import os  # Добавляем импорт os
        
        # Установка размера терминала для оптимального отображения
        sys.stdout.write('\x1b[8;50;100t')
        
        # Настройка буфера терминала для плавной анимации
        if sys.platform == 'win32':
            import msvcrt
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        
        # Очистка экрана перед запуском
        print('\033[2J\033[H')
        
        # Дополнительные настройки терминала для улучшения производительности
        if sys.platform != 'win32':
            import termios
            import tty
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        
        main()
        
    except KeyboardInterrupt:
        print('\033[?25h')  # Показать курсор
        print("\nProgram terminated")
        
    except Exception as e:
        print('\033[?25h')  # Показать курсор в случае ошибки
        print(f"\nAn error occurred: {str(e)}")
        
    finally:
        # Восстановление настроек терминала
        if sys.platform != 'win32':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
        # С брос цветов и настроек терминала
        print('\033[0m')
        
        # Очистка экрана при выходе
        print('\033[2J\033[H')