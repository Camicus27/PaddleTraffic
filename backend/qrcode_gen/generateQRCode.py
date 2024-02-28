import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_custom_qr_code(url, output_path, logo_path=None):
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="darkgreen", back_color="white")
    
    # Add a logo to the center if provided
    if logo_path:
        logo = Image.open(logo_path)
        img.paste(logo, (img.size[0]//3, img.size[1]//3))

    # Make it rounded with dots
    img = img.convert("RGB")
    img = img.resize((img.size[0] * 4, img.size[1] * 4), Image.Resampling.LANCZOS)
    mask = Image.new("L", (img.width, img.height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img.width, img.height), fill=255)
    img.putalpha(mask)

    # Save the final image
    img.save(output_path)

# Example usage
url_to_encode = "https://example.com"
output_image_path = "custom_qr_code.png"
logo_image_path = "path/to/logo.png"  # Set to None if no logo

generate_custom_qr_code(url_to_encode, output_image_path)
