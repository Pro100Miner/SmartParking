import cv2
import numpy as np

def correct(coord):
    coord1 = []
    pob = []
    for i in range(len(coord)):
        for j in range (len(coord[i])):
            pob.append(int(coord[i][j]))
        coord1.append(pob)
        pob = []
        coord = coord1
    return coord
def a_variable_of_the_required_format(parking_coordinates):

    parking_coordinates1 = []
    for i in range(len(parking_coordinates)):
        parking_coordinates1.append(parking_coordinates[i].split(" "))
    return parking_coordinates1

# Функция которая проверяет ниже ли точка прямой или нет

def the_point_location_recognizer(k, b, x, y1):
  y = k * x + b
  if y > y1:    #y ордината прямой, y1 ордината точки
    return False
  else:
    return True

def finding_the_quation_of_a_straight_line1(coord):

  x1 = int(coord[0])
  y1 = int(coord[1])
  x2 = int(coord[2])
  y2 = int(coord[3])

  print(x1, "x1", y1, "y1", x2, "x2", y2, "y2")

  k1 = (y2 - y1)/(x2 - x1)
  a1 = -k1 * x1 + y1

  return k1, a1


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

def makes_a_correct_array_of_lines(data):
  data_lines = []
  for i in range(0, len(data)-2, 2):
    data_lines.append(data[i:i+4])
  data_lines.append([data[6], data[7], data[0], data[1]])

  return data_lines

def is_the_parking_spot_inside(l, x, y):

  t = 0
  f = 0
  for i in range(4):
    k, b = finding_the_quation_of_a_straight_line1(l[i])
    p = the_point_location_recognizer(k, b, x, y)
    if p == False:
      f = f + 1
    else:
      t = t + 1
  if t == 2 and f == 2:
    return True
  else:
    return False

# массив true и false
# true - место занято
# false - место свободно

# koor_mass - массив координат парковочных мест
# coord - массив координат машин
def true_false(parking_coordinates1, coord):
    parking_coordinates = a_variable_of_the_required_format(parking_coordinates1)
    #coord = correct(coord)
    print(parking_coordinates)
    print(len(coord), coord, "coord")
    t_f = []
    sch = 0 # счётчик
    print(len(parking_coordinates))
    for i in range(len(parking_coordinates)): # цикл на каждую парковку
        for j in range(len(coord)): # цикл на каждое место
            print(j)
            x, y = finding_the_quation_of_a_straight_line(coord[j]) # находим место пересечения
            l = makes_a_correct_array_of_lines(parking_coordinates[i]) # переделываем координаты порковки
            if is_the_parking_spot_inside(l, x, y) == True: # проверяем находится ли jтая машина на iместе
            # Если да то + к счётчику
                sch = 1
        if sch == 1:
            t_f.append(True)
        else:
            t_f.append(False)
        sch = 0

    return t_f
# cropped - обрезанная фотография
# parking_coordinates - координаты парковок
# t_f - массив True и False
def draw_parking_markings(parking_coordinates1, cropped, t_f):
    print(t_f, "lalalala", len(t_f))
    parking_coordinates = a_variable_of_the_required_format(parking_coordinates1)
    print(len(parking_coordinates), len(parking_coordinates1))
    for i in range(len(t_f)):
        x1,y1,x2,y2,x3,y3,x4,y4 = parking_coordinates[i][0], parking_coordinates[i][1], parking_coordinates[i][2], parking_coordinates[i][3], parking_coordinates[i][4], parking_coordinates[i][5], parking_coordinates[i][6], parking_coordinates[i][7]
        points = np.array([[int(x1), int(y1)], [int(x2), int(y2)],[int(x3), int(y3)], [int(x4), int(y4)]])
        if t_f[i] == True:
            cv2.polylines(cropped, [points], True, (10, 23, 230), 3)
        else:
            cv2.polylines(cropped, [points], True, (10, 230, 21), 3)

    output_image_path1 = 'src/img/result.jpg'
    cv2.imwrite(output_image_path1, cropped)