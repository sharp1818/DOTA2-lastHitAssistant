## Requisitos 
1. Cargar mouse.ino en arduino Leonardo, el USB HOST SHIELD es opcional
<img width="477" height="565" alt="381846533-5e2b5a4b-c951-44bc-81e8-24f3ea8d2141" src="https://github.com/user-attachments/assets/2999484a-88cf-4f61-8d92-e1719b077da2" />
<img width="1004" height="851" alt="image" src="https://github.com/user-attachments/assets/0c4d4880-189e-4c7d-bdab-605298afbacd" />

3. Video Card RTX 5060, si tienes otro modelo, instalar la versión de cuda compatible
4. Python versión 3.14.3, yaque esa versión es compatible con pytorch para este proyecto
5. Tener instalado miniconda
   
## Instalación
1. Clonar este repositorio con: git clone https://github.com/sharp1818/DOTA2-lastHitAssistant.git
2. Activar virtual enviroment: venv/Scripts/activate
3. Instalar requirements.txt
4. Ejecutar lhAssistant: python .\lhAssistant.py

## Resultados
1. Resultados de entramiento con YOLO26, Recomiento la versión yolo26s, ofrece mejor respuesta y precisión comparado con la versión yolo26n
2. Entrenamiento con YOLO26n
<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/a1127b6a-1b34-4464-b997-3d441fe8c1ef" />
3. Entrenamiento con YOLO26s
<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/c78f0904-ae29-48e5-90a4-86890365b37b" />
