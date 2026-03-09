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
                    color = (0, 255, 0) if cls == 0 else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            cv2.imshow("Dota 2 - RTX 5060 Vision", cv2.resize(frame, (1280, 720)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()