import cv2
import numpy as np
import torch

a = 2
model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
# Список классов для транспорта (машины, грузовики, мотоциклы)
transport_classes = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}

# Функция для обработки изображения
def detected_image(image):
    if image is None:
        print("Ошибка: Не удалось загрузить изображение.")
        return []

    results = model(image)
    boxes = results.xyxy[0].cpu().numpy()  # Тензор с результатами

    transport_boxes = []
    for det in boxes:
        x1, y1, x2, y2, conf, cls_id = det[:6]
        if int(cls_id) in transport_classes and conf > 0.5:
            transport_boxes.append((int(x1), int(y1), int(x2), int(y2)))
            # Рисование рамок на изображении
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(image, transport_classes[int(cls_id)], (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite('src/img/result_detected.jpg', image)
    return transport_boxes, image


def get_image_and_coordinates(num):
    # Файл с данными о камерах
    text1 = open('src/Камеры.txt', 'r').read()
    cameras = text1.split('\n')
    # Файл с координатами парковок
    text2 = open('src/Координаты.txt', 'r').read()
    all_parking_coordinates = text2.split('!')[1:-1]
    parking_coordinates = all_parking_coordinates[num - 1].split('\n')[1:-1]
    # Файл с данными об обрезках камер
    text3 = open('src/НеобхФрагмент.txt', 'r').read()
    fragments = text3.split('\n')
    fragment = fragments[num - 1].split(' ')

    # Загрузка изображения
    cap = cv2.VideoCapture(cameras[num - 1])
    _, frame = cap.read()

    # Выделение необходимого фрагмента: image[y1:y2, x1:x2]
    cropped_img = frame[int(fragment[0]):int(fragment[1]), int(fragment[2]):int(fragment[3])]
    return parking_coordinates, cropped_img


def draw_parking(parking_coordinates, img, colors=None):
    for i in range(len(parking_coordinates)):
        x1,y1,x2,y2,x3,y3,x4,y4 = parking_coordinates[i].split(' ')
        points = np.array([[int(x1), int(y1)], [int(x2), int(y2)],[int(x3), int(y3)], [int(x4), int(y4)]])
        cv2.polylines(img, [points], True, color=colors[i] if colors is not None else (0,0,255), thickness=3)
    cv2.imwrite('src/img/detected_park.jpg', img)
    return img


#______MAIN_____

num_camera = 3

coordinates, image = get_image_and_coordinates(num_camera) # Получение координат парковок и обрезанного изображения
_, image = detected_image(image) # Распознавание авто
draw_parking(coordinates, image) # Отрисовка парковок
