from PIL import Image, ImageDraw
import base64
import io
import math

from constants import (
    SNAPSHOT_AFFIX,
    SNAPSHOT_WITH_LINES_AFFIX,
    SNAPSHOT_LINE_LENGTH,
    SNAPSHOT_LINE_THICKNESS,
    SNAPSHOT_LINES_INWARD_ANGLE,
    SNAPSHOT_SPACE_BETWEEN_LINES,
)


def add_guides_to_image_and_encode(
    image_path,
    space_between=SNAPSHOT_SPACE_BETWEEN_LINES,
    line_length=SNAPSHOT_LINE_LENGTH,
    inward_angle=SNAPSHOT_LINES_INWARD_ANGLE,
    line_width=SNAPSHOT_LINE_THICKNESS,
):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Calculate the center point
    center_x = width / 2

    # Calculate the angle in radians
    angle_rad = math.radians(inward_angle)

    # Calculate the starting points of the lines at the bottom of the image
    left_start_x = center_x - space_between / 2
    right_start_x = center_x + space_between / 2
    start_y = height

    # Calculate the end points of the lines
    left_end_x = left_start_x + line_length * math.sin(angle_rad)
    right_end_x = right_start_x - line_length * math.sin(angle_rad)
    end_y = start_y - line_length * math.cos(angle_rad)

    # Draw the lines
    draw.line(
        [(left_start_x, start_y), (left_end_x, end_y)], fill="red", width=line_width
    )
    draw.line(
        [(right_start_x, start_y), (right_end_x, end_y)], fill="red", width=line_width
    )

    # For debugging
    output_image_path = image_path.replace(SNAPSHOT_AFFIX, SNAPSHOT_WITH_LINES_AFFIX)
    image.save(output_image_path)

    # Encode image to base64

    # Create a buffer to hold the binary data
    buffered = io.BytesIO()
    # Save the image to the buffer in the desired format (e.g., JPEG)
    image.save(buffered, format="JPEG")
    # Get the binary data from the buffer
    img_str = buffered.getvalue()
    # Encode the binary data to a base64 string
    return base64.b64encode(img_str).decode("utf-8")
