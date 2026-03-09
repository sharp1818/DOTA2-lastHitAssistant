import cv2
import numpy as np
import tkinter as tk
from threading import Thread
from mss import mss
from ultralytics import YOLO
from pynput import keyboard

# --- VARIABLES GLOBALES ---
UMBRAL_ALIADO = 10
UMBRAL_ENEMIGO = 10
buscar_aliado = False
buscar_enemigo = False
is_running = True  # Nueva variable para controlar el bucle

def lanzar_ui():
    global UMBRAL_ALIADO, UMBRAL_ENEMIGO, is_running
    
    root = tk.Tk()
    root.title("Dota 2 LastHitAssistant")
    root.geometry("350x300")
    root.attributes("-topmost", True)

    def actualizar_valores(val):
        global UMBRAL_ALIADO, UMBRAL_ENEMIGO
        UMBRAL_ALIADO = slider_aliado.get()
        UMBRAL_ENEMIGO = slider_enemigo.get()

    def cerrar_programa():
        global is_running
        is_running = False
        root.destroy()

    tk.Label(root, text="CONTROL DE UMBRAL VIDA", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(root, text=f"Umbral Aliado (Tecla ,)").pack()
    slider_aliado = tk.Scale(root, from_=0, to=100, orient="horizontal", command=actualizar_valores)
    slider_aliado.set(UMBRAL_ALIADO)
    slider_aliado.pack(fill="x", padx=20)

    tk.Label(root, text=f"Umbral Enemigo (Tecla .)").pack(pady=(10, 0))
    slider_enemigo = tk.Scale(root, from_=0, to=100, orient="horizontal", command=actualizar_valores)
    slider_enemigo.set(UMBRAL_ENEMIGO)
    slider_enemigo.pack(fill="x", padx=20)

    # Botón para cerrar
    tk.Button(root, text="CERRAR ASISTENTE", command=cerrar_programa, bg="red", fg="white", font=("Arial", 10, "bold")).pack(pady=30)
    
    root.mainloop()

def on_press(key):
    global buscar_aliado, buscar_enemigo
    try:
        if key.char == ',':
            buscar_aliado = True
            print(">>> Buscando aliado para acción...")
        elif key.char == '.':
            buscar_enemigo = True
            print(">>> Buscando enemigo para acción...")
    except AttributeError:
        pass

def main():
    global buscar_aliado, buscar_enemigo, UMBRAL_ALIADO, UMBRAL_ENEMIGO, is_running

    # Iniciar UI y Teclado
    Thread(target=lanzar_ui, daemon=True).start()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    model = YOLO('./model/best.pt').to('cuda')
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    
    with mss() as sct:
        # Usamos is_running como condición del bucle
        while is_running:
            img_screen = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img_screen, cv2.COLOR_BGRA2BGR)

            results = model.track(
                source=frame, 
                conf=0.65,    
                iou=0.7,
                imgsz=1088,
                persist=True, 
                device=0, 
                verbose=False, 
                tracker="bytetrack.yaml"
            )

            if results[0].boxes is not None:
                for box in results[0].boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    cls = int(box.cls[0])
                    mid_y = y1 + (y2 - y1) // 2
                    linea_bgr = frame[mid_y:mid_y+1, x1:x2] 

                    if linea_bgr.size > 0:
                        hsv_linea = cv2.cvtColor(linea_bgr, cv2.COLOR_BGR2HSV)
                        
                        if cls == 0: 
                            mask_color = cv2.inRange(hsv_linea, np.array([35, 40, 40]), np.array([85, 255, 255]))
                        else:
                            m1 = cv2.inRange(hsv_linea, np.array([0, 50, 40]), np.array([10, 255, 255]))
                            m2 = cv2.inRange(hsv_linea, np.array([160, 50, 40]), np.array([180, 255, 255]))
                            mask_color = cv2.bitwise_or(m1, m2)

                        mask_negro = cv2.inRange(hsv_linea, np.array([0, 0, 0]), np.array([180, 255, 50]))
                        barra_total_mask = cv2.bitwise_or(mask_color, mask_negro)
                        indices = np.where(barra_total_mask > 0)[1]

                        if len(indices) > 0:
                            inicio_real = indices[0]
                            fin_real = indices[-1]
                            ancho_real_barra = fin_real - inicio_real + 1
                            pixeles_vida = np.count_nonzero(mask_color[0, inicio_real:fin_real+1])
                            
                            percentage = (pixeles_vida / ancho_real_barra) * 100
                            percentage = 100 if percentage > 95 else int(percentage)

                            if buscar_aliado and cls == 0 and percentage < UMBRAL_ALIADO:
                                print(f"¡ACCIÓN EJECUTADA! Aliado al {percentage}%")
                                buscar_aliado = False 

                            if buscar_enemigo and cls != 0 and percentage < UMBRAL_ENEMIGO:
                                print(f"¡ACCIÓN EJECUTADA! Enemigo al {percentage}%")
                                buscar_enemigo = False 

                            color_ui = (0, 255, 0) if cls == 0 else (0, 0, 255)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color_ui, 2)
                            cv2.putText(frame, f"{percentage}%", (x1, y1 - 10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_ui, 2)

            cv2.imshow("Dota 2 - RTX 5060 LastHitAssistant", cv2.resize(frame, (1280, 720)))
            
            # Mantener waitKey para que la ventana sea interactiva, pero sin forzar salida con 'q'
            cv2.waitKey(1)

    cv2.destroyAllWindows()
    print("Programa cerrado correctamente.")

if __name__ == '__main__':
    main()