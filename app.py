from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app=Flask(__name__)

app.config['SECRET_KEY']='Codingforlife'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

answers = []

@app.route('/answer', methods=['POST'])
def store_answer():
  respond = request.form['shopped-before']
  answers.append(respond)

  if (len(answers) == len(survey.questions)):
    return redirect('/complete')
  else:
    return redirect(f'/question/{len(answers)}')

  

@app.route('/')
def go_home():

  title = survey.title
  instructions = survey.instructions

  return render_template('home.html', title = title, instructions = instructions)


@app.route('/question/<int:number>')
def show_question(number):
  
  question = survey.questions[number]

  if (len(answers) != number):
    flash(f'Invalid question {number}') 
    return redirect('/question/0')  
  else:
    return render_template('question.html', question=question)

@app.route('/complete')
def completion():
  return render_template('complete.html')