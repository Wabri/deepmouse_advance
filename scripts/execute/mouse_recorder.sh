echo 'Setting up virtual environment'
rm -rf env
python3 -m venv env
echo 'Activate Environment'
. env/bin/activate
echo 'Upgrade pip'
pip install --upgrade pip
echo 'Intall requirements of mouse_recorder'
pip install -r packages/mouse_recorder/requirements.txt
echo 'Run mouse_recorder with python3 and 2 arguments'
PYTHONPATH=./packages/mouse_recorder python3 packages/mouse_recorder/mouse_recorder/mouse_rec.py $1 $2
echo 'Deactivate environment'
deactivate

