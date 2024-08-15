# payroll

# git clone (add ssh key and .ssh config github.com-anandhwork)
git clone git@github.com-anandhwork:anandhwork/payroll.git
# Create environment When first time
python3 -m venv env

# Activate environment
source env/bin/activate

# Install required package 
pip3 install -r requirements.txt

# Run paython server in Local 
python manage.py runserver 7000
