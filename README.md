<h2 align="center">◢⸻⸻⸻⸻⸻⸻⸻⸻❃⸻⸻⸻⸻⸻⸻⸻⸻◣</h2>
<h1 align="center">❤️ Анимированное 3D Сердце в Терминале ❤️ Animated 3D Heart in Terminal</h1>
<h2 align="center">◢⸻⸻⸻⸻⸻⸻⸻⸻❃⸻⸻⸻⸻⸻⸻⸻⸻◣</h2>

## 🚀 Описание / Description 🚀

Этот проект создает анимированное 3D сердце, которое пульсирует и вращается в терминале. Используются параметрические уравнения и 3D трансформации для создания эффектного визуального представления.

<h2 align="center">◢⸻⸻⸻⸻⸻⸻⸻⸻❃⸻⸻⸻⸻⸻⸻⸻⸻◣</h2>

## 🔥 Особенности / Features 🔥

<h2 align="center">◢⸻⸻⸻⸻⸻⸻⸻⸻❃⸻⸻⸻⸻⸻⸻⸻⸻◣</h2>
Есть только три основыных версии которые не являються ни копиямии ни продолжениями 
так как в каждой версии я пытлся восоздать имено что то новое их за это каждая вресия по своему интересна 

ну вот список самых интерсных и выжных
- Heart-12.py
- Heart-13.py
- Heart-17.py

<h2 align="center">◢⸻⸻⸻⸻⸻⸻⸻⸻❃⸻⸻⸻⸻⸻⸻⸻⸻◣</h2>
## 📊 Установка / Installation 📊

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/ваш_логин/Heart-12.git
    cd Heart-12
    ```

2. Установите необходимые зависимости:
    ```bash
    pip install numpy
    ```

3. Запустите проект:
    ```bash
    python Heart-12.py
    ```

## 📈 Примеры работы / Examples 📈

![Пример работы](ссылка_на_изображение)

## 🌟 Поддержка проекта / Project Support 🌟

Если вам понравился проект, поставьте ⭐ звезду на GitHub!

## 🔧 Технические характеристики / Technical Specifications 🔧

- **Язык программирования**: Python
- **Библиотеки**: NumPy, colorsys, sys, collections, time, math
- **Операционная система**: Кроссплатформенный (Linux, Windows, MacOS)


---

## 📜 Код проекта / Project Code 📜

```python
1. **Импорт библиотек**:
   - В начале кода импортируются необходимые библиотеки:
     - `numpy`: для работы с массивами и математическими операциями.
     - `time`: для работы со временем и задержками.
     - `sys`: для взаимодействия с системой, в частности, для вывода в терминал.
     - `math`: для математических функций, таких как синус и косинус.
     - `collections.deque`: для создания двусторонней очереди, используемой для подсчета FPS.
     - `colorsys`: для преобразования цветов из HSV в RGB.

2. **Функция `rotate_points`**:
   - Эта функция принимает массив точек и угол поворота. Она создает матрицу поворота вокруг оси Y и применяет ее к точкам, возвращая новые координаты.
   - Пример кода:
     ```python
     def rotate_points(points, angle_y):
         Ry = np.array([
             [np.cos(angle_y), 0, np.sin(angle_y)],
             [0, 1, 0],
             [-np.sin(angle_y), 0, np.cos(angle_y)]
         ])
         return np.dot(points, Ry.T)
     ```

3. **Функция `calculate_fps`**:
   - Эта функция подсчитывает количество кадров в секунду (FPS) на основе временных меток, хранящихся в очереди. Она возвращает значение FPS, что позволяет контролировать производительность анимации.
   - Пример кода:
     ```python
     def calculate_fps(fps_counter):
         if len(fps_counter) < 2:
             return 0.0
         time_diff = fps_counter[-1] - fps_counter[0]
         if time_diff <= 0:
             return 0.0
         return len(fps_counter) / time_diff
     ```

4. **Функция `get_colored_char`**:
   - Эта функция преобразует символ в цветной символ, используя HSV цветовую модель. Она принимает символ и его цветовые параметры, а затем возвращает ANSI последовательность для окраски символа.
   - Пример кода:
     ```python
     def get_colored_char(char, hue, saturation=1.0, value=1.0):
         hue = max(0.0, min(1.0, hue))
         r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, saturation, value)]
         return f"\033[38;2;{r};{g};{b}m{char}\033[0m"
     ```

