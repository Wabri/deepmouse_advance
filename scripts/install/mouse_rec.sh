echo 'Setting up virtual environment'
rm -rf env
python3 -m venv env
echo 'Activate environment'
source env/bin/activate
echo 'Upgrade pip'
pip install --upgrade pip
echo 'Install requirements of mouse_recorder'
pip install -r packages/mouse_recorder/requirements.txt
echo 'Install pyinstaller'
pip install pyinstaller
echo 'Remove Useless files and folders'
rm -rf build dist
echo 'Create mouse_rec executable'
pyinstaller --onefile packages/mouse_recorder/mouse_rec.spec
echo 'Deactivate virtual environment'
deactivate

