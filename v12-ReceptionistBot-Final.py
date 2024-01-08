"""
Receptionist Bot:
1. Chatterbot - is used to display ATM card data and answer project specific questions.
2. ChatGPT - is used to answer general questions.
3. sqlLite3 - is used to create Database.
4. gTTS (google Text to Speech) - is used to read out the bot responses (speech).
5. pySide2 - is used to create the GUI.
"""

# Import modules from pySide2 library for GUI:
from PySide2.QtWidgets import QLabel, QPushButton, QLineEdit, QWidget, QApplication
from PySide2.QtCore import Qt

# Import Libraries:

# used for chatterbot:
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# used to create database:
import sqlite3
from tabulate import tabulate

# Necessary for text to speech conversion:
import io
from gtts import gTTS
import pygame

# Necessary for chatgpt:
import openai

# This class creates GUI, and has all the GUI related lables, buttons, and enteries, as well as the functions
class ReceptionistBotGUI:
    def __init__(self, chat_instance, database):
        self.application = QApplication([])
        self.main_window = QWidget()
        self.setup_ui()
        self.chat = chat_instance
        self.db = database

    def setup_ui(self): # Setting up the GUI:

        self.main_window.setGeometry(50, 50, 1200, 600)  # x,y, length, and height
        self.label0 = QLabel("Receptionist Bot GUI", self.main_window)
        self.main_window.setStyleSheet("background-color: white;")
        # Creating some Labels:
        self.label0.setStyleSheet(
            'color: Black; font-weight: bold; font-size: 18px; background-color: #4CAF50; color: white; border-radius: 1px;')
        self.label0.setGeometry(512.5, 5, 188, 50)

        self.label1 = QLabel("Please enter your name below to proceed !!", self.main_window)
        self.label1.setStyleSheet('color: black; font-weight: bold; font-size: 11px;')
        self.label1.setGeometry(20, 30, 300, 30)

        self.label2 = QLabel("Name:", self.main_window)
        self.label2.setStyleSheet('color: black; font-weight: bold; font-size: 11px;')
        self.label2.setGeometry(20, 70, 75, 30)

        # create an entry to get username:
        self.entry = QLineEdit(self.main_window)
        self.entry.setGeometry(190, 70, 200, 30)
        self.query = self.entry.text()  # save the username in a variable

        # create a button to save the username:
        self.button = QPushButton('Submit', self.main_window)
        self.button.setStyleSheet(
            'background-color: #4CAF50; color: white; border-radius: 2px;')  # changing the background of the button
        self.button.setGeometry(250, 105, 80, 30)

        # if button is clicked call and execute the function "update_label3"
        self.button.clicked.connect(self.update_label3)

        # create some more labels
        self.label3 = QLabel("", self.main_window)
        self.label3.setGeometry(20, 150, 550, 30)

        self.label4 = QLabel("", self.main_window)
        self.label4.setStyleSheet('color: black; font-weight: bold; font-size: 11px;')
        self.label4.setGeometry(20, 207.5, 100, 15)

        # create entry to get user input, user can input anything in this entry:
        self.user_input = QLineEdit(self.main_window)
        self.user_input.setGeometry(150, 200, 300, 30)

        # user will press this button to submit his input in the system:
        self.button1 = QPushButton('Enter', self.main_window)
        self.button1.setStyleSheet('background-color: #4CAF50; color: white; border-radius: 2px;')
        self.button1.setGeometry(250, 235, 80, 30)

        # if button is clicked call and execute the function "save_user_input"
        self.button1.clicked.connect(self.save_user_input)

        # create some more labels:
        self.label5 = QLabel("ChatBot Response: ", self.main_window)
        self.label5.setStyleSheet('color: black; font-weight: bold; font-size: 11px;')
        self.label5.setGeometry(600, 60, 150, 30)

        # label to display chatbot response:
        self.label6 = QLabel("", self.main_window)
        self.label6.setStyleSheet('color: black; font-size: 14px; border: 2px solid black; padding: 5px;')
        self.label6.setGeometry(600, 100, 550, 450)
        self.label6.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # aligning the text to top left of the label
        self.label6.setWordWrap(True)  # wrapping the text to start the next line when the first line is ended

        # program will stop when user inputs any of these words:
        self.exit_conditions = ("bye", "okay bye", "okay goodbye", "take care, bye", "ok take care", "ok bye",
                           "goodbye", "exit", "takecare", "Ali")

    def update_label3(self): # Function to display the username, when it's entered, and display a welcome message
        username = self.entry.text()
        self.label4.setText(f"{username}: ") # displaying the username on label4
        self.label1.clear()
        self.label3.setText(f"ReceptionistBot: Hello {username}! I'm a ReceptionistBot. How can I help you today?")
        self.chat.text_to_speech(f"Hello! I'm a ReceptionistBot. How can I help you today?")
        self.label3.setStyleSheet('color: black; font-weight: bold; font-size: 11px;')
        self.entry.clear()

