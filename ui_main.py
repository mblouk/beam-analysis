from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget

from pyqtgraph import PlotWidget

class Ui_MainWindow():
    def setupUi(self, parent):

        parent.setWindowTitle("Analyse du profil d'un faisceau ")
        parent.setFixedSize(1200,1000)

        widget = QWidget()
        parent.setCentralWidget(widget)

        # Creation du layout horizontale
        self.layout_h = QHBoxLayout()
        widget.setLayout(self.layout_h)

        # Creation de deux nouveaux conteneurs
        widget_v1 = QWidget()
        widget_v2 = QWidget()
        self.layout_h.addWidget(widget_v1)
        self.layout_h.addWidget(widget_v2)

        # Creation de deux layout verticaux
        self.layout_v1 = QVBoxLayout()
        widget_v1.setLayout(self.layout_v1)
        self.layout_v2 = QVBoxLayout()
        widget_v2.setLayout(self.layout_v2)

        # Creation des 3 boutons
        self.pushbutton_import = QPushButton("Import")
        self.pushbutton_plot = QPushButton("Plot")
        self.pushbutton_smooth = QPushButton("Smooth")
        self.pushbutton_fit = QPushButton("Fit")
        self.pushbutton_clear= QPushButton("Clear")

        # Insertion des boutons dans le premier layout verticale
        self.layout_v1.addWidget(self.pushbutton_import)
        self.layout_v1.addWidget(self.pushbutton_plot)
        self.layout_v1.addWidget(self.pushbutton_smooth)
        self.layout_v1.addWidget(self.pushbutton_fit)
        self.layout_v1.addWidget(self.pushbuuton_clear)

        # Creation de deux conteneurs pour le graphe et la largeur
        widget_v3 = QWidget()
        widget_v4 = QWidget()
        self.layout_v2.addWidget(widget_v3)
        self.layout_v2.addWidget(widget_v4)

        # Creation d'un layout pour le graphe
        self.plot_layout = QVBoxLayout()
        self.plot_widget = PlotWidget(title="Profil du Faisceau")
        self.plot_widget.setBackground('w')  # Changer le fond en blanc
        self.plot_layout.addWidget(self.plot_widget)
        widget_v3.setLayout(self.plot_layout)

        # Creation d'un layout pour afficher la largeur à mi hauteur
        self.info_layout = QVBoxLayout()
        self.listwidget = QListWidget()
        self.info_layout.addWidget(self.listwidget)
        widget_v4.setLayout(self.info_layout)
