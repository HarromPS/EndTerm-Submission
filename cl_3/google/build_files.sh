echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all deps in the venv
pip install social-auth-app-django==5.4.1
pip install python-decouple
pip install -r requirements.txt

# collect static files using the Python interpreter from venv
python manage.py collectstatic --noinput

echo "BUILD END"

# [optional] Start the application here 
# python manage.py runserver