# This function will be called when user inputs any question/query in the user_input entry:
    def save_user_input(self):
        query = self.user_input.text() # saving the user input in a variable named "query"
        print(f"User: {query}")
        self.user_input.clear()
        self.label6.clear()
        if query.lower() in self.exit_conditions: # if user inputs any word from the exit_conditions, then quit the application
            self.label6.setText("Goodbye!")
            self.chat.text_to_speech("Take-care, Goodbye")
            self.application.quit()
        # a list of words, which when entered then the chatterbot receptionist Bot will response, otherwise chatgpt will reply
        key_words = ["help", "information", "ATM", "card", "number", "need", "details", "balance",
                     "introduce", "receptionist", "introduction"]
        # this variable will be true, if user input matches with any of the words present in the key_words list
        matched_word = any(word in query.lower() for word in key_words)

        self.all_card_numbers_list = self.db.read_card_number_from_file() # Adding the all_card_numbers_list attribute

        # call the function to see if the user_input is matching with any card number from our database
        has_number, ATM_CardNumber = self.db.contains_number(query, self.all_card_numbers_list)
        if has_number: # if number matched then get the data for that card from database
            data_row = self.db.get_data_from_file(ATM_CardNumber)
            # empty lists to contain the data if the card number entered by user matches with our database:
            headers = []
            account_info = []
            if data_row:
                for header, value in data_row.items():  # iterating through the key:value pair in the dictionary
                    headers.append(header)  # append the headers to a new list
                    account_info.append(value)  # append the account information to a new list
                print(tabulate([account_info], headers=headers))  # print in tabular form
                formatted_info = "\n".join([f"{header}: {value}" for header, value in data_row.items()])
                self.label6.setText(f"Sure sir, Here's the data for {ATM_CardNumber}:\n\n{formatted_info}")

                print(f"ReceptionistBot: Sure sir, Here's the data for {ATM_CardNumber}:")
                self.chat.text_to_speech("Sure sir, I've displayed the data for the card on the screen")
        # if number entered by user didn't match with our database record:
        else:
            # check if the first 4 digits of the user input are digits:
            if query[0:3].isdigit():
                self.label6.setText(f"Sorry, I couldn't find data for {ATM_CardNumber}, please try again!")
                self.chat.text_to_speech("Sorry, I couldn't find data for this card, please try again!")
            # check if user input contains any word from the key_words list, chatterbot will reply in this case from trained data
            elif matched_word:
                response = self.chat.chatbot.get_response(query)
                self.label6.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                self.label6.setWordWrap(True)
                self.label6.setText(str(response))

                print(f"ReceptionistBot: {response}")
                self.chat.text_to_speech(response)

            # otherwise, chatgpt will reply to the user input:
            else:
                response = self.chat.get_chatgpt_response(query)
                self.label6.setText(response)

                print(f"ChatGPT - ReceptionistBot: {response}")
                self.chat.text_to_speech(response)

    def run(self):
        self.main_window.show()  # display the main GUI window
        self.application.exec_()  # initiating the event loop, allowing the GUI to respond to the user inputs as per code's logic

