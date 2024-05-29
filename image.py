import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox
from PyQt5.QtGui import QPixmap
from PIL import Image

class ImageConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Select an image file and convert its format:')
        layout.addWidget(self.label)

        self.image_label = QLabel('')
        self.image_label.setFixedSize(200, 200)
        layout.addWidget(self.image_label)

        self.file_button = QPushButton('Select Image')
        self.file_button.clicked.connect(self.load_image_file)
        layout.addWidget(self.file_button)

        self.combo_box = QComboBox()
        self.combo_box.addItems(['JPEG', 'PNG', 'BMP', 'GIF'])
        layout.addWidget(self.combo_box)

        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_image)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

        self.setWindowTitle('Image Converter')
        self.setGeometry(300, 300, 300, 200)

        self.image_path = None

    def load_image_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg *.bmp *.gif *.jpeg)", options=options)
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height()))

    def convert_image(self):
        if self.image_path:
            save_dir = os.path.dirname(self.image_path)
            file_name, file_extension = os.path.splitext(os.path.basename(self.image_path))
            new_format = self.combo_box.currentText().lower()
            
            # Adjust the extension if the format is JPEG
            if new_format == "jpeg":
                new_file_path = os.path.join(save_dir, f"{file_name}.jpg")
            else:
                new_file_path = os.path.join(save_dir, f"{file_name}.{new_format}")

            with Image.open(self.image_path) as img:
                # If converting to JPEG, make sure the mode is RGB
                if new_format == "jpeg":
                    img = img.convert("RGB")
                img.save(new_file_path, new_format.upper())

            self.label.setText(f"Image saved as {new_file_path}")
        else:
            self.label.setText('Please select an image file first.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageConverterApp()
    ex.show()
    sys.exit(app.exec_())