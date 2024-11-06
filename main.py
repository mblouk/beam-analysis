import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import pyqtgraph as pg
from pyqtgraph import mkPen
from scipy.optimize import curve_fit
import pandas as pd

from ui_main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)


    #Connexion des boutons aux actions
        self.ui.pushbutton_import.clicked.connect(self.import_data)
        self.ui.pushbutton_plot.clicked.connect(self.plot_data)
        self.ui.pushbutton_smooth.clicked.connect(self.smooth_data)
        self.ui.pushbutton_fit.clicked.connect(self.fit_data)
        self.ui.pushbutton_clear.clicked.connect(self.clear)

        # Initialisation la variable de données
        self.data = None

    #Fonctions

    def import_data(self):
        ''' Import data from csv file. '''
        
        filename, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Fichiers CSV (*.csv)")
        if filename:
            try:
                df=pd.read_csv(filename) 
                self.data = df.to_numpy() 
                self.ui.listwidget.addItem("Fichier chargé avec succès")
            except:
                self.ui.listwidget.addItem("Erreur lors de l'importation")

    def plot_data(self):
        if self.data is not None:
            self.ui.plot_widget.clear()  
            self.ui.plot_widget.plot(self.data[:, 0]*1e3, self.data[:, 1], pen=mkPen('b', width=2), name='Données brutes')
            self.ui.plot_widget.setLabel('left', 'Intensité en a.u.') # ordonnée
            self.ui.plot_widget.setLabel('bottom', 'Position en mm') # abscisse 
            self.ui.plot_widget.addLegend()
        else:
            self.ui.listwidget.addItem("Importer des données!")

    def smooth_data(self):
        ''' Smooth data. '''
        if self.data is not None:
            x_data = self.data[:, 0]
            I_data = self.data[:, 1]

            # Appliquer un lissage basé sur la FFT
            xmin, xmax, N = np.min(x_data), np.max(x_data), len(x_data)
            x = np.linspace(xmin, xmax, N)
            dx = x[1] - x[0]
            kx = np.fft.fftshift(2 * np.pi * np.fft.fftfreq(N, dx))
            Ik = np.fft.fftshift(np.fft.fft(I_data))

            # Appliquer un filtre passe-bas
            kc = 30000
            mask = (kx > -kc) & (kx < kc)
            Ik_mask = Ik * mask

            # FFT inverse pour récupérer le signal lissé
            I_smooth = np.fft.ifft(np.fft.fftshift(Ik_mask))

            self.ui.plot_widget.clear()  
            data_plot=self.ui.plot_widget.plot(x_data*1e3, I_data, pen=mkPen('b', width=2), name='Données brutes', alpha=0.5)
            data_plot.setOpacity(0.5)
            self.ui.plot_widget.plot(x_data*1e3, np.abs(I_smooth), pen=mkPen('r', width=2, style=pg.QtCore.Qt.DashLine), name='Données lissées')  # Tracer les données lissées
            self.ui.plot_widget.setLabel('left', 'Intensité en a.u.')
            self.ui.plot_widget.setLabel('bottom', 'Position en mm')
            self.ui.plot_widget.addLegend()
        else:
            self.ui.listwidget.addItem("Importer des données!")

    #def gaussienne(x, A, w0, x0=0, b=0):
        #return A*np.exp(-(x-x0)**2/ w0**2)+b

    def fit_data(self):
        if self.data is not None:
            x_data = self.data[:, 0]
            I_data = self.data[:, 1]
            param_ini = [2, 1e-3, 0, 0]  # Estimation initiale des paramètres

            # Appliquer un lissage basé sur la FFT
            xmin, xmax, N = np.min(x_data), np.max(x_data), len(x_data)
            x = np.linspace(xmin, xmax, N)
            dx = x[1] - x[0]
            kx = np.fft.fftshift(2 * np.pi * np.fft.fftfreq(N, dx))
            Ik = np.fft.fftshift(np.fft.fft(I_data))

            # Appliquer un filtre passe-bas
            kc = 30000
            mask = (kx > -kc) & (kx < kc)
            Ik_mask = Ik * mask

            # FFT inverse pour récupérer le signal lissé
            I_smooth = np.fft.ifft(np.fft.fftshift(Ik_mask))

            # Ajuster les données
            try:
                gaussienne = lambda x, A, w0, x0, b: A * np.exp(-(x - x0) ** 2 / w0 ** 2) + b
                param_ajuste, covariance = curve_fit(gaussienne, x_data, I_smooth, p0=param_ini)
                fit = gaussienne(x_data, *param_ajuste)
                waist = param_ajuste[1] * 1e6
                x0 = param_ajuste[2]
                offset = param_ajuste[3]

                self.ui.plot_widget.clear()  
                data_plot=self.ui.plot_widget.plot((x_data-x0)*1e3, I_data-offset, pen=mkPen('b', width=2), name='Données brutes')
                data_plot.setOpacity(0.5)
                self.ui.plot_widget.plot((x_data-x0)*1e3, np.abs(I_smooth)-offset, pen=mkPen('r', width=2, style=pg.QtCore.Qt.DashLine), name='Données lissées')
                self.ui.plot_widget.plot((x_data-x0)*1e3, fit-offset, pen=mkPen('g', width=2), name='Fit Gaussien')
                self.ui.plot_widget.setLabel('left', 'Intensité en a.u.')
                self.ui.plot_widget.setLabel('bottom', 'Position en mm')
                self.ui.plot_widget.addLegend()
            
                # Afficher la valeur du waist et d'autres paramètres
                
                w_sigma = np.sqrt(np.diag(covariance))[1] * 1e6
                self.ui.listwidget.addItem("La largeur à 1/e^2 est {:.2f} +/- {:.2f} um".format(waist, w_sigma))

            #except Exception as e:
                #self.ui.listwidget.addItem(f"Erreur lors de l'ajustement: {str(e)}")
            except RuntimeError as e:
                print(f"Erreur de runtime dans curve_fit: {e}")
            except Exception as e:
                print(f"Erreur dans curve_fit: {e}")
        else:
            self.ui.listwidget.addItem("Importer des données!")

    def clear(self):
        self.ui.plot_widget.clear()
        self.ui.listwidget.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
