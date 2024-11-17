from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import re
import time
import os
import json
import google.generativeai as genai
from IPython.display import Markdown
from gtts import gTTS
import speech_recognition as sr
import pygame
import time
import cv2
from dotenv import load_dotenv
from groq import Groq, RateLimitError 

user_responses = []


conversation_history = []


load_dotenv()

groq_api_key = os.getenv("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")
client_api = Groq(api_key="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")

# Set your API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyBAtGOtAIGni2RBnhIBTrn71HJPU5vb7TU"

# Configure generative AI
genai.configure(api_key="AIzaSyBAtGOtAIGni2RBnhIBTrn71HJPU5vb7TU")

app = Flask(__name__)

app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['quiz_app'] 
users_collection = db['users'] 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    college = request.form['college']
    
    if users_collection.find_one({'email': email}):
        return "Email already exists!"
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    users_collection.insert_one({
        'username': username,
        'email': email,
        'password': hashed_password,
        'college': college
    })
    return redirect(url_for('home'))

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    
    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({'success': False, 'message': 'Incorrect email ID!'})
    
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'success': False, 'message': 'Incorrect password!'})
    
    session['user'] = user['username']
    return jsonify({'success': True})


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    username = request.form['username']
    email = request.form['email']
    new_password = request.form['new_password']
    
    user = users_collection.find_one({'username': username, 'email': email})
    if not user:
        return jsonify({'success': False, 'message': 'User not found. Please check the details!'})
    
    hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    
    users_collection.update_one(
        {'username': username, 'email': email},
        {'$set': {'password': hashed_new_password}}
    )
    return jsonify({'success': True, 'message': 'Password updated successfully!'})

@app.route('/interface')
def interface():
    if 'user' in session:
        return render_template('interface.html', username=session['user'])
    return redirect(url_for('home'))

@app.route('/gamification')
def gamification():
    return render_template('gamification.html')

@app.route('/memoryGame')
def memoryGame():
    return render_template('memoryGame.html')

@app.route('/knowledgeLadder')
def knowledgeLadder():
    return render_template('knowledgeLadder.html')

@app.route('/quizOptions')
def quiz_options():
    return render_template('quizOptions.html')

@app.route('/Quize')
def Quize():
    return render_template('Quize.html')

