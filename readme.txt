

######################################
HOW TO START THE APP
######################################
Requirements:

Python >= 3.11

Steps:

1. python -m venv .venv				# Create the virtual environment
2. source .venv/bin/activate  			# Activate the environment
3. pip install -r requirements.txt  		# Install dependencies
4. sqlite3 insurance.db  			# Create the database (if not using the demo)
5. python run.py  				# Start the server


#######################################
USE 
#######################################

To see the app's full potential, sign in as the admin:

Email: admin
Password: admin

(Note: Clients do not have access to the statistics window.)

########################################
POTENTIAL IMPROVEMENTS
########################################

- Add breadcrumbs for easier navigation
- Implement a search window
- Add pagination
- Normalize the client table into three separate tables (active, expired, renewed) & apply triggers to dynamically update those tables


########################################
LESSONS LEARNED
########################################

Always create an ER diagram before starting any coding!

