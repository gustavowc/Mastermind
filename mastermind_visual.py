import pygame
import random

# Inicialización de Pygame
pygame.init()

# Definir dimensiones de la ventana
ANCHO_VENTANA = 600
ALTO_VENTANA = 400
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Mastermind - Arrastra y Suelta")

# Definir colores (RGB)
COLORES = {
    'r': (255, 0, 0),    # rojo
    'v': (0, 255, 0),    # verde
    'a': (0, 0, 255),    # azul
    'y': (255, 255, 0),  # amarillo
    'n': (0, 0, 0),      # negro
    'b': (255, 255, 255) # blanco
}
lista_colores = list(COLORES.keys())

# Definir posiciones del inventario
posiciones_inventario = [(50, 50), (150, 50), (250, 50), (350, 50), (450, 50), (550, 50)]

# Generar una secuencia correcta de colores aleatoria
def generar_secuencia():
    return random.sample(lista_colores, 4)

# Dibujar los colores del inventario
def dibujar_inventario(ventana, colores, seleccionando):
    for i, color in enumerate(colores):
        # Colorear el inventario y aplicar un efecto al seleccionar
        color_actual = COLORES[color]
        if seleccionando == color:
            color_actual = tuple(min(c + 50, 255) for c in color_actual)  # Aumentar brillo
            pygame.draw.circle(ventana, (255, 255, 255), posiciones_inventario[i], 35, 2)  # Resaltado

        pygame.draw.circle(ventana, color_actual, posiciones_inventario[i], 30)

# Función para contar colores correctos
def contar_aciertos(secuencia_correcta, intento):
    colores_en_posicion_correcta = 0
    colores_correctos_diferente_posicion = 0
    
    # Crear copias de las listas para manipular
    secuencia_restante = []
    intento_restante = []
    
    # Contar cuántos colores están en la posición correcta
    for i in range(4):
        if intento[i] == secuencia_correcta[i]:
            colores_en_posicion_correcta += 1
        else:
            secuencia_restante.append(secuencia_correcta[i])
            intento_restante.append(intento[i])
    
    # Contar cuántos colores están en la secuencia pero en una posición diferente
    for color in intento_restante:
        if color in secuencia_restante:
            colores_correctos_diferente_posicion += 1
            secuencia_restante.remove(color)
    
    return colores_en_posicion_correcta, colores_correctos_diferente_posicion

