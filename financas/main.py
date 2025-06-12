from flask import Flask, request, redirect, render_template, flash, session

app = Flask(__name__)
app.secret_key = "senhanadasecreta"

usuarios = []
transferencias = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome")
        tel = request.form.get("tel")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirm_senha = request.form.get("confirm_senha")
        maiuscula = False
        minuscula = False
        numero = False
        simbolo = False

        if not all([nome, tel, cpf, email, senha, confirm_senha]):
            flash("Preencha todos os campos!")
            return redirect("/cadastro")

        for u in usuarios:
            if u['cpf'] == cpf:
                flash("Cpf já cadastrado")
                return redirect("/cadastro")

        if senha != confirm_senha:
            flash("Senhas não coincidem!")
            return redirect("/cadastro")
        
        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres")
            return redirect("/cadastro")

        for c in senha:
            if c.isupper():
                maiuscula = True
            elif c.islower():
                minuscula = True
            elif c.isdigit():
                numero = True
            elif not c.isalnum() and not c.isspace():
                simbolo = True

        if not (maiuscula and minuscula and numero and simbolo):
            flash("A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial")
            return redirect("/cadastro")

        usuario = {
            "nome": nome,
            "tel": tel,
            "cpf": cpf,
            "email": email,
            "senha": senha,
            "transferencias": []
        }

        usuarios.append(usuario)
        flash("Cadastro realizado com sucesso!")
        return redirect("/login")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf = request.form['cpf']
        senha = request.form['senha']

        for u in usuarios:
            if u['cpf'] == cpf:
                if u['senha'] == senha:
                    session['usuario_cpf'] = cpf
                    return redirect('/inicial_usuario')
                else:
                    flash('Credenciais inválidas')
                    return redirect('/login')
        flash('Usuário não encontrado')
        return redirect('/login')
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('_flashes', None)
    session.pop('usuario_cpf', None)
    flash('Você foi deslogado com sucesso')
    return redirect('/')

@app.route("/inicial_usuario")
def inicial_usuario():
    if 'usuario_cpf' not in session:
        flash('Por favor, faça login primeiro')
        return redirect('/login')
    
    usuario_atual = next((u for u in usuarios if u['cpf'] == session['usuario_cpf']), None)
    
    if not usuario_atual:
        flash('Usuário não encontrado')
        return redirect('/login')
    
    return render_template("inicial_usuario.html", usuario=usuario_atual)

@app.route("/editar_perfil", methods=["GET", "POST"])
def editar():
    if 'usuario_cpf' not in session:
        flash('Por favor, faça login primeiro')
        return redirect('/login')
    
    usuario_atual = next((u for u in usuarios if u['cpf'] == session['usuario_cpf']), None)
    
    if not usuario_atual:
        flash('Usuário não encontrado')
        return redirect('/login')

    if request.method == "POST":
        nome = request.form.get("nome")
        tel = request.form.get("tel")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirm_senha = request.form.get("confirm_senha")

        if not all([nome, tel, email, senha, confirm_senha]):
            flash("Preencha todos os campos!")
            return redirect("/editar_perfil")

        if senha != confirm_senha:
            flash("Senhas não coincidem!")
            return redirect("/editar_perfil")
        
        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres")
            return redirect("/editar_perfil")

        maiuscula = any(c.isupper() for c in senha)
        minuscula = any(c.islower() for c in senha)
        numero = any(c.isdigit() for c in senha)
        simbolo = any(not c.isalnum() and not c.isspace() for c in senha)

        if not (maiuscula and minuscula and numero and simbolo):
            flash("A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial")
            return redirect("/editar_perfil")

        usuario_atual['nome'] = nome
        usuario_atual['tel'] = tel
        usuario_atual['email'] = email
        usuario_atual['senha'] = senha
        
        return redirect("/inicial_usuario")
        
    return render_template("editar_perfil.html", usuario=usuario_atual)

@app.route("/historico_transferencia")
def historico_transferencia():
    if 'usuario_cpf' not in session:
        flash('Por favor, faça login primeiro')
        return redirect('/login')
    
    usuario_atual = next((u for u in usuarios if u['cpf'] == session['usuario_cpf']), None)
    
    if not usuario_atual:
        flash('Usuário não encontrado')
        return redirect('/login')
    
    entradas = []
    saidas = []

    for t in usuario_atual['transferencias']:
        if t['entrada_saida'] == 'entrada':
            entradas.append(t)
        elif t['entrada_saida'] == 'saida':
            t_corrigida = t.copy()
            t_corrigida['valor'] = abs(t_corrigida['valor'])
            saidas.append(t_corrigida)
    
    total = sum(t['valor'] for t in entradas) - sum(t['valor'] for t in saidas)
    
    return render_template("historico_transferencia.html",
                           entradas=entradas,
                           saidas=saidas,
                           total=total)

