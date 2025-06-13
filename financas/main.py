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
        if t['valor'] > 0:  # Agora verificamos pelo valor
            entradas.append(t)
        else:
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
            entrada_saida = request.form.get('entrada_saida', '')  # Alterado para entrada_saida

            if not data_sem_formatar or not valor_str or not entrada_saida:
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

            nova_transferencia = {
                'codigo': codigo,
                'data': data,
                'entrada_saida': entrada_saida,  # Usando entrada_saida diretamente
                'valor': valor,
                'tipo': 'entrada' if valor > 0 else 'saida'  # Adicionado campo tipo separado
            }

            usuario_atual['transferencias'].append(nova_transferencia)
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
        return redirect('/historico_transferencia')

    if request.method == 'POST':
        try:
            data_sem_formatar = request.form.get('data')
            valor_str = request.form.get('valor')
            entrada_saida = request.form.get('entrada_saida', '')
            
            # Validações
            if not all([data_sem_formatar, valor_str, entrada_saida]):
                flash('Preencha todos os campos obrigatórios!')
                return redirect(f'/editar_transferencia/{codigo}')
            
            try:
                valor = float(valor_str)
                if valor == 0:
                    flash('O valor não pode ser zero!')
                    return redirect(f'/editar_transferencia/{codigo}')
            except ValueError:
                flash('Valor inválido! Digite um número válido.')
                return redirect(f'/editar_transferencia/{codigo}')

            # Formatar data
            try:
                if '-' in data_sem_formatar:  # Formato YYYY-MM-DD
                    year, month, day = data_sem_formatar.split('-')
                    data_formatada = f"{day}/{month}/{year}"
                else:  # Assume que já está no formato DD/MM/YYYY
                    data_formatada = data_sem_formatar
            except:
                data_formatada = data_sem_formatar
            
            # Atualizar transferência
            transferencia.update({
                'data': data_formatada,
                'entrada_saida': entrada_saida,
                'valor': valor,
                'tipo': 'entrada' if valor > 0 else 'saida'
            })
            
            return redirect('/historico_transferencia')
            
        except Exception as e:
            flash(f"Erro ao processar os dados: {str(e)}")
            return redirect(f'/editar_transferencia/{codigo}')

    # Preparar dados para o template
    data_input = transferencia['data']
    if '/' in data_input:  # Converter DD/MM/YYYY para YYYY-MM-DD
        try:
            day, month, year = data_input.split('/')
            data_input = f"{year}-{month}-{day}"
        except:
            pass
            
    return render_template('editar_transferencia.html',
                         transferencia=transferencia,
                         data=data_input,
                         valor=transferencia['valor'],
                         entrada_saida=transferencia['entrada_saida'],
                         codigo=transferencia['codigo'])

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