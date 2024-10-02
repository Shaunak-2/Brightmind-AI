import time
import streamlit as st
from groq import Groq, RateLimitError
import os

# Initialize the Groq client
client = Groq(api_key="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")

def save_qa_to_file(chapter, verse, qa_text):
    # Create a folder named 'QnA' if it doesn't exist
    folder_path = 'QnA'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Generate file name
    file_name = f'QnA_{chapter}_{verse}.txt'
    file_path = os.path.join(folder_path, file_name)
    
    # Save Q&A text to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(qa_text)



# Define the system prompt
system_prompt = """ You will be a given a text input. Analyze the input and help the user by - Generating Multiple Types of Questions and Answers covering essential concepts form the give input.

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

# Streamlit UI
st.title("Q&A Generator Using LLAMA-3")


# Get the list of chapters (subfolders)

# Function to request completion with retry on rate limit error
def request_completion(input_text):
    while True:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"{system_prompt}"},
                    {"role": "user", "content": f"{input_text}"}
                ],
                model="llama3-70b-8192",
                temperature=0.1
            )
            print("done")
            return chat_completion.choices[0].message.content
        except RateLimitError as e:
            error_message = e.args[0]
            if 'rate limit reached' in error_message:
                # Extract retry time from the error message
                retry_after = float(error_message.split("Please try again in")[1].split("s.")[0])
                st.warning(f"Rate limit reached. Retrying in {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                raise e

# Iterate through each chapter
input_text = st.text_area("Input")

if input_text:
            with st.spinner(f"Generating..."):
                output = request_completion(input_text)
                # Display output
                st.markdown(output)