from app import(
    app,
    db
)
from flask import(
    render_template,
    request,
    jsonify,
    make_response,
    redirect,
    url_for
)

from app.models.sistema import(
    Disciplina,
    Assunto
)

from app.core.database import SessionLocal


#SITE

@app.route('/')
@app.route('/index')
@app.route('/panel/home')
@app.route('/panel/index')
def home_page():
    return render_template('panel/educasoft/home.html')
    return render_template('base/base.html')
    # return render_template('panel/home.html')


@app.route('/panel/materia/listar')
def listar_materias():
    return render_template('panel/educasoft/materia-listar.html')


@app.route('/panel/materia/create')
def materia_create():
    return render_template('panel/educasoft/materia-create.html')





@app.route('/panel/materia/<int:id>/view')
@app.route('/panel/materia/<int:id>/edit')
def materia_edit(id):
    data_materia = Disciplina.list_by_id(session=SessionLocal(), id=id)
    if not data_materia:
        return page_not_found(404)
    return render_template('panel/educasoft/materia-editar.html', id=id, data=data_materia)





#ASSUNTO !


@app.route('/panel/materia/<int:id>/assunto/create')
def materia_assunto_create(id):
    return render_template('panel/educasoft/materia-assunto-create.html', id=id)



@app.route('/panel/materia/assunto/<int:id_assunto>/view')
def materia_assunto_view(id_assunto):
    return render_template('panel/educasoft/materia-assunto-ver.html', id=id_assunto)




@app.route('/panel/materia/assunto/<int:id_assunto>/edit')
def materia_assunto_edit(id_assunto):
    data_assunto = Assunto.list_by_id(session=SessionLocal(), id=id_assunto)
    if not data_assunto:
        return page_not_found(404)
    return render_template('panel/educasoft/materia-assunto-editar.html', id=id_assunto, data=data_assunto)




#QUESTAO


@app.route('/panel/materia/assunto/<int:id>/question/create')
def materia_assunto_question_create(id):
    return render_template('panel/educasoft/materia-assunto-questao-create.html', id=id)




@app.route('/panel/materia/assunto/questao/<int:id_questao>/edit')
def materia_assunto_question_edit(id_questao):
    return render_template('panel/educasoft/materia-assunto-questao-editar.html', id=id_questao)




#ERROS
@app.errorhandler(404)
def page_not_found(error):
    return render_template("base/base-404.html"), 404



# @app.route('/quiz')
# def quiz_page():
#     return render_template('panel/quiz.html')



# @app.route('/quiz/<int:id>')
# def quiz_responder(id):
#     return render_template('panel/quiz-responder.html', id=id)


# @app.route('/view/materia/index')
# @app.route('/view/materia/list')
# def materia_list():
#     #return render_template('panel/materia.html')
#     return render_template('panel/materia-modulos.html')


# @app.route('/view/materia/create')
# def materia_create():
#     return render_template('panel/materia-create.html')


# @app.route('/view/materia/<int:id>/view')
# @app.route('/view/materia/<int:id>/edit')
# def materia_edit(id):
#     return render_template('panel/materia-edit.html', id=id)


# @app.route('/view/materia/<int:id>/create-question')
# def materia_question_create(id):
#     return render_template('panel/materia-question-create.html', id=id)


# @app.route('/register')
# def register():
#     return render_template('base/base_register.html')


# @app.route('/login')
# def login():
#     return render_template('base/base_login.html')