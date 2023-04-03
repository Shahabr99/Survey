from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


RESPONSES_KEY = "responses"

app=Flask(__name__)

app.config['SECRET_KEY']='Its-a-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)


@app.route('/')
def go_homepage():
    title = survey.title
    instructions = survey.instructions

    return render_template('home.html', title=title, instructions=instructions)

@app.route('/start', methods=['POST'])
def start_survey():
    
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route('/respond', methods=['POST'])
def store_answer():
    answer = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    else:
        return redirect(f"/questions/{len(responses)}")



@app.route('/questions/<int:number>')
def ask_question(number):

    responses = session.get(RESPONSES_KEY)

    if responses is None:
        return redirect("/")

    if(len(responses) == len(survey.questions)):
        return redirect('/complete')

    if len(responses) != number:
        flash(f"Invalid question")
        return redirect(f"/question/{len(responses)}")

    question = survey.questions[number]
    return render_template("question.html", q_number= number, question=question)

@app.route('/complete')
def survey_completion():
    return render_template('complete.html')