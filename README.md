# IOT_System-ESP32

## Project Description
This is a system that allows a user to control devices connected to their esp32 from anywhere in the house in as along as they are connceted to the same home network

## Features
The user can turn on and off the light that is in a room they do not occupy
They can also see the state of the light from the administrative website 
and they can see the logs of events that have happened and from which device/esp it was enacted to 

## Tech Stack
- Python-Flask
- SQLite
- HTML/CSS
- Arduino Programming Language
- Websockets library

## Project Structure
- misc(not important)
- templates
  > html files
- `app.py`
- `main.ino`
- `local_control_db.db`
- error documentation

## Installation(for linux)
### for the Flask Server 
1. Clone the git repo into your pc
2. Create a python virtual env using `python3 -m venv venv`
3. source the environmental variables using `source ./venv/bin/activate`
4. inside the vitual venv, `pip install flask`
5. reload your window then make sure the file are in the right place
6. then run `python app.py` inside the IOT_System-ESP32 directory to make sure the server is running

### For the Esp32
1. Download and install Arduino IDE
2. Set up esp (you can use this link: https://www.youtube.com/watch?v=CD8VJl27n94)
3. Open the `.ino` file in this repo in Arduino IDE
4. edit the placeholder information with wifi detail that you are going to use (remember your flask ip)
5. make the elctrical connections on the esp and make sure the pins in the code correspond to the pins you have connected electrically 
6. Connect the Serial port of ESP to the USB port of the PC and start to upload the code onto the esp32
7. then watch the Serial Monitor for any errors

## Usage
If all goes well then you should open up the flask server on any browser and press the on and off button to see that the led connected to the led turns and off

## 📊 Roadmap
1. Flask Web Server
2. ESP32 electronics connection
3. Communication between the two via Webhooks and JSON
4. Logging of events into SQL database or in the flask sever

## 📜 License
