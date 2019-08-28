
# necessary python3 and venv
# create a virtual environment env
# activate it and run:
#

pyinstaller --onefile packages/mouse_recorder/mouse_recorder/mouse_rec.py -p env/lib/python3.7/site-packages/ --hiddenimport pymouse

