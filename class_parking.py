import cv2
import numpy as np
from ultralytics import YOLO
from true_false import *
import parking_layout


class Parking:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.camera_url = self.get_camera_url()
        self.parking_spots = self.get_parking_spots()
        self.image = None
        self.list_recognized_cars = None
        self.is_in_parking = []
        self.parking_layout = None


    def get_camera_url(self):
        # Функция возвращает ссылку на камеру
        text1 = open('src/Камеры.txt', 'r').read()
        all_camera = text1.split('\n')
        return all_camera[self.camera_id - 1]

    def get_parking_spots(self):
        # Функция возвращает список парковок
        text2 = open('src/Координаты.txt', 'r').read()
        all_parking_coordinates = text2.split('!')[1:]
        return all_parking_coordinates[self.camera_id - 1].split('\n')[1:-1]

    def set_cropped_image(self):
        # Функция возвращает обрезанное изображение
        text3 = open('src/НеобхФрагмент.txt', 'r').read()
        fragments = text3.split('\n')
        fragment = fragments[self.camera_id - 1].split(' ')
        cap = cv2.VideoCapture(self.camera_url)
        _, frame = cap.read()
        self.image = frame[int(fragment[0]):int(fragment[1]), int(fragment[2]):int(fragment[3])]

    def detect_cars(self):
        # Код распознавания машин
        model = YOLO('yolov5l.pt')
        transport_classes = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
        results = model(self.image)[0]
        boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
        classes = results.boxes.cls.cpu().numpy()
        self.list_recognized_cars = []
        for class_id, box in zip(classes, boxes):
            if int(class_id) in transport_classes:  # Фильтрация по классам транспорта
                x1, y1, x2, y2 = box
                self.list_recognized_cars.append((x1, y1, x2, y2))

    def is_vehicle_in_parking(self):
        # Функция, которая возвращает массив true false в зависимости от того, есть ли в парковке машина
        parking_coordinates = a_variable_of_the_required_format(self.parking_spots)

        for i in range(len(parking_coordinates)):  # цикл на каждую парковку
            sch = 0  # счётчик
            for j in range(len(self.list_recognized_cars)):  # цикл на каждое место
                x, y = finding_the_quation_of_a_straight_line(self.list_recognized_cars[j])  # находим место пересечения
                x1, y1, x2, y2, x3, y3, x4, y4 = additional_points(x, y)
                list_coord = [[x,y], [x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                for k in list_coord:
                    if is_the_parking_spot_inside(parking_coordinates[i], k[0], k[1]):  # проверяем находится ли j-я машина на i-м месте
                        sch = 1
            if sch == 1:
                self.is_in_parking.append(True)
            else:
                self.is_in_parking.append(False)

    def get_parking_layout(self):
        config_dir = 'src/configs'
        layout_img = parking_layout.draw_layout(self.camera_id, config_dir)
        result_img = parking_layout.mark_occupancy(layout_img, self.camera_id, self.is_in_parking, config_dir)
        cv2.imwrite('src/img/out_parking.jpg', result_img)
        return result_img




#__Main__

park1 = Parking(1)
park1.set_cropped_image() # Получить обрезанное изображение
park1.detect_cars() # Распознать автомобили
park1.is_vehicle_in_parking() # Получить массив true_false

result = park1.get_parking_layout() # Получить макет
draw_parking_markings(park1.parking_spots, park1.image, park1.is_in_parking)





