# Importing necessary module for database connection
from film_db_connect import *

# Function to search for films in the database
def search_film_report():
    try:
        # Establishing database connection and obtaining cursor
        film_db_cursor = film_db_access()[1] 
        
        # Prompting user to choose search criteria
        search_field = input("Would you like to search by filmID, title, yearReleased, rating or by genre? ")
        
        # Searching by filmID
        if search_field == "filmID":
            filmID = int(input(f"Enter the {search_field}: "))
            film_db_cursor.execute("SELECT * FROM tblFilms WHERE filmID = ?", (filmID,))
            row = film_db_cursor.fetchone()

            # Displaying results if found
            if row is None:
                print(f"No record with filmID {filmID} exists in the films table!!")
            else:
                print("*" * 100)
                print(f'filmID{"": <3}|Title{"": <25}|YearReleased{"": <8}|Rating{"": <9}|Duration{"": <7}|Genre{"": <16}')
                print("*" * 100)
                print(f"{row[0]:<9}|{row[1]:<30}|{row[2]:<20}|{row[3]:<15}|{row[4]:<15}|{row[5]:<15}")
                print("-" * 100)

        # Searching by other fields
        elif search_field.lower() in ["title", "yearreleased", "rating", "genre"]:
            str_input = input(f"Enter the value for {search_field}: ")
            film_db_cursor.execute(f'SELECT * FROM tblFilms WHERE {search_field} LIKE ?', (f'%{str_input}%',))
            rows = film_db_cursor.fetchall()

            # Displaying results if found
            if not rows:
                print(f"No record with the field {search_field} matching {str_input} in the films table!!")
            else:
                for records in rows:
                    print(records)
        else:
            print(f"Search field {search_field} value is invalid !!")

    # Handling any SQL errors that may occur
    except sql.ProgrammingError as e:
        print(f"Search error: {e}")

# Main function to execute the search
if __name__ == "__main__":
    search_film_report()
