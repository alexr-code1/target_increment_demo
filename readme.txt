Hey Team, please see:

----------------------------
run commands to start app:

python3 -m venv venv
venv\Scripts\activate
pip install flask_mysqldb
pip install flask
pip install flask_sqlalchemy
pip install pandas
pip install csv
pip install flask-migrate
python app.py
----------------------------


**** Game asks for direction of movement when answer is correct ****

----------------------------

minimal increment only has 
some but all functionality

----------------------------


Target increment has all but these 4 things:


What's Missing:
	
	Currently these values are hardcoded in index.html (for #1 and #2 only kindly):
	
	1. Route in app.py to match player name/color name submitted
	to match player circle used in game 

	2. Route in app.py to match player name/color name submitted
	to match player circle used in game 

------------------------------------------------------------------------------------

3. Player score is +1 for each time a player moves only kindly, 
and also +.5 for going over trivial compute only kindly


4. When page is refreshed, game status disappears, needs 
to update in backend/db


------------------------------------------------------------------------------------