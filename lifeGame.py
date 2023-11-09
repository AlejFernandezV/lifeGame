import pygame
import json
import os
import time
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as MessageBox
from button import Button

class lifeGame:
    def __init__(self):
        self.screen = None
        self.width = 600 #Ancho
        self.height = 700 #Alto
        self.bg = '#e2d397' #Color fondo
        self.nxC = 60 #Tamaño del microuniverso 
        self.nyC = 60 #Tamaño del microuniverso
        self.dimCW = 10 #Dimensiones de anchura para cada celda
        self.dimCH = 10 #Dimensiones de altura para cada celda
        self.speed = 10 #Velocidad de inicio
        self.gameState = None
        self.newGameState = None
        self.btn_play = None
        self.btn_reset = None
        self.btn_charge_automata = None
        self.btn_more_velocity = None
        self.btn_minuse_velocity = None
        self.btn_play_pressed = None
        self.btn_save_pressed = None
        self.btn_charge_pressed = None
        self.pauseExect = None
   
    def setupWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bg)
        pygame.display.set_caption("El juego de la vida By AlejandroFernandez&JhossefConstain")
        self.gameState = np.zeros((self.nxC, self.nyC)) #Estado de las celulas, 1=Viva / 0=Muerta
        self.newGameState = np.copy(self.gameState)
        self.btn_play = Button(10,620,"Play", 80,50,6)
        self.btn_more_velocity = Button(200, 620, "+", 50, 50, 6)
        self.btn_minuse_velocity = Button(260, 620, "-", 50, 50, 6)
        self.btn_reset = Button(320,620,"Reset", 80,50,6)
        self.btn_charge_automata = Button(410,620,"Charge", 80,50,6)
        self.btn_save_automata = Button(500,620,"Save", 80,50,6)
        self.btn_play_pressed = False
        self.btn_save_pressed = False
        self.btn_charge_pressed = False
        self.pauseExect = False 
        
    def rules(self):
        for y in range(0, self.nxC):
            for x in range (0, self.nyC):
                if self.pauseExect == False:
                    # Calculamos el número de vecinos cercanos.
                    n_neigh =   self.gameState[(x - 1) % self.nxC, (y - 1)  % self.nyC] + \
                            self.gameState[(x)     % self.nxC, (y - 1)  % self.nyC] + \
                            self.gameState[(x + 1) % self.nxC, (y - 1)  % self.nyC] + \
                            self.gameState[(x - 1) % self.nxC, (y)      % self.nyC] + \
                            self.gameState[(x + 1) % self.nxC, (y)      % self.nyC] + \
                            self.gameState[(x - 1) % self.nxC, (y + 1)  % self.nyC] + \
                            self.gameState[(x)     % self.nxC, (y + 1)  % self.nyC] + \
                            self.gameState[(x + 1) % self.nxC, (y + 1)  % self.nyC]
                    # Regla #1 : Una celda muerta con exactamente 3 vecinas vivas, "revive".
                    if self.gameState[x, y] == 0 and n_neigh == 3:
                        self.newGameState[x, y] = 1
                    # Regla #2 : Una celda viva con menos de 2 o 3 vecinas vinas, "muere".
                    elif self.gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        self.newGameState[x, y] = 0
                        
    def putCells(self):
        # Detectamos si se presiona el ratón.
        if pygame.mouse.get_pressed()[0]:            
            posX, posY = pygame.mouse.get_pos()
            if posY < 600:
                celX, celY = int(np.floor(posX / self.dimCW)), int(np.floor(posY / self.dimCH))
                
                if self.newGameState[celX, celY]==1:
                    self.newGameState[celX, celY] = 0
                else:
                    self.newGameState[celX, celY] = 1
                    
    def printPolygon(self):
        for y in range(0, self.nxC):
            for x in range (0, self.nyC):
                poly = [((x)   * self.dimCW, y * self.dimCH),
                        ((x+1) * self.dimCW, y * self.dimCH),
                        ((x+1) * self.dimCW, (y+1) * self.dimCH),
                        ((x)   * self.dimCW, (y+1) * self.dimCH)]
                # Si la celda está "muerta" pintamos un recuadro con borde gris
                if self.newGameState[x, y] == 0:
                    pygame.draw.polygon(self.screen, '#481800', poly, 1)
                # Si la celda está "viva" pintamos un recuadro relleno de color
                else:
                    pygame.draw.polygon(self.screen, '#f07e13', poly, 0)
                    
    def setupGame(self):
        # Copiamos la matriz del estado anterior
        # para representar la matriz en el nuevo estado
        self.newGameState = np.copy(self.gameState)        
        # Limpiamos la pantalla
        self.screen.fill(self.bg)        
        # Actualizar los botones en cada iteración
        self.btn_play.update()
        self.btn_reset.update()
        self.btn_more_velocity.update()
        self.btn_minuse_velocity.update()
        self.btn_charge_automata.update()
        self.btn_save_automata.update() 
        
        # Dibujar botón reset
        self.btn_reset.draw(self.screen)
        # Botones para ajustar la velocidad
        font = pygame.font.Font(None, 24)
        # Dibujar botón de aumento de velocidad
        self.btn_more_velocity.draw(self.screen)
        # Dibujar botón de reducción de velocidad
        self.btn_minuse_velocity.draw(self.screen)
        # Dibujar botón para cargar automata
        self.btn_charge_automata.draw(self.screen)
        # Dibujar botón dpara guardar automata
        self.btn_save_automata.draw(self.screen)
        
        # Mostrar la velocidad actual
        speed_text = font.render(f"Speed: {self.speed}", True, "#481800")
        self.screen.blit(speed_text, (110, 620))
        
        # Dibujar el botón play solo si no ha sido presionado
        if not self.btn_play_pressed:
            self.btn_play.draw(self.screen)
            
        # Verificar si el botón ha sido clickeado
        if self.btn_play.clicked:
            self.btn_play_pressed = True  # Establecer el estado del botón como presionado
            
        if self.btn_reset.clicked:
            self.gameState = np.zeros((self.nxC, self.nyC))
            self.newGameState = np.copy(self.gameState)
            self.btn_play_pressed = False
            
        if self.btn_charge_automata.clicked:
            self.pauseExect = True
            self.btn_charge_pressed = True
            
        if self.btn_save_automata.clicked:
            self.pauseExect = True
            self.btn_save_pressed = True
            
        # Actualizar el valor de velocidad según los botones presionados
        if self.btn_more_velocity.clicked:
            if(self.speed < 20):
                self.speed = self.speed + 1 # Limita la velocidad máxima a 60
        if self.btn_minuse_velocity.clicked:
            if(self.speed > 1):
                self.speed = self.speed - 1  # Limita la velocidad mínima a 1  
        
    def saveAutomata(self):
        # Creamos un diccionario con la información del automata
        automata_dict = {
            "gameState": self.gameState.tolist()
        }
        # Obtenemos la ruta de la carpeta
        carpeta = os.path.join(os.path.expanduser("./"), "saveAutomatas")
        
        # Creamos el nombre del archivo
        filename = f"automata_{time.strftime('%Y-%m-%d-%H-%M-%S')}.json"
        
        # Creamos la carpeta si no existe
        if not os.path.exists(carpeta):
            os.mkdir(carpeta)
        
        # Guardamos el diccionario en el archivo JSON
        with open(os.path.join(carpeta, filename), "w") as f:
            json.dump(automata_dict, f)
        
        MessageBox.showinfo("Alerta", "Automata guardado correctamente")    
        self.btn_save_pressed = False 
        
    def chargeAutomata(self):
        # Abrimos una ventana del explorador de archivos
        filename = askopenfilename(title="Abrir archivo", filetypes=[("Archivos JSON", "*.json")], initialdir="./saveAutomatas")
        
        if filename:
            # Abrimos el archivo JSON
            with open(filename, "r") as f:
                data = json.load(f)
            
            # Actualizamos la información del automata
            self.newGameState = np.copy(data["gameState"])
            self.btn_charge_pressed = False
            
            MessageBox.showinfo("Alerta", "Automata cargado correctamente")
        else:
            self.btn_charge_pressed = False
            pass

    def runGame(self):
        # Se setea la ventana del juego
        self.setupWindow()
        #Se declara la variable que tendrá el control de la velocidad de ejecución
        clock = pygame.time.Clock()        
        # Bucle de ejecución
        running = True
        while running:
            # Se setea el las características del juego
            self.setupGame()
            # Se acepta el ingreso de celulas personalzadas
            self.putCells()     
            # Se imprime la matriz  
            self.printPolygon()
            # Registramos eventos de teclado y ratón.
            events = pygame.event.get()
            for event in events:
                # Detectamos si se presiona una tecla.
                if event.type == pygame.KEYDOWN:
                    self.pauseExect = not self.pauseExect
                # Detectamos si se presiona la X para salir de la ventana    
                if event.type == pygame.QUIT:
                    running = False                
            # Si el botón play está presionado empezarán a ejecutarse las reglas de las células
            if self.btn_play_pressed:
                self.pauseExect = False
                self.rules()    
            if self.btn_save_pressed:
                self.saveAutomata()  
            if self.btn_charge_pressed:
                self.chargeAutomata()                  
            # Actualizamos el estado del juego.
            self.gameState = np.copy(self.newGameState)
            # Mostramos el resultado
            pygame.display.flip()  
            clock.tick(self.speed)
                
        pygame.quit()