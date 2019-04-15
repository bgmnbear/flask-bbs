from flask_restful import Resource, abort, reqparse

from models.answer import Answer


def abort_if_answer_doesnt_exist(a):
    if a is None:
        abort(404, message="Answer doesn't exist")


parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)
parser.add_argument('user_id', type=str)
parser.add_argument('question_id', type=str)


class AnswerApi(Resource):
    def get(self, question_id):
        a = Answer.find_by(id=int(question_id))
        abort_if_answer_doesnt_exist(a)
        return a.json()

    def delete(self, question_id):
        Answer.delete(id=int(question_id))
        return '', 204


class AnswerListApi(Resource):
    def get(self):
        pass

    def post(self):
        args = parser.parse_args()
        d = {'title': args['title'], 'content': args['content'], 'user_id': args['user_id'],
             'question_id': args['question_id']}
        a = Answer.new(d)
        a.save()
        return a.json(), 201
