from flask_restful import Resource, abort, reqparse
from models.question import Question


def abort_if_question_doesnt_exist(q):
    if q is None:
        abort(404, message="Question doesn't exist")


post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str)
post_parser.add_argument('content', type=str)
post_parser.add_argument('user_id', type=str)


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
        args = post_parser.parse_args()
        d = {'title': args.title, 'content': args.content, 'user_id': args.user_id}
        q = Question.new(d)
        q.save()
        return q.json(), 201
