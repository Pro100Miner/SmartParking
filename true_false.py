import cv2
import numpy as np

# Функция для нужного формата
def a_variable_of_the_required_format(parking_coordinates):

    parking_coordinates1 = []
    for i in range(len(parking_coordinates)):
        parking_coordinates1.append(parking_coordinates[i].split(" "))
    return parking_coordinates1

# Функция находящая пересечение диагоналей
def finding_the_quation_of_a_straight_line(coord):

  x1 = int(coord[0])
  y1 = int(coord[1])
  x2 = int(coord[2])
  y2 = int(coord[3])


  k1 = (y2 - y1)/(x2 - x1)
  k2 = (y1 - y2)/(x2 - x1)

  a1 = -k1 * x1 + y1
  a2 = -k2 * x1 + y2

  x = (a2 - a1) / (k1 - k2)
  y = k1 * x + a1

  return x, y

# Функция для нужного формата
def makes_a_correct_array_of_lines(data):
  data_lines = []
  for i in range(0, len(data)-2, 2):
    data_lines.append(data[i:i+4])
  data_lines.append([data[6], data[7], data[0], data[1]])

  return data_lines

# Функция проверяет находится ли точка внутри парковочного места
def is_the_parking_spot_inside(vertices1, x, y):
    vertices = []
    vertices.append(vertices1[0:2])
    vertices.append(vertices1[2:4])
    vertices.append(vertices1[4:6])
    vertices.append(vertices1[6:8])

    inside = False  # Флаг, указывающий, внутри ли точка
    for i in range(4):  # Проходим по всем сторонам

        x1, y1 = vertices[i]  # Первая вершина стороны
        x2, y2 = vertices[(i + 1) % 4] # Вторая вершина стороны (замыкаем многоугольник)

            # Проверяем, пересекает ли луч сторону:
            # 1. Точка должна быть между y1 и y2 по вертикали
            # 2. Точка должна быть слева от пересечения луча со стороной
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside  # Меняем флаг при каждом пересечении

    return inside


# Функция для получения массива True/False
# True - место занято
# False - место свободно

# parking_coordinates1 - массив координат парковочных мест
# coord - массив координат машин
def true_false(parking_coordinates1, coord):
    parking_coordinates = a_variable_of_the_required_format(parking_coordinates1)
    t_f = []
    sch = 0 # счётчик
    for i in range(len(parking_coordinates)): # цикл на каждую парковку
        for j in range(len(coord)): # цикл на каждое место

            x, y = finding_the_quation_of_a_straight_line(coord[j]) # находим место пересечения
            #l = makes_a_correct_array_of_lines(parking_coordinates[i]) # переделываем координаты порковки

            if is_the_parking_spot_inside(parking_coordinates[i], x, y) == True: # проверяем находится ли jтая машина на iместе
            # Если да то + к счётчику
                sch = 1
        if sch == 1:
            t_f.append(True)
        else:
            t_f.append(False)
        sch = 0

    return t_f

# Функция для разметки парковочных мест
# cropped - обрезанная фотография
# parking_coordinates - координаты парковок
# t_f - массив True и False
def draw_parking_markings(parking_coordinates1, cropped, t_f):
    parking_coordinates = a_variable_of_the_required_format(parking_coordinates1)
    print(len(parking_coordinates), len(parking_coordinates1))
    for i in range(len(t_f)):
        x1,y1,x2,y2,x3,y3,x4,y4 = parking_coordinates[i][0], parking_coordinates[i][1], parking_coordinates[i][2], parking_coordinates[i][3], parking_coordinates[i][4], parking_coordinates[i][5], parking_coordinates[i][6], parking_coordinates[i][7]
        points = np.array([[int(x1), int(y1)], [int(x2), int(y2)],[int(x3), int(y3)], [int(x4), int(y4)]])
        if t_f[i] == False:
            cv2.polylines(cropped, [points], True, (10, 230, 21), 3)
    for i in range(len(t_f)):
        x1,y1,x2,y2,x3,y3,x4,y4 = parking_coordinates[i][0], parking_coordinates[i][1], parking_coordinates[i][2], parking_coordinates[i][3], parking_coordinates[i][4], parking_coordinates[i][5], parking_coordinates[i][6], parking_coordinates[i][7]
        points = np.array([[int(x1), int(y1)], [int(x2), int(y2)],[int(x3), int(y3)], [int(x4), int(y4)]])
        if t_f[i] == True:
            cv2.polylines(cropped, [points], True, (10, 23, 230), 3)

    output_image_path1 = 'src/img/result.jpg'
    cv2.imwrite(output_image_path1, cropped)