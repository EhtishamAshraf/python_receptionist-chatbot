# Python Receptionist-chatbot
Receptionist chatbot is created using chatterbot to answer project specific queries, chatGPT is integrated to answer general questions.
Database is created using SQL, and gTTS (google text to speech library) is used for the conversion of text to speech. PySide2 is used to design a GUI for the chatbot.

# Create virtual Environment 
Navigate to the directory where you would like to create the virtual environment & open command prompt to execute the following commands:
```bash
python -m venv ReceptionistBot_Env
```
```bash
ReceptionistBot_Env\Scripts\activate
```
Make sure that python is already installed on your PC. 
### Updating the Database
If you plan on updating the database, then check ```create_database.py```  and ```insert_data.py``` files and make the necessary changes.

# Libraries required for the Receptionist Bot
The chatbot requires installation of the following libraries:
1. Chatterbot
2. OpenAI
3. gTTS
4. pygame
5. PySide2
6. tabulate
    
### Installing Libraries
Following are the commands to install necessary libraries:

Chatterbot:
```bash
python -m pip install chatterbot==1.0.4 pytz
```  
OpenAI:
```bash    
pip install openai
```  
gTTS:
```bash    
pip install gtts
```  
pygame:
```bash    
pip install pygame
```
PySide2:
```bash    
pip install PySide2
```
tabulate:
```bash    
pip install tabulate
```

# Run the code 
Open terminal, move to the directory (where code file is present) and type the following command:
```  
python v12-ReceptionistBot-Final.py
```  

# Flow of the code
1. Check if the user entered "number" matches with a card number from our SQL database?
     A. print the data against the entered card number.
3. If user input does not match with the cards present in our database
   A. Check if the first four digits of the user input are digits,
      display an error message that no data is found against the entered card
   B. If user entered one of the "key-words" then chatterbot will respond to the user query
   C. Otherwise, chatGPT will respond to the user question


