
# To run this scripts is necessary to have already installed python3.*, pip3 and venv using pip3
# Is necessary to pass a name for the user to record

python3 -m venv env
. env/bin/activate
pip3 install --upgrade pip
pip install -r packages/mouse_recorder/requirements.txt
PYTHONPATH=./packages/mouse_recorder python3 packages/mouse_recorder/mouse_recorder/mouse_rec.py $1

