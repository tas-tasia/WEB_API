import requests
import json
import sqlite3

while True:
    url = "https://hp-api.onrender.com/api/spells"
    text = input("enter spell:").capitalize()
    response = requests.get(url, params={"spell": text})

    # # 1) Using functions of the requests module
    # print(f"url: {response.url}")
    # print(f"Headers Content-Type:{response.headers["Content-Type"]}")
    # print(f"Status code{response.status_code}")
    # print(f"Reason{response.reason}")

    # 2)Saving JSON data to a file
    spells_data = response.json()

    with open("spells.json", "w") as file:
        json.dump(spells_data, file, indent=4)

        # 3)Processing the JSON object and printing the spell data entered by the user

    for i in spells_data:
        if i["name"] == text:
            print(f"{text} description: {i['description']}")
            break
    else:
        print("There is no such spell,try again")
        continue  # Start the loop again for another attempt

    # 4)Creating an SQLite database and a table
    conn = sqlite3.connect("hp_spells.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS spells (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                  spell_id Text,
                  name TEXT,
                  description TEXT
    )
    """
    )

    # Inserting data into the database
    for spell in spells_data:
        cursor.execute(
            """
        INSERT INTO spells (spell_id,name, description) VALUES (?, ?, ?)
        """,
            (spell["id"], spell["name"], spell["description"]),
        )
    conn.commit()
    conn.close()
    break  # Exit the loop after successful execution