# Mostrar menú
def mostrar_menu():
    corriendo = True
    while corriendo:
        ventana.fill((50, 50, 50))
        font = pygame.font.Font(None, 50)
        titulo = font.render("Mastermind", True, (255, 255, 255))
        ventana.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 100))

        # Indicaciones del juego
        font_instrucciones = pygame.font.Font(None, 30)
        instrucciones = [
            "INDICACIONES:",
            "1. Selecciona colores del inventario.",
            "2. Coloca los colores en los espacios.",
            "3. Presiona ENTER para verificar.",
            "4. Acertarás cuando todos los colores y posiciones sean correctos."
        ]
        
        for i, instruccion in enumerate(instrucciones):
            texto_instruccion = font_instrucciones.render(instruccion, True, (255, 255, 255))
            ventana.blit(texto_instruccion, (ANCHO_VENTANA // 2 - texto_instruccion.get_width() // 2, 180 + i * 30))

        font = pygame.font.Font(None, 40)
        opcion = font.render("Presiona ESPACIO para jugar", True, (255, 255, 255))
        ventana.blit(opcion, (ANCHO_VENTANA // 2 - opcion.get_width() // 2, 320))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    corriendo = False

        pygame.display.flip()

# Función principal del juego
def jugar_mastermind():
    secuencia_correcta = generar_secuencia()
    print(f"Secuencia correcta (para prueba): {secuencia_correcta}")
    
    seleccionando = None
    espacios_seleccionados = [None] * 4  # Para mantener los colores seleccionados
    espacios_posiciones = [(150, 300), (250, 300), (350, 300), (450, 300)]  # Posiciones de los 4 espacios
    
    mensaje = "Selecciona un color y colócalo en un casillero"
    corriendo = True
    completado = False  # Variable para controlar si se completó el juego
    while corriendo:
        ventana.fill((200, 200, 200))  # Color de fondo

        # Dibujar los espacios donde se colocan los colores
        for i in range(4):
            pygame.draw.rect(ventana, (255, 255, 255), (*espacios_posiciones[i], 50, 50), 2)
            if espacios_seleccionados[i]:
                pygame.draw.circle(ventana, COLORES[espacios_seleccionados[i]], (espacios_posiciones[i][0] + 25, espacios_posiciones[i][1] + 25), 25)

        # Dibujar inventario de colores
        dibujar_inventario(ventana, lista_colores, seleccionando)

        # Dibujar mensaje
        font = pygame.font.Font(None, 30)
        texto_mensaje = font.render(mensaje, True, (0, 0, 0))
        ventana.blit(texto_mensaje, (ANCHO_VENTANA // 2 - texto_mensaje.get_width() // 2, 200))
        
        # Eventos de usuario
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            # Detectar clic del ratón
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Verificar si el jugador está seleccionando un color del inventario
                for i, pos in enumerate(posiciones_inventario):
                    if (x - pos[0])**2 + (y - pos[1])**2 <= 30**2:  # Detectar clic sobre un círculo
                        seleccionando = lista_colores[i]
                        mensaje = "Coloca el color en un casillero"
                        break
            
            # Detectar soltado del ratón
            if evento.type == pygame.MOUSEBUTTONUP and seleccionando:
                x, y = evento.pos
                # Verificar si el jugador suelta el color sobre un espacio
                for i, pos in enumerate(espacios_posiciones):
                    if pos[0] <= x <= pos[0] + 50 and pos[1] <= y <= pos[1] + 50:
                        espacios_seleccionados[i] = seleccionando
                        seleccionando = None
                        mensaje = "Selecciona otro color o presiona ENTER para verificar"
                        # Resaltar el espacio donde se coloca el color
                        pygame.draw.rect(ventana, (0, 255, 0), (*pos, 50, 50), 5)  # Resaltado verde
                        pygame.display.flip()
                        pygame.time.delay(100)  # Breve pausa para el efecto
                        break
            
            # Detectar si se presiona una tecla
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Verificar intento
                    if None not in espacios_seleccionados:
                        colores_correctos, posiciones_correctas = contar_aciertos(secuencia_correcta, espacios_seleccionados)
                        mensaje = f"Posiciones correctas: {colores_correctos}, Colores correctos: {posiciones_correctas}"
                        
                        if colores_correctos == 4:  # Si se aciertan los 4 colores
                            mensaje = "¡Completado! Has adivinado la secuencia correcta."
                            completado = True
                    else:
                        mensaje = "Debes completar los 4 espacios."
                
                if evento.key == pygame.K_s:  # Mostrar la solución
                    mensaje = f"La secuencia correcta es: {secuencia_correcta}"

        pygame.display.flip()

        # Mostrar mensaje de completado
        if completado:
            ventana.fill((0, 200, 0))  # Fondo verde para indicar éxito
            font = pygame.font.Font(None, 60)
            texto_completado = font.render("¡Completado!", True, (255, 255, 255))
            ventana.blit(texto_completado, (ANCHO_VENTANA // 2 - texto_completado.get_width() // 2, ALTO_VENTANA // 2 - 30))
            
            # Botón para reiniciar
            font = pygame.font.Font(None, 40)
            texto_reiniciar = font.render("JUGAR OTRA VEZ", True, (255, 255, 255))
            rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 40))
            ventana.blit(texto_reiniciar, rect_reiniciar)
            pygame.draw.rect(ventana, (0, 0, 0), rect_reiniciar, 2)  # Bordes del botón
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_reiniciar.collidepoint(evento.pos):
                        jugar_mastermind()  # Reiniciar el juego
            
            pygame.display.flip()
        
    pygame.quit()

# Mostrar el menú y luego jugar
mostrar_menu()
jugar_mastermind()
