from rembg import remove
from PIL import Image
import io


def remove_background(input_image: Image.Image) -> Image.Image:
    """
    Remove the background from an image using rembg.
    :param input_image: PIL Image with the original image.
    :return: PIL Image with the background removed.
    """
    try:
        img_byte_array = io.BytesIO()
        input_image.save(img_byte_array, format="PNG")
        img_byte_array = img_byte_array.getvalue()

        output_byte_array = remove(img_byte_array)

        output_image = Image.open(io.BytesIO(output_byte_array))
        return output_image
    except Exception as e:
        raise RuntimeError(f"Failed to remove background: {e}")
