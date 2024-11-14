let level = 1;
let currentQuestionIndex = 0;
let questions = [
        { 
            "question": "What programming language is commonly used for data science and machine learning?", 
            "answers": ["Java", "Python", "C++", "Ruby"], 
            "correct": "Python", 
            "difficulty": 1 
        },
        { 
            "question": "In blockchain technology, what is a 'smart contract'?", 
            "answers": ["A physical contract on a blockchain", "Self-executing code with contract terms", "An agreement verified by lawyers", "An automatic cryptocurrency transaction"], 
            "correct": "Self-executing code with contract terms", 
            "difficulty": 2 
        },
        { 
            "question": "If a train travels 60 km/hr and covers a distance of 300 km, how much time will it take?", 
            "answers": ["4 hours", "5 hours", "6 hours", "7 hours"], 
            "correct": "5 hours", 
            "difficulty": 1 
        },
        { 
            "question": "In machine learning, which term refers to the difference between the expected prediction of the model and the actual outcome?", 
            "answers": ["Variance", "Overfitting", "Bias", "Regularization"], 
            "correct": "Bias", 
            "difficulty": 3 
        },
        { 
            "question": "What is the probability of getting a sum of 7 when rolling two dice?", 
            "answers": ["1/6", "1/12", "1/8", "1/4"], 
            "correct": "1/6", 
            "difficulty": 2 
        },
        { 
            "question": "Which organization is responsible for defining web standards?", 
            "answers": ["NASA", "Mozilla", "W3C", "IEEE"], 
            "correct": "W3C", 
            "difficulty": 1 
        }    
];

function startGame() {
    level = 1;
    currentQuestionIndex = 0;
    document.getElementById('level-text').innerText = "Level: " + level;
    document.getElementById('start-btn').style.display = "none";
    showQuestion();
}

function showQuestion() {
    // Display question and answers
    const questionElement = document.getElementById('question-text');
    const answersElement = document.getElementById('answers');
    answersElement.innerHTML = ''; // Clear previous answers

    const question = questions[currentQuestionIndex];
    questionElement.innerText = question.question;

    question.answers.forEach(answer => {
        const button = document.createElement('button');
        button.innerText = answer;
        button.addEventListener('click', () => checkAnswer(answer));
        answersElement.appendChild(button);
    });
}

function checkAnswer(selectedAnswer) {
    const question = questions[currentQuestionIndex];
    const buttons = document.querySelectorAll('#answers button');

    buttons.forEach(button => {
        if (button.innerText === question.correct) {
            button.classList.add('correct');
        } else if (button.innerText === selectedAnswer) {
            button.classList.add('wrong');
        }
    });

    if (selectedAnswer === question.correct) {
        level++;
        document.getElementById('level-text').innerText = "Level: " + level;

        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            setTimeout(showQuestion, 1000); // Move to the next question
        } else {
            document.getElementById('question-text').innerText = "Congratulations! You've completed the ladder!";
            document.getElementById('start-btn').style.display = "block";
            document.getElementById('start-btn').innerText = "Play Again";
        }
    } else {
        document.getElementById('question-text').innerText = "Game Over! You reached Level " + level;
        document.getElementById('start-btn').style.display = "block";
        document.getElementById('start-btn').innerText = "Try Again";
    }
}
