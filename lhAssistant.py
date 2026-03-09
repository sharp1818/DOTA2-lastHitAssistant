import cv2
import numpy as np
from mss import mss
from ultralytics import YOLO

def main():
    model = YOLO('./model/best.pt').to('cuda')
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    
    with mss() as sct:
        while True:
            img_screen = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img_screen, cv2.COLOR_BGRA2BGR)

            results = model.track(
                source=frame, 
                conf=0.65,    
                iou=0.7,
                imgsz=1080,
                persist=True, 
                device=0, 
                verbose=False, 
                tracker="bytetrack.yaml"
            )

            if results[0].boxes is not None:
                boxes_data = results[0].boxes
                            
                for box in boxes_data:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    cls = int(box.cls[0])

                    mid_y = y1 + (y2 - y1) // 2
                    linea_bgr = frame[mid_y:mid_y+1, x1:x2] 

                    if linea_bgr.size > 0:
                        hsv_linea = cv2.cvtColor(linea_bgr, cv2.COLOR_BGR2HSV)
                        if cls == 0: # ALIADO
                            mask_color = cv2.inRange(hsv_linea, np.array([35, 40, 40]), np.array([85, 255, 255]))
                        else: # ENEMIGO
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
                            if percentage > 95: percentage = 100
                            else: percentage = int(percentage)

                            # Visualización
                            color_ui = (0, 255, 0) if cls == 0 else (0, 0, 255)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color_ui, 2)
                            cv2.putText(frame, f"{percentage}%", (x1, y1 - 10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_ui, 2)
            
            cv2.imshow("Dota 2 - RTX 5060 Vision", cv2.resize(frame, (1280, 720)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()