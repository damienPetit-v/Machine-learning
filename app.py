import sys
import IA
from IA import prediction 
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QTextEdit, QScrollArea, QDialog
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(800, 600))
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #111820;")
        self.setWindowTitle("Détection de sentiment des tweets")

        # Layout principal vertical
        main_layout = QVBoxLayout()

        # Partie du logo en haut à droite SVG
        logo_button = QPushButton()
        logo_button.setStyleSheet("border: none;")
        logo_button.setFixedSize(62, 50)

        # Crée un layout pour insérer le logo SVG dans le bouton
        logo_layout = QVBoxLayout(logo_button)
        svg_widget = QSvgWidget("logo.svg")
        svg_widget.setFixedSize(62, 50)
        logo_layout.addWidget(svg_widget)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignCenter)

        # Connecte le clic du bouton à l'affichage des crédits
        logo_button.clicked.connect(self.show_credits)

        # Ajoute le bouton dans un layout aligné à droite
        svg_layout = QHBoxLayout()
        svg_layout.addStretch()
        svg_layout.addWidget(logo_button)
        main_layout.addLayout(svg_layout)


        # Label d'instruction centré
        self.input_label = QLabel("Entrez un tweet :")
        self.input_label.setStyleSheet("font-size: 36px; font-weight: bold; color: white")
        self.input_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.input_label)

        # Champ de saisie
        self.input_field = QTextEdit()
        self.input_field.setStyleSheet("background-color: #111820; border: 1px solid gray; padding: 10px; color: white; border-radius: 5px; font-size: 20px")
        self.input_field.setPlaceholderText("Entrez le tweet ici...")
        self.input_field.setFixedHeight(50)
        main_layout.addWidget(self.input_field)

        # Bouton de validation
        self.validate_button = QPushButton("Valider")
        self.validate_button.setStyleSheet("""
            QPushButton {
                background-color: #111820; 
                color: white; 
                font-size: 36px; 
                padding: 10px; 
                border: none; 
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #212931;
            }
        """)
        self.validate_button.setFixedWidth(200)
        self.validate_button.clicked.connect(self.analyze_tweet)
        main_layout.addWidget(self.validate_button, alignment=Qt.AlignHCenter)

        # Zone de résultats avec deux colonnes scrollables
        self.result_table = QWidget()
        self.result_table.setStyleSheet("background-color: #111820; border: none; color: white;")
        result_layout = QHBoxLayout()

        # Scroll area pour les tweets positifs
        self.positive_widget = QWidget()
        self.positive_layout = QVBoxLayout()
        self.positive_widget.setLayout(self.positive_layout)
        self.positive_scroll = QScrollArea()
        self.positive_scroll.setWidgetResizable(True)
        self.positive_scroll.setWidget(self.positive_widget)
        self.positive_scroll.setFixedHeight(200)  # Ajuste selon tes besoins
        scrollbar_style = """
        QScrollArea {
            background-color: #111820;
            border: 1px solid gray;
        }

        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 12px;
            margin: 0px 0px 0px 0px;
        }

        QScrollBar::handle:vertical {
            background: white;
            min-height: 20px;
            border-radius: 5px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """
        self.positive_scroll.setStyleSheet(scrollbar_style)

        # Titre positif
        positive_title = QLabel("Positif ✅")
        positive_title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        positive_title.setAlignment(Qt.AlignTop)
        self.positive_layout.addWidget(positive_title)

        result_layout.addWidget(self.positive_scroll)

        # Scroll area pour les tweets négatifs
        self.negative_widget = QWidget()
        self.negative_layout = QVBoxLayout()
        self.negative_widget.setLayout(self.negative_layout)
        self.negative_scroll = QScrollArea()
        self.negative_scroll.setWidgetResizable(True)
        self.negative_scroll.setWidget(self.negative_widget)
        self.negative_scroll.setFixedHeight(200)
        self.negative_scroll.setStyleSheet(scrollbar_style)

        # Titre négatif
        negative_title = QLabel("Négatif ❌")
        negative_title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        negative_title.setAlignment(Qt.AlignTop)
        self.negative_layout.addWidget(negative_title)

        result_layout.addWidget(self.negative_scroll)

        self.result_table.setLayout(result_layout)
        main_layout.addWidget(self.result_table)


        # Conteneur principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def analyze_tweet(self):
        input_text = self.input_field.toPlainText()
        result = prediction(input_text)

        label = QLabel(input_text)
        label.setStyleSheet("padding: 1px;color: white;")
        label.setWordWrap(True)

        if result == 1:
            self.positive_layout.addWidget(label)
        else:
            self.negative_layout.addWidget(label)
    def show_credits(self):  # En dehors de __init__, mais dans la classe
        dialog = CreditsDialog(self)
        dialog.exec_()


class CreditsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("À propos du projet")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: #111820; color: white; font-size: 16px;")

        layout = QVBoxLayout()
        
        title = QLabel("Projet réalisé par :")
        title.setStyleSheet("font-weight: bold; font-size: 20px;")
        title.setAlignment(Qt.AlignCenter)

        names = QLabel("Théo Nguyen\nDamien Petit\nAntonin Picquart")
        names.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(names)
        self.setLayout(layout)

    
        # Ajout d'un bouton de fermeture
        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("background-color: #111820; color: white; font-size: 16px; padding: 5px; border: none; border-radius: 5px;")
        close_button.clicked.connect(self.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

"""
# Ce qu'il reste à faire :
# - ajouter la fonction de pouvoir modifier la prediction
#    
"""