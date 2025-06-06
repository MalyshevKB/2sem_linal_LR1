## Отчёт по лабораторной работе №1

**"Визуализация топологических поверхностей"**

---
### **1. Описание проекта**

Программа визуализирует ленту Мёбиуса и другие топологические поверхности в 3D-пространстве с возможностью интерактивного управления параметрами.

---
### **2. Основные компоненты**

1. **Класс `TopologicalVisualizer`**

- Инициализирует окно Tkinter, настройки интерфейса и преобразований.

- **Параметры**:

- `DETAIL` — точность разбиения поверхности (по умолчанию 30).

- `COLOR_FACTOR` — коэффициент для цветовой градации.
  

2. **Генерация поверхности**

- **`create_shape`**: Создает точку на поверхности ленты Мёбиуса в 3D-пространстве.

- Формула:

```math
\begin{cases}

x = (a + r \cos(\theta/2)) \cos(\theta) \\
y = (a + r \cos(\theta/2)) \sin(\theta) \\
z = b \cdot r \sin(\theta/2)
\end{cases} 
```
- Где:

- \(a, b\) — параметры с слайдеров (`param1`, `param2`),

- $(\theta)$ — угол, $(r)$ — радиус.

  

3. **Визуализация**

- **`generate_geometry`**: Строит треугольные полигоны для аппроксимации поверхности.

- **`render`**: Отрисовывает поверхность с учетом глубины (сортировка полигонов).

- **Цвет**: Зависит от координаты $(z)$ (глубины) — оттенки синего.

  

4. **Управление**

- **Слайдеры**: Изменяют параметры $(a)$ (радиус) и $(b)$ (скручивание).

- **Клавиши**:

- `W/S` — масштабирование,

- Стрелки — вращение вокруг осей $(X/Y)$.

---
#### **3. Пример использования**



app = TopologicalVisualizer() # Создание экземпляра

app.run() # Запуск визуализации

**Результат**:

- Окно с лентой Мёбиуса и координатными осями.

- Интерактивное изменение формы поверхности через слайдеры и клавиатуру.

  

---

  

#### **4. Математическая основа**


**Матрица камеры по-умолчанию**
```math
 C = \begin{pmatrix}
50 && 0 && 0 && 0 \\
0 && 50 && 0 && 0 \\
0 && 0 && 50 && 0 \\
0 && 0 && 0 && 50
\end{pmatrix} 
```

**Поворот вокруг оси OX**
```math
R_{x}(\phi) = \begin{pmatrix}
1 && 0 && 0 && 0 \\
0 && cos \phi && -\sin \phi && 0 \\
0 && \sin \phi && \cos \phi && 0 \\
0 && 0 && 0 && 1
\end{pmatrix} 
```
```math
C' = R_{x}(\phi) \cdot C
```

**Поворот вокруг оси OY**
```math
R_{x}(\phi) = \begin{pmatrix}
\cos \phi && 0 && \sin \phi && 0 \\
0 && 1 && 0 && 0 \\
-\sin \phi && 0 && \cos \phi && 0 \\
0 && 0 && 0 && 1
\end{pmatrix} 
```
```math
C' = R_{y}(\phi) \cdot C
```

 **Отрисовка (`render`)**
1. **Сортировка полигонов** по глубине (по среднему значению $(z)$) для корректного отображения.
2. **Проецирование 3D → 2D**:
   - Каждая точка преобразуется в экранные координаты:
     
     $$[
     x_{\text{экран}} = x_{\text{3D}} + \frac{\text{ширина}}{2}, \quad y_{\text{экран}} = y_{\text{3D}} + \frac{\text{высота}}{2}
     ]$$
3. **Заливка полигонов** с цветом, зависящим от глубины:
   
   
   $$[
   \text{color} = \min(255, 10 \cdot |z|)
   ]$$


**Приближение/отдаление камеры**
```math
C' = 1.1C
```
```math
C' = \frac{1}{1.1}C
```



  


  