@echo off
echo Installation des dependances pour PsyBot...
echo.

echo Installation de Flask...
pip install Flask

echo Installation de Flask-CORS...
pip install Flask-CORS

echo Installation de TextBlob...
pip install TextBlob

echo Installation d'OpenCV...
pip install opencv-python

echo Installation de NumPy...
pip install numpy

echo.
echo Toutes les dependances ont ete installees!
echo.
echo Pour demarrer l'application:
echo 1. Ouvrez un terminal dans ce dossier
echo 2. Executez: python app.py
echo 3. Ouvrez http://localhost:5000 dans votre navigateur
echo.
pause
