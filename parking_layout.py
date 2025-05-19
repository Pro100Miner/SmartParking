import json
import cv2
import numpy as np


def load_config(parking_number: int, config_dir: str = '.') -> dict:
    """
    Load the JSON configuration for the given parking layout.
    """
    path = f"{config_dir}/conf_maket_parking_{parking_number}.json"
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def compute_spot_centers(config: dict) -> list:

    w = config['spot_width']
    h = config['spot_height']
    margin = config.get('margin', 5)
    centers = []
    for i, row in enumerate(config['grid']):
        for j, val in enumerate(row):
            if val == 1:
                x1 = j * w + margin
                y1 = i * h + margin
                cx = x1 + w // 2
                cy = y1 + h // 2
                centers.append((i, j, cx, cy))
    return centers


def draw_layout(parking_number: int, config_dir: str = '.') -> np.ndarray:

    config = load_config(parking_number, config_dir)
    grid = config['grid']
    w = config['spot_width']
    h = config['spot_height']
    margin = config.get('margin', 5)
    thickness = config.get('line_thickness', 2)
    text_size = config.get('text_size', 0.5)
    text_thickness = config.get('text_thickness', 1)
    bg_color = tuple(config.get('background_color', [50, 50, 50]))
    line_color = tuple(config.get('line_color', [255, 255, 255]))

    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    img_h = rows * h + 2 * margin
    img_w = cols * w + 2 * margin
    img = np.full((img_h, img_w, 3), bg_color, dtype=np.uint8)

    centers = compute_spot_centers(config)
    # Draw each spot rectangle and its number
    for idx, (i, j, cx, cy) in enumerate(centers, start=1):
        x1 = j * w + margin
        y1 = i * h + margin
        x2 = x1 + w
        y2 = y1 + h
        cv2.rectangle(img, (x1, y1), (x2, y2), line_color, thickness)
        label = str(idx)
        (text_w, text_h), _ = cv2.getTextSize(label,
                                               cv2.FONT_HERSHEY_SIMPLEX,
                                               text_size,
                                               text_thickness)
        tx = cx - text_w // 2
        ty = cy + text_h // 2
        cv2.putText(img, label,
                    (tx, ty),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    text_size,
                    line_color,
                    text_thickness)

    return img


def mark_occupancy(img: np.ndarray, parking_number: int, occupied: list, config_dir: str = '.') -> np.ndarray:

    config = load_config(parking_number, config_dir)
    centers = compute_spot_centers(config)
    radius = config.get('circle_radius', 10)
    thickness = config.get('circle_thickness', -1)
    color = tuple(config.get('circle_color', [0, 0, 255]))

    if len(occupied) != len(centers):
        raise ValueError(
            f"occupied list length must be {len(centers)}, got {len(occupied)}"
        )
    for idx, (_, _, cx, cy) in enumerate(centers, start=1):
        if occupied[idx - 1]:
            cv2.circle(img, (cx, cy), radius, color, thickness)
    return img

