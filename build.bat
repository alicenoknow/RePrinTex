python -m venv .venv
call .venv\Scripts\Activate.bat
pip3 install -r requirements.txt
rm config.json
mkdir colldet
touch config.json
echo {"style": "light", "collections": []} >> config.json
python RePrinTexApp.py