@app.route('/chatbot', methods=['GET'])
def chatbot_page():
    return render_template('chatbot.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    if not request.is_json:
        return jsonify(response="Invalid Content-Type. Expected application/json."), 400

    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify(response="No question provided."), 400
    
    response = chatbot_function(question)
    return jsonify(response=response)


@app.route('/choice')
def choice():
    return render_template('choice.html')

@app.route('/interView')
def interView():
    return render_template('interview.html')


@app.route('/One2One')
def One2One():
    return render_template('One2One.html')


@app.route('/generate_interview', methods=['POST'])
def generate_interview():
    query = request.form['query']
    num_questions = int(request.form['num_questions'])

        
    query = f'{query} can you generate  {num_questions} questions on the above paragraph'
    # Choose a model (replace 'gemini-pro' with your desired model)
    model_name = 'gemini-pro'
    model = genai.GenerativeModel(model_name)

    # Generate content
    response = model.generate_content(query)

    # Extract and display the generated response
    generated_text = response.text
    print(f"Generated Response:\n{generated_text}")

    str_data = f'{generated_text}'

    # Split the string into individual questions using regular expressions
    questions = re.split(r'\d+\.\s*', str_data)
    # Remove empty strings from the list
    questions = [q.strip() for q in questions if q.strip()]

    # Create an array to store each question substring
    questionArray = [question for question in questions]

    # Display the extracted questions
    for i, question in enumerate(questionArray):
        print(f"Question {i + 1}: {question}")



    def text_to_speech(questionArray , language='en'):
        for i , text in enumerate(questionArray):
            saveAs = f'output{i}.mp3'
            tts = gTTS(text = text , lang = language , slow=False)
            tts.save(saveAs)
            print("saved")




    # def speech_to_text_from_microphone():
    #     global user_responses  # Access the global array

    #     recognizer = sr.Recognizer()

    #     with sr.Microphone() as source:
    #         print("Say answer:")
    #         recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
    #         audio_data = recognizer.listen(source)

    #         try:
    #             text = recognizer.recognize_google(audio_data)
    #             print("Your answer:", text)

    #             # Store the recognized text in the global array
    #             user_responses.append(text)
    #         except sr.UnknownValueError:
    #             print("Could not understand audio")
    #         except sr.RequestError as e:
    #             print(f"Could not request results from Google Speech Recognition service; {e}")




    # def play_audio(file_path):
    #     pygame.init()
    #     pygame.mixer.init()

    #     try:
    #         pygame.mixer.music.load(file_path)
    #         pygame.mixer.music.play()

    #         while pygame.mixer.music.get_busy():
    #             # Wait for the audio to finish playing
    #             pygame.time.Clock().tick(10)

    #     except Exception as e:
    #         print(f"Error: {e}")
    #     finally:
    #         pygame.mixer.quit()

    text_to_speech(questionArray)

    return render_template('One2One.html')

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    query = request.form['query']
    num_questions = int(request.form['num_questions'])

    # Generate questions
    query = f'{query} Can you generate {num_questions} questions on the above paragraph? Each question should be in MCQ format, like: **Question ----------- (a) option a (b) option b (c) option c (d) option d (Correct Answer: option)'
    model_name = 'gemini-pro'
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(query)
    generated_text = response.text

    # Extract questions and options
    lines = generated_text.strip().split('\n')
    questions = []
    options_a = []
    options_b = []
    options_c = []
    options_d = []
    correct_answers = []  # To store correct answers

    current_question = ""
    current_a = ""
    current_b = ""
    current_c = ""
    current_d = ""
    current_correct_answer = ""  # To capture correct answers

    for line in lines:
        line = line.strip()
        
        # Detect a new question start
        if line.startswith("**Question"):
            # If a question was already being processed, save it before starting a new one
            if current_question:
                questions.append(current_question.strip())
                options_a.append(current_a.strip())
                options_b.append(current_b.strip())
                options_c.append(current_c.strip())
                options_d.append(current_d.strip())
                correct_answers.append(current_correct_answer)  # Save correct answer for the current question

            # Reset variables for the new question
            current_question = line.replace("**Question", "").strip()
            current_a = ""
            current_b = ""
            current_c = ""
            current_d = ""
            current_correct_answer = ""
        
        elif line.startswith("(a)"):
            current_a = line.replace("(a)", "").strip()
        elif line.startswith("(b)"):
            current_b = line.replace("(b)", "").strip()
        elif line.startswith("(c)"):
            current_c = line.replace("(c)", "").strip()
        elif line.startswith("(d)"):
            current_d = line.replace("(d)", "").strip()
        elif line.startswith("(Correct Answer:"):
            # Capture the correct answer based on its label (a, b, c, or d)
            current_correct_answer = line.replace("(Correct Answer:", "").replace(")", "").strip()
            if current_correct_answer not in ['a', 'b', 'c', 'd']:
                raise ValueError(f"Unexpected answer format: {current_correct_answer}")
        else:
            if current_question:
                current_question += " " + line.strip()
            else:
                current_question = line.strip()

    # Save the last question if there is any
    if current_question:
        questions.append(current_question.strip())
        options_a.append(current_a.strip())
        options_b.append(current_b.strip())
        options_c.append(current_c.strip())
        options_d.append(current_d.strip())
        correct_answers.append(current_correct_answer)  # Add final correct answer

    # Convert lists to JSON for rendering
    questions_json = json.dumps(questions)
    options_a_json = json.dumps(options_a)
    options_b_json = json.dumps(options_b)
    options_c_json = json.dumps(options_c)
    options_d_json = json.dumps(options_d)
    correct_answers_json = json.dumps(correct_answers)

    return render_template('CreateQuiz.html', questions=questions_json, options_a=options_a_json, options_b=options_b_json, options_c=options_c_json, options_d=options_d_json, correct_answers=correct_answers_json)

@app.route('/startInterview')
def startInterview():
    for i in range(0 , 3):
        audio_file_path = f'output{i}.mp3'
        play_videos(i)
        play_audio(audio_file_path)
        speech_to_text_from_microphone()
    

def play_videos(start_index=0):
    while True:
        file_name = f"result_voice ({start_index}).mp4"  # Assuming video files are in .mp4 format
        if not os.path.exists(file_name):
            print(f"No more video files found starting from index {start_index}.")
            break

        cap = cv2.VideoCapture(file_name)
        
        if not cap.isOpened():
            print(f"Error opening video file: {file_name}")
            break

        print(f"Playing video file: {file_name}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"Finished playing video file: {file_name}")
                break
            cv2.imshow('Video Playback', frame)
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                print("Playback interrupted by user.")
                cap.release()
                cv2.destroyAllWindows()
                return
        
        cap.release()
        start_index += 1

    cv2.destroyAllWindows()


def play_audio(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            # Wait for the audio to finish playing
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.mixer.quit()

def speech_to_text_from_microphone():
    global user_responses  # Access the global array

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio_data = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio_data)
            print("You said:", text)

            # Store the recognized text in the global array
            user_responses.append(text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def text_to_speech(questionArray , language='en'):
    for i , text in enumerate(questionArray):
        saveAs = f'output{i}.mp3'
        tts = gTTS(text = text , lang = language , slow=False)
        tts.save(saveAs)
        print("saved")


def save_feedback(feedback):
    with open("feedback.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([feedback])

def chatbot_function(question):
    if "feedback" in question.lower():
        save_feedback(question)
        return "Thank you for your feedback! We will review it soon."

    conversation_history.append({"role": "user", "content": question})

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant on a platform designed for graduated or ungraduated students and job seekers. Which is basically has different modules like text based quiz or topic based quiz or interview where ai avataar will take an interview of user."
                "You help users by providing answers to general knowledge questions, guiding them through quizzes, puzzles or today's technology questions"
                "and collecting feedback on the platform's features. Answer questions clearly and provide suggestions "
                "based on the user's needs."
            )
        }
    ] + conversation_history

    try:
        response = client_api.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=150,
            top_p=1,
            stop=None,
            stream=False
        )
        generated_text = response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

    conversation_history.append({"role": "assistant", "content": generated_text})

    return generated_text