@app.route('/adicionar_transferencia', methods=['GET', 'POST'])
def adicionar_transferencia():
    if 'usuario_cpf' not in session:
        flash('Por favor, faça login primeiro')
        return redirect('/login')

    usuario_atual = next((u for u in usuarios if u['cpf'] == session['usuario_cpf']), None)
    if not usuario_atual:
        flash('Usuário não encontrado')
        return redirect('/login')

    if request.method == 'POST':
        try:
            data_sem_formatar = request.form.get('data')
            valor_str = request.form.get('valor')
            descricao = request.form.get('descricao', '')  # Adicione este campo no formulário HTML

            if not data_sem_formatar or not valor_str:
                flash('Preencha todos os campos!')
                return redirect('/adicionar_transferencia')

            try:
                valor = float(valor_str)
                if valor == 0:
                    flash('O valor não pode ser zero!')
                    return redirect('/adicionar_transferencia')
            except ValueError:
                flash('Valor inválido! Digite um número válido.')
                return redirect('/adicionar_transferencia')

            # Gerar código único
            if usuario_atual['transferencias']:
                codigo = max(t['codigo'] for t in usuario_atual['transferencias']) + 1
            else:
                codigo = 1

            # Reformatar data
            try:
                year, month, day = data_sem_formatar.split('-')
                data = f"{day}/{month}/{year}"
            except:
                data = data_sem_formatar

            entrada_ou_saida = "entrada" if valor > 0 else "saida"  # Corrigido para "saida" (sem acento)

            nova_transferencia = {
                'codigo': codigo,
                'data': data,
                'descricao': descricao,
                'entrada_saida': entrada_ou_saida,
                'valor': valor
            }

            usuario_atual['transferencias'].append(nova_transferencia)
            flash('Transferência adicionada com sucesso!')
            return redirect('/historico_transferencia')

        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}')
            return redirect('/adicionar_transferencia')

    return render_template('adicionar_transferencia.html')

@app.route('/editar_transferencia/<int:codigo>', methods=['GET', 'POST'])
def editar_transferencia(codigo):
    if 'usuario_cpf' not in session:
        flash('Por favor, faça login primeiro')
        return redirect('/login')
    
    usuario_atual = next((u for u in usuarios if u['cpf'] == session['usuario_cpf']), None)
    if not usuario_atual:
        flash('Usuário não encontrado')
        return redirect('/login')

    transferencia = next((t for t in usuario_atual['transferencias'] if t['codigo'] == codigo), None)
    
    if transferencia is None:
        flash("Transferência não encontrada!")
        return redirect('/historico_transferencia')

    if request.method == 'POST':
        try:
            data_sem_formatar = request.form['data']
            entrada_saida = request.form['entrada_saida'].lower()
            valor = float(request.form['valor'])
            descricao = request.form.get('descricao', '')
            
            # Formatar data
            if '-' in data_sem_formatar:
                year, month, day = data_sem_formatar.split('-')
                data = f"{day}/{month}/{year}"
            else:
                data = data_sem_formatar
            
            # Corrigir valor para negativo se for saída
            valor_corrigido = abs(valor) if entrada_saida == 'entrada' else -abs(valor)
            
            transferencia.update({
                'data': data,
                'descricao': descricao,
                'entrada_saida': entrada_saida,
                'valor': valor_corrigido
            })
            
            flash("Transferência editada com sucesso!")
            return redirect('/historico_transferencia')
        except (ValueError, KeyError) as e:
            flash(f"Erro ao processar os dados: {str(e)}")
            return redirect(f'/edicionar_transferencia/{codigo}')

    # Preparar data para o input type="date"
    data_input = ""
    if '/' in transferencia['data']:
        try:
            day, month, year = transferencia['data'].split('/')
            data_input = f"{year}-{month}-{day}"
        except ValueError:
            data_input = transferencia['data']
    
    return render_template('editar_transferencia.html',
                         transferencia=transferencia,
                         data=data_input)

@app.route('/apagar_transferencia/<int:codigo>')
def apagar_transferencia(codigo):
    if 'usuario_cpf' not in session:
        flash('Por favor, faça login primeiro')
        return redirect('/login')
    
    usuario_atual = next((u for u in usuarios if u['cpf'] == session['usuario_cpf']), None)
    if not usuario_atual:
        flash('Usuário não encontrado')
        return redirect('/login')
    
    usuario_atual['transferencias'] = [t for t in usuario_atual['transferencias'] if t['codigo'] != codigo]
    flash('Transferência removida com sucesso!')
    return redirect('/historico_transferencia')

@app.route("/reserva_emergencia", methods=["GET", "POST"])
def reserva_emergencia():
    if request.method == "POST":
        try:
            media = float(request.form.get("media"))
            meses = float(request.form.get("meses"))
            prazo = float(request.form.get("prazo"))
            if all([media, meses, prazo]):
                reserva_total = media * meses
                reserva_mensal = reserva_total / prazo
                flash(f"Reserva recomendada: R${reserva_total:.2f} (R${reserva_mensal:.2f} por mês)")
                return redirect("/reserva_emergencia")
        except:
            flash("Valores inválidos!")
        flash("Preencha todos os campos!")
        return redirect("/reserva_emergencia")
    
    return render_template("reserva_emergencia.html")

if __name__ == "__main__":
    app.run(debug=True)
