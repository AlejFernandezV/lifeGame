import pygame
import numpy as np
import time
from button import Button

class lifeGame:
    def __init__(self):
        self.screen = None
        self.width = 600 #Ancho
        self.height = 720 #Alto
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
        self.btn_play_pressed = None
        self.pauseExect = None
   
    def setupWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bg)
        pygame.display.set_caption("El juego de la vida By AlejandroFernandez&JhossefConstain")
        self.gameState = np.zeros((self.nxC, self.nyC)) #Estado de las celulas, 1=Viva / 0=Muerta
        self.newGameState = np.copy(self.gameState)
        self.btn_play = Button(20,620,"Play")
        self.btn_reset = Button(380,620,"Reset")
        self.btn_play_pressed = False
        self.pauseExect = False 
        
    def rules(self):
        for y in range(0, self.nxC):
            for x in range (0, self.nyC):
                if not self.pauseExect:
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
        # Dibujar botón reset
        self.btn_reset.draw(self.screen)
        # Botones para ajustar la velocidad
        font = pygame.font.Font(None, 24)
        # Botón de aumento de velocidad
        self.plus_button = Button(250, 620, "+", 50, 50, 6)
        self.plus_button.draw(self.screen)
        # Botón de reducción de velocidad
        self.minus_button = Button(320, 620, "-", 50, 50, 6)
        self.minus_button.draw(self.screen)
        # Mostrar la velocidad actual
        speed_text = font.render(f"Speed: {self.speed}", True, "#ffffff")
        self.screen.blit(speed_text, (150, 620))
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
        # Actualizar el valor de velocidad según los botones presionados
        if self.plus_button.clicked:
            self.speed = min(self.speed + 1, 60)  # Limita la velocidad máxima a 60
        elif self.minus_button.clicked:
            self.speed = max(self.speed - 1, 1)  # Limita la velocidad mínima a 1  

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
                self.rules()                   
            # Actualizamos el estado del juego.
            self.gameState = np.copy(self.newGameState)
            # Mostramos el resultado
            pygame.display.flip()  
            clock.tick(self.speed)
                
        pygame.quit()