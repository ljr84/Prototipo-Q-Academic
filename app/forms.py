
from app import(
    app,
    db
)
from flask import(
    render_template,
    request,
    jsonify,
    make_response,
    Response
)
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal


from app.models.sistema import(
    Disciplina,
    Assunto,
    Pergunta
)





@app.route('/api/materia/list', methods=["GET"])
def api_materia_list():
    temp = Disciplina.list_all(session=SessionLocal())
    if temp:
        data = []
        for item in temp:
            data.append({
                'id': item.id,
                'name': item.name,
                'icon': item.icon,
                'description': item.description,
                'total': len(item.assuntos),
                'date_created': item.date_created
            })
        return jsonify(error=False, data=data)
    else:
        return jsonify(error=True, message='no return')





@app.route('/api/materia/create', methods=["POST"])
def api_materia_create():
    if request.method == "POST":
        name = request.form['name']
        icon = request.form['icon']
        description = request.form["description"]
        temp = Disciplina.create(session=SessionLocal(), data={
            'name': name,
            'icon': icon,
            "description": description
        })
        if temp:
            data_out = {
                'id': temp.id,
                'name': temp.name,
                'icon': temp.icon,
                'description': temp.description,
                'date_created': temp.date_created
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou criar materia"}), 400
    return jsonify(error=True)



@app.route('/api/materia/<int:id_disciplina>')
def api_materia_view(id_disciplina):
    temp = Disciplina.list_by_id_moar(session=SessionLocal(), id=id_disciplina)
    if temp:
        return jsonify(error=False, data=temp)
    return jsonify(error=True, message='not found'), 404





@app.route('/api/materia/<int:id_disciplina>/edit', methods=["POST"])
def api_materia_edit(id_disciplina):
    if request.method == "POST":
        name = request.form.get("name", None)
        description = request.form.get("description", None)
        if name or description:
            ss = SessionLocal()
            temp = Disciplina.list_by_id(session=ss, id=id_disciplina)
            if temp:
                if name:
                    temp.name = name
                if description:
                    temp.description = description
                ss.commit()
                return jsonify(error=False, data=temp)
            else:
                return jsonify(error=True, message='not found'), 404
        else:
            return jsonify(error=True, message='not found'), 404
    else:
        return jsonify(error=True, message='not found'), 404






@app.route('/api/materia/<int:id_disciplina>/delete', methods=["DELETE"])
def api_materia_delete(id_disciplina):
    session = SessionLocal()
    temp = Disciplina.list_by_id(session=session, id=id_disciplina)
    if temp:
        if len(temp.assuntos)>0:
            return jsonify(error=True, message="Voce precisa deletar as questoes do assunto antess]"), 400
        else:
            try:
                session.delete(temp)
                session.commit()
                return jsonify(error=False), 204
            except Exception as err:
                return jsonify(error=True, message='exception', detail=str(err)), 400
    else:
        return jsonify(error=True, message='not found'), 404
    
            
        













@app.route('/api/materia/<int:disciplina_id>/assunto/create', methods=["POST"])
def api_materia_assunto_create(disciplina_id):
    if request.method == "POST":
        description = request.form["description"]
        temp = Assunto.create(session=SessionLocal(), data={
            'description': description,
            'disciplina_id': disciplina_id,
        })
        if temp:
            data_out = {
                'id': temp.id,
                'disciplina_id': temp.disciplina_id,
                'description': temp.description,
                'date_created': temp.date_created,
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou criar assunto"}), 400
    return jsonify(error=True)






@app.route('/api/materia/assunto/<int:assunto_id>/question/create', methods=["POST"])
def api_materia_assunto_question_create(assunto_id):
    if request.method == "POST":
        question = request.form["question"]
        correct = request.form["correct"]
        if not correct.lower() in ('1', '0'):
            return jsonify(error=True, message="\"correct\" value invalid"), 400
        correct = True if correct == '1' else False
        temp = Pergunta.create(session=SessionLocal(), data={
            'question': question,
            'correct': correct,
            'assunto_id': assunto_id,
        })
        if temp:
            data_out = {
                'id': temp.id,
                'assunto_id': temp.assunto_id,
                'question': temp.question,
                'correct': temp.correct,
                'date_created': temp.date_created
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou criar questao"}), 400
    return jsonify(error=True)





@app.route('/api/materia/assunto/<int:id_assunto>')
def api_materia_assunto_view(id_assunto):
    temp = Assunto.list_by_id_moar(session=SessionLocal(), id=id_assunto)
    if temp:
        return jsonify(error=False, data=temp)
    return jsonify(error=True, message='not found'), 404






@app.route('/api/materia/assunto/<int:id_assunto>/update', methods=["POST"])
def api_materia_assunto_update(id_assunto):
    session = SessionLocal()
    description = request.form.get('description', False)
    if not description:
        return jsonify(error=True, message='missing `description`'), 400
    temp = Assunto.list_by_id(session=session, id=id_assunto)
    if not temp:
        return jsonify(error=True, message='not found'), 404
    try:
        temp.description = description
        session.commit()
        return jsonify(error=False), 200
    except Exception as err:
        return jsonify(error=True, message='exception', detail=str(err)), 400



@app.route('/api/materia/assunto/<int:id_assunto>/delete', methods=["DELETE"])
def api_materia_assunto_delete(id_assunto):
    session = SessionLocal()
    temp = Assunto.list_by_id(session=session, id=id_assunto)
    if temp:
        if len(temp.perguntas)>0:
            return jsonify(error=True, message="Voce precisa deletar as questoes do assunto antess]"), 400
        else:
            try:
                session.delete(temp)
                session.commit()
                return jsonify(error=False), 204
            except Exception as err:
                return jsonify(error=True, message='exception', detail=str(err)), 400
    else:
        return jsonify(error=True, message='not found'), 404
    
            
        




@app.route('/api/materia/assunto/questao/<int:id_questao>')
def api_materia_assunto_questao_view(id_questao):
    temp = Pergunta.list_by_id(session=SessionLocal(), id=id_questao)
    if temp:
        print(temp)
        return jsonify(error=False, data=temp)
    return jsonify(error=True, message='not found'), 404









@app.route('/api/materia/assunto/questao/<int:id_questao>/edit', methods=["POST"])
def api_materia_assunto_questao_edit(id_questao):
    if request.method == "POST":
        question = request.form["question"]
        correct = request.form["correct"]
        if not correct.lower() in ('1', '0'):
            return jsonify(error=True, message="\"correct\" value invalid"), 400
        correct = True if correct == '1' else False
        sessao = SessionLocal()
        temp = Pergunta.list_by_id(session=sessao, id=id_questao)
        if temp:
            print(temp)
            temp.question = question
            temp.correct = correct
            sessao.commit()
            data_out = {
                'id': temp.id,
                'assunto_id': temp.assunto_id,
                'question': temp.question,
                'correct': temp.correct,
                'date_created': temp.date_created
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou editar questao"}), 400
    return jsonify(error=True)










@app.route('/api/materia/assunto/questao/<int:id_questao>', methods=["DELETE"])
def api_materia_assunto_questao_delete(id_questao):
    session = SessionLocal()
    temp = Pergunta.list_by_id(session=session, id=id_questao)
    if temp:
        try:
            session.delete(temp)
            session.commit()
            return jsonify(error=False), 204
        except Exception as err:
            return jsonify(error=True, message='exception', detail=str(err)), 400
    else:
        return jsonify(error=True, message='not found'), 404








# random question 
# @app.route('/api/question/create', methods=["POST"])
# def api_question_create():
#     if request.method == "POST":
#         id_materia = request.form["id_materia"]
#         question = request.form["question"]
#         total_alternatives = int(request.form['total_alternatives'])
#         alternatives = []
#         for i in range(0, total_alternatives):
#             temp_is_correct = request.form.getlist(f'alternatives[{i}][is_correct]')[0]
#             alternatives.append({
#                 'alternative': request.form.getlist(f'alternatives[{i}][alternative]')[0],
#                 'is_correct': temp_is_correct
#             })
#         print(alternatives)
#         temp = Pergunta.create(session=SessionLocal(), data={
#             "question": question,
#             "materia_id": id_materia
#         })
#         if temp:
#             for alternative in alternatives:
#                 av = Resposta.create(session=SessionLocal(), data={
#                     'alternative': alternative['alternative'],
#                     'correct': True if alternative['is_correct'].lower() == 's' else False,
#                     'question_id': temp.id
#                 })
#                 if not av:
#                     return jsonify({'error': True, 'message': 'failed add alternative'})
#             data_out = {
#                 'id': temp.id,
#                 'question': temp.question,
#                 'materia_id': temp.materia_id,
#                 'date_created': temp.date_created
#             }
#             return jsonify(error=False, data=data_out)
#         else:
#             return jsonify({"msg": "aplicacao falhou criar materia"}), 400
#     return jsonify(error=True)



# @app.route('/api/alternative/create', methods=["POST"])
# def api_alternative_create():
#     if request.method == "POST":
#         id_question = request.form["id_question"]
#         alternative = request.form["alternative"]
#         correct = request.form["correct"]
#         temp = Pergunta.create(session=SessionLocal(), data={
#             "alternative": alternative,
#             "question_id": id_question,
#             "correct": True if correct.lower() == 's' else False
#         })
#         if temp:
#             data_out = {
#                 'id': temp.id,
#                 'alternative': temp.alternative,
#                 'correct': temp.correct,
#                 'question_id': temp.question_id,
#                 'date_created': temp.date_created
#             }
#             return jsonify(error=False, data=data_out)
#         else:
#             return jsonify({"msg": "aplicacao falhou criar materia"}), 400
#     return jsonify(error=True)