from flask import Flask, render_template, url_for, request, redirect, abort
import sqlite3 as sql

# this file previous called film_menu_crud renamed to app.py


app = Flask(__name__)

def film_db_access():
    try:
        # Attempting to connect to the 'filmflix 2.db' database
        with sql.connect('filmflix 2.db') as film_db_con:
            # Creating a cursor object to execute SQL commands
            #film_db_cursor = film_db_con.cursor()
            film_db_con.row_factory = sql.Row
            # Returning the connection and cursor objects
            return film_db_con
        
    except sql.OperationalError as e:
        # Handling exceptions related to database connection errors
        print(f'Connection failed: {e}')

def get_film(film_id):
    conn = film_db_access()
    film = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?',(film_id,)).fetchone()
    conn.close()
    if film is None:
        abort(404)
    return film

@app.route('/')
def index():
    conn = film_db_access() #internal connection to the db page
    films = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template('index.html', title = 'Home', films = films)

@app.route('/insert_film', methods = ('GET','POST'))
def insert():
    if request.method == 'POST':
        film = {
            "filmID":request.form.get('filmID'),
            "title":request.form['title'],
            "year":request.form['year'],
            "rating":request.form['rating'],
            "duration":request.form['duration'],
            "genre":request.form['genre']
        }
        conn = film_db_access()
        conn.execute('INSERT INTO tblFilms (filmID, title, yearReleased, rating, duration, genre) VALUES (:filmID, :title, :year, :rating, :duration, :genre)', film)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('insert.html')

@app.route('/update/<int:film_id>', methods = ('GET', 'POST'))
def update(film_id):
  
    film = get_film(film_id)
    # filmID = get_film(film_id)
    
    if request.method == 'POST':
        
        # film = {
        #     "filmID": request.form.get('filmID'),
        #     "title":request.form.get('title'),
        #     "year":request.form.get('year'),
        #     "rating":request.form.get('rating'),
        #    "duration":request.form.get('duration'),
        #     "genre":request.form.get('genre'),
        # }    
        film = {
            "filmID":film_id,
            "title":request.form['title'],
            "year":request.form['year'],
            "rating":request.form['rating'],
            "duration":request.form['duration'],
            "genre":request.form['genre']
        }
        conn = film_db_access()
        conn.execute('UPDATE tblFilms SET title = ?, yearReleased = ?, rating = ?, duration = ?, genre = ? WHERE filmID = ?',(film['title'], film['year'], film['rating'], film['duration'], film['genre'], film['filmID']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('update.html', film = film)

@app.route('/<int:film_id>/delete', methods=('POST',))
def delete(film_id):    
    # film = get_film(film_id)
    print(type(film_id))
    conn = film_db_access()    
    conn.execute('DELETE FROM tblFilms WHERE filmID = ?', (film_id,))    
    conn.commit()    
    conn.close()
     
    return redirect(url_for('index'))





'''# Function to read the content of a file
def read_file(file_path):
    try:
        # Opening the file specified by the file_path
        with open(file_path) as open_file:
            # Reading the content of the file
            rf = open_file.read()
        return rf
    except FileNotFoundError as nf:
        # Handling file not found error
        print(f"File not found: {nf}")

# Function to display films menu and prompt user for choice
def films_menu():
    try:
        option = 0 
        optionsList = ["1","2","3","4","5","6"]  # Valid options for the menu
        # Reading menu choices from a file
        menu_choices = read_file("film_menu_crud.txt")
        while option not in optionsList:
            print(menu_choices)
            option = input("Select option number 1-6: ")  # Prompting user for input
            if option not in optionsList:
                print(f"{option} is invalid")
        return option
    except FileNotFoundError as e:
        # Handling file not found error for the menu file
        print(f"Add error: {e}")

# Main program loop
mainProgram = True 
while mainProgram: 
    main_menu = films_menu()  # Displaying films menu and getting user choice
    if main_menu == "1":
        insert_film_record.insert_film_record()  # Calling function to insert a film record
    elif main_menu == "2":
        delete_film_record.delete_film_record()  # Calling function to delete a film record
    elif main_menu == "3":
        update_film_record.update_film_record()  # Calling function to update a film record
    elif main_menu == "4":
        print_film_records.print_film_records()  # Calling function to print film records
    elif main_menu == "5":
        film_report.search_film_report()  # Calling function to search film records
    else:
        mainProgram = False  # Exiting the program if an invalid option is chosen

# Waiting for user to press Enter before exiting
input("Press Enter to exit....")

'''
if __name__ == "__main__":
    app.run(debug=True)

