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
    if request.method == "POST":  # Faz o código rodar caso o usuário preencha e envie as informações no formulário
        nome = request.form.get("nome")  # Informação do nome
        tel = request.form.get("tel")  # Informação do telefone
        cpf = request.form.get("cpf")  # Informação do cpf
        email = request.form.get("email")  # Informação do email
        senha = request.form.get("senha")  # Informação da senha
        confirm_senha = request.form.get("confirm_senha")  # Informação da confirmação de senha
        maiuscula = False  # Variavel que diz se tem letra maiuscula
        minuscula = False  # Variavel que diz se tem letra minuscula
        numero = False  # Variavel que diz se tem numero
        simbolo = False  # Variavel que diz se tem caractere especial

        if not all([nome, tel, cpf, email, senha, confirm_senha]):  # Caso não preencha todos os campos
            flash("Preencha todos os campos!")  # Essa mensagem aparece para o usuário
            return redirect("/cadastro")

        for u in usuarios:
            if u['cpf'] == cpf:
                flash("Cpf já cadastrado")
                return redirect("/cadastro")

        if senha != confirm_senha:  # Caso a senha não for igual a confirmação
            flash("Senhas não coincidem!")  # Essa mensagem aparece para o usuário
            return redirect("/cadastro")
        
        if len(senha) < 8:  # Ou qualquer tamanho mínimo que você queira
            flash("A senha deve ter pelo menos 8 caracteres")
            return redirect("/cadastro")

        for c in senha:
            if c.isupper():  # Verifica se tem letra maiuscula na senha
                maiuscula = True

            elif c.islower():  # Verifica se tem letra minuscula na senha
                minuscula = True

            elif c.isdigit():  # Verifica se tem numero na senha
                numero = True

            elif not c.isalnum() and not c.isspace():  # Verifica se tem caractere especial na senha
                simbolo = True

        if not (maiuscula and minuscula and numero and simbolo):
            flash("A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial")
            return redirect("/cadastro")

        usuario = {
            "nome": nome,
            "tel": tel,
            "cpf": cpf,
            "email": email,
            "senha": senha
        }
        usuarios.append(usuario)
        flash("Cadastro realizado com sucesso!")
        print(usuarios)
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
                    flash('Usuário logado com sucesso')
                    session['usuario_cpf'] = cpf  # Armazena o CPF do usuário na sessão
                    print(f"Usuário {u['nome']} logado com sucesso")
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
    # Verifica se o usuário está logado
    if 'usuario_cpf' not in session:
        flash('Por favor, faça login primeiro')
        return redirect('/login')
    
    # Encontra o usuário atual
    usuario_atual = None
    for u in usuarios:
        if u['cpf'] == session['usuario_cpf']:
            usuario_atual = u
            break
    
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

        # Verificação de complexidade da senha
        maiuscula = any(c.isupper() for c in senha)
        minuscula = any(c.islower() for c in senha)
        numero = any(c.isdigit() for c in senha)
        simbolo = any(not c.isalnum() and not c.isspace() for c in senha)

        if not (maiuscula and minuscula and numero and simbolo):
            flash("A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial")
            return redirect("/editar_perfil")

        # Atualiza os dados do usuário
        usuario_atual['nome'] = nome
        usuario_atual['tel'] = tel
        usuario_atual['email'] = email
        usuario_atual['senha'] = senha

        flash("Perfil atualizado com sucesso!")
        return redirect("/inicial_usuario")
        
    return render_template("editar_perfil.html", usuario=usuario_atual)


@app.route("/historico_transferencia")
def historico_transferencia():
    total = sum(t[3] for t in transferencias)
    return render_template("historico_transferencia.html", transferencias=transferencias, total=total)


@app.route('/adicionar_transferencia', methods=['GET', 'POST'])
def adicionar_transferencia():
    if request.method == 'POST':
        data_sem_formatar = request.form['data']
        entrada_saida = request.form['entrada_saida']
        valor = float(request.form['valor'])
        codigo = len(transferencias) + 1
        data_formatando = data_sem_formatar.split('-')
        data = f"{data_formatando[2]}/{data_formatando[1]}/{data_formatando[0]}"
        transferencias.append([codigo, data, entrada_saida, valor])
        return redirect('/historico_transferencia')  
    return render_template('adicionar_transferencia.html')  


@app.route('/editar_transferencia/<int:codigo>', methods=['GET', 'POST'])
def editar_transferencia(codigo):
    global transferencias
    transferencia = None
    
    # 1. Encontra a transferência pelo código
    for t in transferencias:
        if t[0] == codigo:
            transferencia = t
            break
    
    if not transferencia:
        flash("Transferência não encontrada!")
        return redirect('/historico_transferencia')

    if request.method == 'POST':
        data_sem_formatar = request.form['data']
        entrada_saida = request.form['entrada_saida']
        valor = float(request.form['valor'])
        
        try:
            # Formata a data (DD/MM/YYYY → YYYY-MM-DD)
            data_formatando = data_sem_formatar.split('-')
            data = f"{data_formatando[2]}/{data_formatando[1]}/{data_formatando[0]}"
        except:
            flash("Formato de data inválido!")
            return redirect(f'/editar_transferencia/{codigo}')
        
        # 2. Atualiza a transferência existente (sem index)
        for t in transferencias:
            if t[0] == codigo:
                t[1] = data
                t[2] = entrada_saida
                t[3] = valor
                break
        
        flash("Transferência editada com sucesso!")
        return redirect('/historico_transferencia')
    
    # Prepara a data para o formulário (YYYY-MM-DD)
    data_input = ""
    if transferencia[1].count('/') == 2:
        try:
            day, month, year = transferencia[1].split('/')
            data_input = f"{year}-{month}-{day}"
        except:
            data_input = ""
    
    return render_template('editar_transferencia.html', 
                         codigo=codigo, 
                         data=data_input, 
                         entrada_saida=transferencia[2], 
                         valor=transferencia[3])

@app.route('/apagar_transferencia/<int:codigo>')
def apagar_transferencia(codigo):
    global transferencias
    transferencias = [t for t in transferencias if t[0] != codigo]
    return redirect('/historico_transferencia') 


@app.route("/reserva_emergencia", methods=["GET", "POST"])
def reserva_emergencia():
    if request.method == "POST":
        media = float(request.form.get("media"))  # Informação da média de gastos mensais
        meses = float(request.form.get("meses"))  # Informação do número de meses para a reserva
        prazo = float(request.form.get("prazo"))

        if all([media, meses, prazo]):
            reserva_total = media * meses
            reserva_mensal_recomendada = reserva_total / prazo
            flash(f"Reserva de emergência recomendada: R${reserva_total:.2f} (R${reserva_mensal_recomendada:.2f} por mês)")
            return redirect("/reserva_emergencia")
        flash("Preencha todos os campos!")
        return redirect("/reserva_emergencia")
    
    return render_template("reserva_emergencia.html")



if __name__ == "__main__":
    app.run(debug=True)
