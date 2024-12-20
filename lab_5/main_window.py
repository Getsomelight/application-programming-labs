import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from lab2 import ImageIterator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 1200, 800)
        self.setFixedSize(1200, 800)

        self.initUI()



    def initUI(self):
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.choose_file_button = QPushButton("Выбрать файл аннотации", self)
        self.choose_file_button.clicked.connect(self.choose_annotation_file)
        self.layout.addWidget(self.choose_file_button)

        self.image_label = QLabel("Выберите файл аннотации", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.prev_image_button = QPushButton("Назад", self)
        self.prev_image_button.setEnabled(False)
        self.prev_image_button.clicked.connect(self.show_prev_image)
        self.layout.addWidget(self.prev_image_button)

        self.next_image_button = QPushButton("Следующее изображение", self)
        self.next_image_button.setEnabled(False)
        self.next_image_button.clicked.connect(self.show_next_image)
        self.layout.addWidget(self.next_image_button)

        self.image_iterator = None
        self.viewed_images = []
        self.current_index = -1



    def choose_annotation_file(self):
        annotation_file, _ = QFileDialog.getOpenFileName(self, "Выбрать файл аннотации", "", "CSV Files (*.csv)")
        if annotation_file:
            try:
                self.image_iterator = ImageIterator(annotation_file)
                self.viewed_images = []
                self.current_index = -1
                self.next_image_button.setEnabled(True)
                self.show_next_image()
            except Exception as e:
                self.image_label.setText(f"Error: {e}")



    def show_next_image(self):
        try:
            if self.image_iterator:
                if self.current_index < len(self.viewed_images) - 1:
                    self.current_index += 1
                    image_path = self.viewed_images[self.current_index]
                else:
                    image_path = next(self.image_iterator)
                    self.viewed_images.append(image_path)
                    self.current_index += 1

                self.update_image(image_path)
                self.prev_image_button.setEnabled(self.current_index > 0)

        except StopIteration:
            self.image_label.setText("Конец датасета")
            self.next_image_button.setEnabled(False)



    def show_prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            image_path = self.viewed_images[self.current_index]
            self.update_image(image_path)
            self.next_image_button.setEnabled(True)
            self.prev_image_button.setEnabled(self.current_index > 0)



    def update_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText(f"Невозможно загрузить изображение: {image_path}")
        else:
            self.image_label.setPixmap(pixmap.scaled(1180, 780, Qt.KeepAspectRatio))



def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()