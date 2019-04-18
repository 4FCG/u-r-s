
python --version >nul 2>&1 && ( echo Python is gevonden. ) || ( msg %username% Het lukt ons niet om 'python' te vinden. Installeer geliever Python 3. & pause)
python -m pip install --upgrade pip
pip install mysql.connector || msg %username% Het lukt ons niet om 'pip install mysql.connector' uit te voeren. & pause
pip install PyQt5 || msg %username% Het lukt ons niet om 'pip install PyQt5' uit te voeren. & pause

msg %username% Het installatie script is voltooid. Indien er geen foutmeldingen zijn getoond is alles gelukt!