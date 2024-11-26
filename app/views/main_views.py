from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello():
    return 'Hello'

@bp.route('/')
def index():
    # question_list = Question.query.order_by(Question.create_date.desc())
    # return render_templete('question/question_list.html
    return 'index'