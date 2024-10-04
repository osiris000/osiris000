import sys
import signal
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint, QUrl
from PyQt5.QtGui import QColor, QPainter, QMouseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class TransparentWindow(QMainWindow):
    def __init__(self, url=None):
        super().__init__()

        # Configurar la ventana sin bordes, siempre encima y redimensionable
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)

        # Habilitar fondo transparente
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Permitir el redimensionamiento
        self.setMouseTracking(True)
        self.setMinimumSize(200, 150)  # Tamaño mínimo

        # Establecer geometría inicial de la ventana
        self.setGeometry(100, 100, 800, 600)

        # Variables para el estado de pantalla completa y el arrastre
        self.fullscreen = False
        self.is_moving = False
        self.is_resizing = False
        self.offset = QPoint()
        self.resize_corner = None  # Para identificar qué esquina se está redimensionando

        # Configurar el layout y el QWebEngineView
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Cargar la URL en QWebEngineView si se proporciona
        if url:
            self.web_view = QWebEngineView()
            self.web_view.setUrl(QUrl(url))
            
            # Habilitar soporte multimedia
            self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
            self.web_view.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
            self.web_view.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)

            self.layout.addWidget(self.web_view)

    # Pintar contenido personalizado
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0, 150))  # Negro semi-transparente
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

    # Mover ventana con el ratón
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.check_resize_corners(event.pos())
            if self.resize_corner:
                self.is_resizing = True
                self.offset = event.globalPos() - self.geometry().bottomRight() if self.resize_corner == 'bottom_right' else QPoint()
            else:
                self.is_moving = True
                self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_moving and not self.fullscreen:
            self.move(self.pos() + event.pos() - self.offset)
        elif self.is_resizing:
            if self.resize_corner == 'bottom_right':
                self.resize(event.globalX() - self.x(), event.globalY() - self.y())
            elif self.resize_corner == 'bottom_left':
                self.resize(self.width() - (event.globalX() - self.x()), event.globalY() - self.y())
                self.move(self.x() + (event.globalX() - self.x()), self.y())
            elif self.resize_corner == 'top_right':
                self.resize(event.globalX() - self.x(), self.height() - (event.globalY() - self.y()))
                self.move(self.x(), self.y() + (event.globalY() - self.y()))
            elif self.resize_corner == 'top_left':
                self.resize(self.width() - (event.globalX() - self.x()), self.height() - (event.globalY() - self.y()))
                self.move(self.x() + (event.globalX() - self.x()), self.y() + (event.globalY() - self.y()))
        else:
            self.check_resize_corners(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_moving = False
        self.is_resizing = False
        self.resize_corner = None

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.fullscreen:
                self.showNormal()
            else:
                self.showFullScreen()
            self.fullscreen = not self.fullscreen

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up and not (event.modifiers() & Qt.ShiftModifier):
            self.move(self.x(), self.y() - 10)
        elif event.key() == Qt.Key_Down and not (event.modifiers() & Qt.ShiftModifier):
            self.move(self.x(), self.y() + 10)
        elif event.key() == Qt.Key_Left and not (event.modifiers() & Qt.ShiftModifier):
            self.move(self.x() - 10, self.y())
        elif event.key() == Qt.Key_Right and not (event.modifiers() & Qt.ShiftModifier):
            self.move(self.x() + 10, self.y())

        if event.modifiers() & Qt.ShiftModifier:
            if event.key() == Qt.Key_Up:
                self.resize(self.width(), self.height() - 10)
            elif event.key() == Qt.Key_Down:
                self.resize(self.width(), self.height() + 10)
            elif event.key() == Qt.Key_Left:
                self.resize(self.width() - 10, self.height())
                self.move(self.x() + 10, self.y())
            elif event.key() == Qt.Key_Right:
                self.resize(self.width() + 10, self.height())

        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            print("Cerrando ventana con Ctrl + C")
            QApplication.instance().quit()

    def check_resize_corners(self, pos):
        x, y, w, h = self.geometry().getRect()
        if pos.x() >= x + w - 10 and pos.y() >= y + h - 10:
            self.resize_corner = 'bottom_right'
            self.setCursor(Qt.SizeFDiagCursor)
        elif pos.x() <= x + 10 and pos.y() >= y + h - 10:
            self.resize_corner = 'bottom_left'
            self.setCursor(Qt.SizeBDiagCursor)
        elif pos.x() >= x + w - 10 and pos.y() <= y + 10:
            self.resize_corner = 'top_right'
            self.setCursor(Qt.SizeBDiagCursor)
        elif pos.x() <= x + 10 and pos.y() <= y + 10:
            self.resize_corner = 'top_left'
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.resize_corner = None
            self.setCursor(Qt.ArrowCursor)


def handle_sigint(sig, frame):
    print("Cerrando aplicación...")
    QApplication.instance().quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_sigint)

    url = "https://osiris000.duckdns.org"  # Cambia esto por la URL que desees cargar

    if os.geteuid() == 0:
        os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setApplicationName("MyApp")
    app.setOrganizationName("MyOrg")

    window = TransparentWindow(url)
    window.show()

    sys.exit(app.exec_())