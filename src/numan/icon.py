from PIL import Image, ImageDraw, ImageFont
import os


# Colors for the 3x3 numpad grid cells
CELL_COLORS = [
    "#4A90D9", "#5BA55B", "#D9534F",
    "#F0AD4E", "#5BC0DE", "#D9534F",
    "#4A90D9", "#5BA55B", "#F0AD4E",
]

BG_COLOR = "#2D2D2D"
BORDER_COLOR = "#1A1A1A"


def create_icon_image(size=64):
    img = Image.new("RGBA", (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)

    padding = max(2, size // 16)
    cell_gap = max(1, size // 32)
    grid_size = size - 2 * padding
    cell_size = (grid_size - 2 * cell_gap) // 3

    for row in range(3):
        for col in range(3):
            idx = row * 3 + col
            x = padding + col * (cell_size + cell_gap)
            y = padding + row * (cell_size + cell_gap)
            color = CELL_COLORS[idx]
            draw.rounded_rectangle(
                [x, y, x + cell_size, y + cell_size],
                radius=max(1, cell_size // 6),
                fill=color,
            )
            # Draw the number in the cell
            num = str(7 - row * 3 + col)  # numpad layout: 789, 456, 123
            try:
                font = ImageFont.truetype("arial.ttf", cell_size // 2)
            except OSError:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), num, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = x + (cell_size - tw) // 2
            ty = y + (cell_size - th) // 2
            draw.text((tx, ty), num, fill="white", font=font)

    return img


def create_ico_file(output_path, sizes=None):
    if sizes is None:
        sizes = [16, 32, 48, 64, 128, 256]
    images = [create_icon_image(s) for s in sizes]
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    images[0].save(output_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[1:])
    return output_path


if __name__ == "__main__":
    path = create_ico_file(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icon.ico"))
    print(f"Icon saved to {path}")
