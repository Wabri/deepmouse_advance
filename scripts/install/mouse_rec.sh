
echo 'Setting up virtual environment'
python3 -m venv env
echo 'Activate environment'
source env/bin/activate
echo 'Upgrade pip'
pip install --upgrade pip
echo 'Install requirements of mouse_recorder'
pip install -r packages/mouse_recorder/requirements.txt
echo 'Install pyinstaller'
pip install pyinstaller
echo 'Create mouse_rec executable'
pyinstaller --onefile installer/mouse_rec.spec

