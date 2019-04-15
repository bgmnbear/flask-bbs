from flask import Flask
from flask_restful import Api

from api.resources.answer import AnswerApi, AnswerListApi
from api.resources.question import QuestionApi, QuestionListApi

app = Flask(__name__)
api = Api(app)

api.add_resource(QuestionApi, '/question/<question_id>')
api.add_resource(QuestionListApi, '/question')
api.add_resource(AnswerApi, '/answer/<answer_id>')
api.add_resource(AnswerListApi, '/answer')

if __name__ == '__main__':
    app.run(debug=True)