# This class deals with chatbot, chatgpt, and speech functions.
class ChatFunctions:
    def __init__(self):
        openai.api_key = ''  # Use OpenAI API key here to use chatGPT
        self.chatbot = ChatBot(
            'ReceptionistBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',  # bot's data will be stored in a SQL database
            # chatbot will reply with the "best match answer" from the existing conversation corpus
            logic_adapter='chatterbot.logic.BestMatch',
            database_uri='sqlite:///RecepBot_database.sqlite3'  # URI where bot's data will be stored
        )
        self.trainer = ListTrainer(self.chatbot)
        self.init_chatbot()

    def init_chatbot(self):
        # Bot training part:
        # Information related to ATM Card: "First line is the input by the user and Second line is the response of the bot"
        self.trainer.train([
            "I need help",
            "Sure, I am available!",
            "Hello, can you help me?",
            "Of course, that's what I'm meant to do, please provide me with the details",
            "I want to check my account details",
            "Understood, to proceed, please provide me with your ATM card number",
            "I want to check my account information",
            "Understood, to proceed, please provide me with your ATM card number",
            "I want to check my account balance",
            "Understood, to proceed, please provide me with your ATM card number",
            "ATM",
            "If you want to check your account details, please provide me with your ATM Card number",
            "Card",
            "If you want to check your account details, please provide me with your ATM Card number",
            "Number",
            "If you want to check your account details, please provide me with your ATM Card number"
        ])
        # Intro of the bot:
        self.trainer.train([
            "Tell me about yourself",
            "I am a Receptionist Bot, ready to help customers",
            "Introduce yourself please",
            "I am a Receptionist Bot, I provide assistance to customers",
            "Can you introduce yourself?",
            "Of course, I am a Receptionist Bot",
            "Give me your introduction?",
            "I am a Receptionist Bot :)",
            "who are you?",
            "I am a Receptionist Bot",
            "Are you really a bot?",
            "Yes, 100%",
            "Are you a receptionist bot?",
            "Yes, 100%"
        ])

    # Function to get response from chatgpt:
    def get_chatgpt_response(self, input_text):
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": input_text}])
        return response.choices[0].message.content # get the first response generated by chatgpt (i.e., choice = 0)

    def text_to_speech(self, text): # function to convert text to speech:
        tts = gTTS(text=str(text))

        speech_stream = io.BytesIO()  # An in memory stream is created to store the speech in it
        tts.write_to_fp(speech_stream)  # writing the speech to the memory stream created above
        speech_stream.seek(0)  # Setting the stream position to 0, to read the audio data from the beginning

        # Using mixer module to play the audio:
        pygame.mixer.init()
        pygame.mixer.music.load(speech_stream)
        pygame.mixer.music.play()

        # loop to check after every 10 seconds if the audio is still playing:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Check every 10 milliseconds

        pygame.mixer.music.stop()


class DatabaseFunctions: # Class for the Database and it's functions:
    def __init__(self):
        self.conn = sqlite3.connect('Receptionistbot_database.db')
        self.cursor = self.conn.cursor()

    def read_card_number_from_file(self): # Function to read all card numbers from the dataset file:
        self.cursor.execute('SELECT card_number FROM Card_data') # execute the query
        reader = self.cursor.fetchall() # contains a list of tuples. Each tuple contains the card number

        # for loop to iterate through each tuple in the list and row[0] to extract the first and only element of the tuple
        return [row[0] for row in reader]  # A list containing all the card numbers.

    def contains_number(self, input_text, card_numbers): # Function to check if the input contains a valid card number:
        for number in card_numbers:
            if number in input_text:
                return True, number
        return False, input_text

    def get_data_from_file(self, number): # Function to get data from the dataset file:
        self.cursor.execute('SELECT * FROM Card_data')
        reader = self.cursor.fetchall()
        headers = ["Total Balance", "Transactions", "Card Holder Name", "Last Activity Date", "Last Transaction"]
        for row in reader:
            if row[0] == number:  # check if first row is matching with the user input, if matching extract all the data
                return dict(zip(headers[0:], row[1:]))
        return "I'm sorry, I don't have details for that card."


class ReceptionistBot: # Main ReceptionistBot class
    def __init__(self):   # Initialize instances of all classes
        self.chat = ChatFunctions()
        self.db = DatabaseFunctions()
        self.gui = ReceptionistBotGUI(self.chat, self.db)

    def run_bot(self):   # function to run the Bot
        self.gui.run()   # Bot runs by executing the GUI


# main:
if __name__ == "__main__":
    bot = ReceptionistBot() # create an instance of the ReceptionistBot
    bot.run_bot() # run the ReceptionistBot