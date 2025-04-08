import cv2
import numpy as np
import torch


model = YOLO('src/yolov5m.pt')
# Список классов для транспорта (машины, грузовики, мотоциклы)
transport_classes = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
number_kam = 1

# Функция для обработки изображения
def process_image(image):
    if image is None:
        print("Ошибка: Не удалось загрузить изображение.")
        return
    # Получение результатов от модели YOLOv8
    results = model(image)[0]
    # Получение оригинального изображения и результатов
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
    classes = results.boxes.cls.cpu().numpy()

    # Список для хранения координат транспорта
    transport_boxes = []

    # Обработка результатов
    for class_id, box in zip(classes, boxes):
        if int(class_id) in transport_classes:  # Фильтрация по классам транспорта
            x1, y1, x2, y2 = box
            transport_boxes.append((x1, y1, x2, y2))

            # Рисование рамок на изображении
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, transport_classes[int(class_id)], (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # Сохранение измененного изображения
    output_image_path = 'p3.jpg'
    cv2.imwrite(output_image_path, image)
    # Возвращение координат транспорта
    return transport_boxes


def obrabotka(number_kam):
  o1= open('FILES/Камеры.txt', 'r')
  text1 = o1.read()
  o2 = open('FILES/Координаты.txt', 'r')
  text2 = o2.read()
  o3 = open('FILES/НеобхФрагмент.txt', 'r')
  text3 = o3.read()

  cameras = text1.split('\n') # Файл с данными о камерах
  coordinates_park = text2.split('!')[1:-1] # Файл с координатами парковок
  fragments = text3.split('\n') #  Файл с данными об обрезках камер

  # Загрузка изображения
  cap = cv2.VideoCapture(cameras[number_kam-1])
  ret, frame = cap.read()

  fragment = fragments[number_kam-1].split(' ')

  koor_mass = coordinates_park[number_kam-1].split('\n')
  koor_mass.pop(0)
  koor_mass.pop(-1)
  # Выделение необходимого фрагмента: image[y1:y2, x1:x2]
  cropped = frame[int(fragment[0]):int(fragment[1]), int(fragment[2]):int(fragment[3])]

  for i in range(len(koor_mass)):
    x1,y1,x2,y2,x3,y3,x4,y4 = koor_mass[i].split(' ')
    points = np.array([[int(x1), int(y1)], [int(x2), int(y2)],[int(x3), int(y3)], [int(x4), int(y4)]])
    cv2.polylines(cropped, [points], True, (10, 20, 241), 3)

  output_image_path1 = 'parkov_1.jpg'
  cv2.imwrite(output_image_path1, cropped)


obrabotka(number_kam)