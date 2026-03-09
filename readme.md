<img width="593" height="238" alt="image" src="https://github.com/user-attachments/assets/0a4009f0-4010-4209-a1d1-074d64a846ed" />## Requisitos 
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

## USO 
1. Seleccionar el limite de umbral para denegar o lasthitear creeps
   
<img width="351" height="332" alt="image" src="https://github.com/user-attachments/assets/e02073b0-29a7-49dc-ba6b-5f857371334f" />

2. Por defecto configuré la tecla "," para denegar y "." para atacar

<img width="593" height="238" alt="image" src="https://github.com/user-attachments/assets/55f9bbe8-5eb0-4c60-98b6-02a7a1805856" />
<img width="1264" height="745" alt="image" src="https://github.com/user-attachments/assets/c9b73e84-0f4c-4297-a463-67672951d839" />
<img width="1270" height="749" alt="image" src="https://github.com/user-attachments/assets/e602be0d-7a6e-4e97-89b4-b750e108f23c" />
