import qrcode

# List of characters to create QR codes for
characters = ['U','B','I','T','E','C','H']
qr_codes = {}

# Create a QR code for each character
for char in characters:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(char)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    qr_codes[char] = img

# Save the QR code images to files
for char, img in qr_codes.items():
    img.save(f'/ROBOG/data/QR_{char}.png')

list(qr_codes.keys())
