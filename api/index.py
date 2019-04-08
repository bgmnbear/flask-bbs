from flask import Flask
from flask_restful import Resource, Api, abort

from models.question import Question
from utils import log

app = Flask(__name__)
api = Api(app)


def abort_if_question_doesnt_exist(q):
    if q is None:
        abort(404, message="Question doesn't exist")


class QuestionApi(Resource):
    def get(self, question_id):
        q = Question.find_by(id=int(question_id))
        abort_if_question_doesnt_exist(q)
        return q.json()

    def delete(self, question_id):
        q = Question.delete(id=int(question_id))
        return '', 204


class QuestionListApi(Resource):
    def get(self):
        pass

    def post(self):
        q = Question.new(dict(title='123123', content='123123', user_id='33'))
        q.save()
        log('post', q)


class Answer(Resource):
    pass


api.add_resource(QuestionApi, '/question/<question_id>')
api.add_resource(QuestionListApi, '/question')

if __name__ == '__main__':
    app.run(debug=True)