5. **Функция `create_heart_points`**:
   - Эта функция генерирует координаты точек, формирующих сердце, используя параметрические уравнения. Она создает несколько слоев для добавления объема и случайные внутренние точки для улучшения визуального эффекта.
   - Пример кода:
     ```python
     def create_heart_points(scale=5, num_points=1000, num_layers=30):
         t = np.linspace(0, 2 * np.pi, num_points)
         x = 16 * np.sin(t) ** 3
         y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
         z = np.zeros_like(x)

         points = []
         for i in range(num_layers):
             factor = 1 - i / num_layers
             layer_x = factor * x
             layer_y = factor * y
             layer_z = np.full_like(x, -i / 2)
             points.extend(zip(layer_x, layer_y, layer_z))

         for _ in range(num_points // 2):
             r = np.random.random() * 0.8
             theta = np.random.random() * 2 * np.pi
             phi = np.random.random() * np.pi
             x = r * 16 * np.sin(theta) ** 3 * np.sin(phi)
             y = r * (13 * np.cos(theta) - 5 * np.cos(2 * theta) - 
                      2 * np.cos(3 * theta) - np.cos(4 * theta)) * np.sin(phi)
             z = r * 15 * np.cos(phi)
             points.append((x, y, z))

         return scale * np.array(points)
     ```

6. **Функция `draw_heart`**:
   - Эта функция отвечает за отрисовку сердца на экране. Она проецирует 3D координаты на 2D экран, учитывает глубину и использует символы для отображения.
   - Пример кода:
     ```python
     def draw_heart(points, width=80, height=40, time_val=0):
         shading_chars = " .:!*OQ#"
         x = (points[:, 0] / np.max(np.abs(points[:, 0])) * (width // 2) + width // 2).astype(int)
         y = (-points[:, 1] / np.max(np.abs(points[:, 1])) * (height // 2) + height // 2).astype(int)
         z = points[:, 2]

         mask = (0 <= x) & (x < width) & (0 <= y) & (y < height)
         x, y, z = x[mask], y[mask], z[mask]

         screen = np.full((height, width), ' ', dtype=object)
         z_buffer = np.full((height, width), float('-inf'))

         if len(z) > 0:
             z_min, z_max = np.min(z), np.max(z)
             if z_max > z_min:
                 z_normalized = (z - z_min) / (z_max - z_min)
                 intensity = (z_normalized * (len(shading_chars) - 1)).astype(int)

                 for xi, yi, zi, char_index in zip(x, y, z, intensity):
                     if zi > z_buffer[yi, xi]:
                         z_buffer[yi, xi] = zi
                         z_factor = (zi - z_min) / (z_max - z_min)
                         hue = (time_val + z_factor) % 1.0
                         screen[yi, xi] = get_colored_char(shading_chars[char_index], hue)

         return '\n'.join(''.join(row) for row in screen)
     ```

7. **Функция `pulsating_effect`**:
   - Эта функция создает синусоидальное изменение размера для эффекта пульсации сердца.
   - Пример кода:
     ```python
     def pulsating_effect(time):
         return 1 + 0.05 * math.sin(time * 2)
     ```

8. **Основная функция `main`**:
   - В этой функции происходит инициализация, создание точек сердца, а также основной цикл анимации, который обновляет и отображает сердце в терминале.
   - Пример кода:
     ```python
     def main():
         heart_points = create_heart_points(scale=8)
         angle_y = 0
         print('\033[2J')
         print('\033[?25l')
         fps_counter = deque(maxlen=60)
         start_time = time.time()

         try:
             while True:
                 frame_start = time.time()
                 current_time = frame_start - start_time
                 scale = pulsating_effect(current_time)
                 scaled_points = heart_points * scale
                 rotated_points = rotate_points(scaled_points, angle_y)
                 frame = draw_heart(rotated_points, time_val=(current_time * 0.1) % 1.0)

                 fps_counter.append(time.time())
                 fps = calculate_fps(fps_counter)

                 status_line = f"\033[1mFPS: {fps:.1f} | Press Ctrl+C to exit\033[0m"
                 frame_with_status = frame + "\n" + status_line

                 terminal_width = 80
                 frame_width = len(frame.split('\n')[0])
                 padding = ' ' * ((terminal_width - frame_width ) // 2)
                 frame_with_status = padding + frame_with_status + padding

                 sys.stdout.write('\033[H' + frame_with_status)
                 sys.stdout.flush()

                 angle_y += 0.05

                 frame_time = time.time() - frame_start
                 if frame_time < 0.033:
                     time.sleep(0.033 - frame_time)

         except KeyboardInterrupt:
             print('\033[?25h')
             print("\nProgram terminated")
     ```

 ### Заключение

Этот проект демонстрирует, как можно использовать Python и математические концепции для создания визуально привлекательной анимации в терминале. Анимированное 3D сердце не только привлекает внимание, но и служит отличным примером применения параметрических уравнений и 3D трансформаций в программировании.