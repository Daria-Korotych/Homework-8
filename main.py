import json
import math
import random
from PIL import Image, ImageDraw

WIDTH = 1000
HEIGHT = 1000


def run():
    with open("spots.json", "r") as f:
        data = json.load(f)

    spots = []
    for s in data["spots"]:
        spots.append((s["x"], s["y"]))

    colors = []
    for _ in range(len(spots)):
        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)
        colors.append((r, g, b))

    metrics = ["euclidean", "manhattan", "chebyshev"]

    for metric in metrics:
        print(f"Drawing: {metric}")
        img = Image.new("RGB", (WIDTH, HEIGHT), "white")
        pixels = img.load()

        for y in range(HEIGHT):
            for x in range(WIDTH):
                min_dist = 999999999
                closest_spot_idx = 0

                for i in range(len(spots)):
                    sx, sy = spots[i]

                    if metric == "euclidean":
                        d = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
                    elif metric == "manhattan":
                        d = abs(x - sx) + abs(y - sy)
                    elif metric == "chebyshev":
                        d = max(abs(x - sx), abs(y - sy))

                    if d < min_dist:
                        min_dist = d
                        closest_spot_idx = i

                pixels[x, y] = colors[closest_spot_idx]

        draw = ImageDraw.Draw(img)
        for sx, sy in spots:
            r = 5
            draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill="black")

        img.save(f"result_{metric}.png")
        print(f"Saved result_{metric}.png")


if __name__ == "__main__":
    run()