def get_system_prompt():
    return """ You will be a given a text input. Analyze the input and help the user by - Generating Multiple Types of Questions and Answers covering essential concepts form the give input.

    1. Read the Text:
       - Carefully read the provided text, noting key themes, concepts, significant terms, or phrases. Understand the context and the message conveyed by the text.

    2. Identify Key Concepts:
       - Highlight the main ideas presented in the text, such as philosophical concepts, instructions, historical context, or other significant points central to understanding the passage.

    3. Generate Questions and Answers:
       - Based on the key concepts identified, create the following types of questions. Ensure all questions are closely tied to the text and encourage exploration, comprehension, and application of the concepts.

       a. Open-ended Questions (3 questions):
       - Formulate questions that encourage deep thinking and exploration of the text. These questions should prompt the reader to consider the broader implications and meanings of the concepts.

       b. Fill-in-the-Blank Questions (3 questions):
       - Create questions where the reader needs to fill in the blanks with key terms or phrases from the text. These questions should test the reader’s recall and understanding of specific details.

       c. True or False Questions (3 questions):
       - Generate statements based on the text that the reader must evaluate as true or false. These should test the reader’s comprehension of the text’s key points.

       d. Multiple Choice Questions (3 questions):
       - Create multiple choice questions with four options, one of which is correct. These should assess the reader’s understanding of key concepts and details from the text.

    4. Provide Answers:
       - Answer each question using information from the text. Ensure that the answers are clear, concise, and informative, directly reflecting the content of the passage.
    """

# Function to request completion with retry on rate limit error
def request_completion(input_text):
    while True:
        try:
            system_prompt = get_system_prompt()
            chat_completion = client_api.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"{system_prompt}"},
                    {"role": "user", "content": f"{input_text}"}
                ],
                model="llama3-70b-8192",
                temperature=0.1
            )
            return chat_completion.choices[0].message.content
        except RateLimitError as e:
            error_message = e.args[0]
            if 'rate limit reached' in error_message:
                retry_after = float(error_message.split("Please try again in")[1].split("s.")[0])
                time.sleep(retry_after)
            else:
                raise e

@app.route('/quizByTopic')
def quizByTopic():
    return render_template('quizByTopic.html')

@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.json['input_text']
    output = request_completion(input_text)
    return jsonify({'output': output})



if __name__ == '__main__':
    app.run(debug=True)
