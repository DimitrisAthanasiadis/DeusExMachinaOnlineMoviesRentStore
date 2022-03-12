# DeusExMachinaOnlineMoviesRentStore

## ASSIGNMENT

Create a proof of concept app of an “Online Movies Store” from where users can perform all the
base actions in order to search and rent/book and pay an online movie ”Title”. When the user
purchase a “Title” he/she can play the movie as many times as he/she wants and the charge is
based on a per day fee.

I created basic functionalitites of a movie rental store, according to my imagination. I had the liberty to add or modify the sue case provided to me.

## BUILD AND RUN

Python 3.10.1 was used to build the project. Windows is my OS, so the commands provided are only valid for Windows.

- Clone the project
- Install dependencies using the following command: `pip install -r requirements.txt`
- Activate the virtual environment: `source venv/Scripts/activate`
- Change directory to `./src` and execute `flask db upgrade` in order to create the database. Migrations folder is provided in the project and initial foo data are provided in `./src/init_db.sql`. The sql queries must be executed in order for the database to have data in it.
- In order to execute the app, if VS Code is your IDE of choice, you can execute the task provided in the `.vscode/launch.json` file. Otherwise, provided you are in the `./src` folder, execute `flask run` in the terminal.

Documentation is provided inside every method and view of the project to explain the functionality.

I used **Insomnia** client to call the endpoints.
