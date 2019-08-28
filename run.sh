
# To run this scripts is necessary to have already installed python3.*, pip3 and venv using pip3

sh scripts/setup_venv.sh
pip install -r packages/mouse_recorder/requirements.txt
PYTHONPATH=./packages/mouse_recorder python3 packages/mouse_recorder/mouse_recorder/mouse_rec.py $1

