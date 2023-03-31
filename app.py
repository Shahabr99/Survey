from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app=Flask(__name__)

app.config['SECRET_KEY']='Codingforlife'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

requests = []

@app.route('/')
def go_home():

  title = satisfaction_survey.title
  instructions = satisfaction_survey.instructions

  return render_template('home.html', title = title, instructions = instructions)


@app.route('/question/<int:number>')
def show_question(number):
  
  question = satisfaction_survey.questions[number]
  

  return render_template('question.html', question=question)