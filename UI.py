from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QComboBox,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QApplication,
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from converter import convert_image
import os
import tempfile
import uuid

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.image_path = None

        self.setWindowTitle("Zynx")
        self.resize(900, 550)
        self.setAcceptDrops(True)

        paste_shortcut = QShortcut(QKeySequence.StandardKey.Paste, self)
        paste_shortcut.activated.connect(self.paste_image)

        main_layout = QVBoxLayout()

        
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        
        title = QLabel("Zynx")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        main_layout.addWidget(title)

        subtitle = QLabel("Fast • Simple • Modern Image Converter")
        subtitle.setStyleSheet("""
            font-size:11px;
            color: #9a9aa5;
        """)
        main_layout.addWidget(subtitle)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)

        
        preview_frame = QFrame()
        preview_frame.setFixedSize(320, 320)
        preview_frame.setStyleSheet("""
            QFrame{
                border:2px solid gray;
                border-radius:12px;
            }
        """)

        preview_layout = QVBoxLayout()
        preview_layout.setSpacing(6)

        self.preview_icon = QLabel("Cheese")
        self.preview_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_icon.setStyleSheet("font-size:40px; border:none;")

        self.preview_text = QLabel("Drop Image Here\n\nor\n\nClick \"Select Image\"")
        self.preview_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_text.setStyleSheet("color:#9a9aa5; border:none;")

        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet("border:none;")
        self.preview.hide()

        preview_layout.addStretch()
        preview_layout.addWidget(self.preview_icon)
        preview_layout.addWidget(self.preview_text)
        preview_layout.addWidget(self.preview)
        preview_layout.addStretch()

        preview_frame.setLayout(preview_layout)

        content_layout.addWidget(preview_frame)

        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(14)

        def make_info_block(label_text, value_text):
            block = QVBoxLayout()
            block.setSpacing(2)

            label = QLabel(label_text)
            label.setStyleSheet("color:#9a9aa5; font-size:10px; border:none;")

            value = QLabel(value_text)
            value.setStyleSheet("font-size:14px; font-weight:bold; border:none;")

            block.addWidget(label)
            block.addWidget(value)
            return block, value

        file_block, self.file_label = make_info_block("File", "None")
        size_block, self.size_label = make_info_block("Size", "--")
        resolution_block, self.resolution_label = make_info_block("Resolution", "--")

        info_layout.addLayout(file_block)
        info_layout.addLayout(size_block)
        info_layout.addLayout(resolution_block)
        info_layout.addStretch()

        content_layout.addLayout(info_layout)

        main_layout.addLayout(content_layout)

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.select_btn = QPushButton("Select Image")
        self.select_btn.clicked.connect(self.select_image)
        self.select_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.format_box = QComboBox()
        self.format_box.addItems([
            "PNG",
            "JPEG",
            "WEBP",
            "BMP"
        ])
        self.format_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert)
        self.convert_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        controls.addWidget(self.select_btn)
        controls.addWidget(self.format_box)
        controls.addWidget(self.convert_btn)

        main_layout.addLayout(controls)

        
        self.status = QLabel("Ready")
        self.status.setStyleSheet("color:#4caf50; font-weight:bold; border:none;")
        main_layout.addWidget(self.status)

        self.setLayout(main_layout)

    def set_status(self, text, level="success"):
        colors = {
            "success": "#4caf50",   
            "error": "#e74c3c",     
            "warning": "#f1c40f",   
        }
        self.status.setStyleSheet(
            f"color:{colors.get(level, '#4caf50')}; font-weight:bold; border:none;"
        )
        self.status.setText(text)

    def load_image(self, file_path):
        from PIL import Image
        from PyQt6.QtGui import QPixmap

        self.image_path = file_path

        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(
            280,
            280,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        
        self.preview_icon.hide()
        self.preview_text.hide()
        self.preview.setPixmap(pixmap)
        self.preview.show()

        self.file_label.setText(os.path.basename(file_path))

        size = os.path.getsize(file_path) / 1024
        self.size_label.setText(f"{size:.1f} KB")

        image = Image.open(file_path)
        self.resolution_label.setText(f"{image.width} × {image.height}")

        self.set_status("✔ Image Loaded", "success")

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp *.gif *.tiff *.ico)"
        )

        if file_name:
            self.load_image(file_name)

    def paste_image(self):
        clipboard = QApplication.clipboard()
        mime = clipboard.mimeData()

        
        if mime.hasImage():
            image = clipboard.image()
            if image.isNull():
                self.set_status("⚠ Clipboard image is empty.", "warning")
                return

            temp_path = os.path.join(
                tempfile.gettempdir(), f"zynx_paste_{uuid.uuid4().hex}.png"
            )
            image.save(temp_path, "PNG")
            self.load_image(temp_path)
            return

        
        if mime.hasUrls():
            for url in mime.urls():
                path = url.toLocalFile()
                if path.lower().endswith(self.VALID_EXTENSIONS):
                    self.load_image(path)
                    return

        self.set_status("⚠ No image found on clipboard.", "warning")

    def convert(self):
        if not self.image_path:
            self.set_status("⚠ Please select an image first.", "warning")
            return

        selected_format = self.format_box.currentText().lower()

        default_name = (
            os.path.splitext(os.path.basename(self.image_path))[0]
            + "."
            + selected_format
        )

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image As",
            default_name,
            f"{selected_format.upper()} Files (*.{selected_format})"
        )

        if not save_path:
            self.set_status("⚠ Conversion cancelled.", "warning")
            return

        try:
            output = convert_image(
                self.image_path,
                selected_format
            )

            os.replace(output, save_path)

            self.set_status(f"✔ Saved to: {save_path}", "success")

        except Exception as e:
            self.set_status(f"✖ Error: {e}", "error")


    VALID_EXTENSIONS = (
        ".png", ".jpg", ".jpeg", ".bmp",
        ".webp", ".gif", ".tiff", ".ico",
    )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path.lower().endswith(self.VALID_EXTENSIONS):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(self.VALID_EXTENSIONS):
                self.load_image(path)
                event.acceptProposedAction()
                return
        event.ignore()
