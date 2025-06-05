from flask import Flask, request, redirect, render_template, flash

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = "senhanadasecreta"  # Chave secreta para sessões e mensagens flash

# Listas para armazenar usuários e transferências (simulando um banco de dados)
usuarios = []
transferencias = []

# Rota principal que renderiza a página inicial
@app.route("/")
def home():
    return render_template("index.html")

# Rota para cadastro de usuários
@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":  # Processa o formulário quando enviado
        # Obtém os dados do formulário
        nome = request.form.get("nome")
        tel = request.form.get("tel")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirm_senha = request.form.get("confirm_senha")

        # Valida se todos os campos foram preenchidos
        if not all([nome, tel, cpf, email, senha, confirm_senha]):
            flash("Preencha todos os campos!")
            return redirect("/cadastro")

        # Verifica se CPF já está cadastrado
        for u in usuarios:
            if u['cpf'] == cpf:
                flash("Cpf já cadastrado")
                return redirect("/cadastro")

        # Verifica se as senhas coincidem
        if senha != confirm_senha:
            flash("Senhas não coincidem!")
            return redirect("/cadastro")

        # Variáveis para validação da senha
        maiuscula = False
        minuscula = False
        numero = False
        simbolo = False

        # Validação da complexidade da senha
        for c in senha:
            if c.upper():
                maiuscula = True
            if c.lower():
                minuscula = True
            if c.isdigit():
                numero = True
            if c.isalnum():
                simbolo = True

        print(senha)  # Debug: mostra a senha no console (não recomendado para produção)

        # Verifica se a senha atende aos requisitos mínimos
        if not (maiuscula or minuscula or numero or simbolo):
            flash("A senha deve conter pelo menos uma letra maiuscula e minuscula, um número e um caractere especial")

        # Cria o dicionário com os dados do usuário
        usuario = {
            "nome": nome,
            "tel": tel,
            "cpf": cpf,
            "email": email,
            "senha": senha
        }

        # Adiciona o usuário à lista e redireciona para login
        usuarios.append(usuario)
        flash("Cadastro realizado com sucesso!")
        print(usuarios)  # Debug: mostra todos os usuários no console
        return redirect("/login")

    return render_template("cadastro.html")

# Rota para login de usuários
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf = request.form['cpf']
        senha = request.form['senha']

        # Verifica as credenciais do usuário
        for u in usuarios:
            if u['cpf'] == cpf:
                if u['senha'] == senha:
                    flash('Usuário logado com sucesso')
                    print(f"Usuário {u['nome']} logado com sucesso")
                    return redirect('/inicial_usuario')
                else:
                    flash('Credenciais inválidas')
                    return redirect('/login')
        flash('Usuário não encontrado')
        return redirect('/login')
    return render_template('login.html')

# Rota para página inicial do usuário após login
@app.route("/inicial_usuario")
def inicial_usuario():
    return render_template("inicial_usuario.html")

# Rota para edição de perfil do usuário
@app.route("/editar_perfil")
def editar():
    if request.method == "POST":
        # Obtém os dados do formulário de edição
        nome = request.form.get("nome")
        tel = request.form.get("tel")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirm_senha = request.form.get("confirm_senha")

        # Validação dos campos
        if not all([nome, tel, cpf, email, senha, confirm_senha]):
            flash("Preencha todos os campos!")
            return redirect("/editar_perfil")

        # Verifica se CPF já existe (exceto para o próprio usuário)
        for u in usuarios:
            if u['cpf'] == cpf:
                flash("Cpf já cadastrado")
                return redirect("/editar_perfil")

        if senha != confirm_senha:
            flash("Senhas não coincidem!")
            return redirect("/editar_perfil")

        # Validação da senha (mesma lógica do cadastro)
        maiuscula = False
        minuscula = False
        numero = False
        simbolo = False

        for c in senha:
            if c.upper():
                maiuscula = True
            if c.lower():
                minuscula = True
            if c.isdigit():
                numero = True
            if c.isalnum():
                simbolo = True

        print(senha)

        if not (maiuscula or minuscula or numero or simbolo):
            flash("A senha deve conter pelo menos uma letra maiuscula e minuscula, um número e um caractere especial")

        # Atualiza os dados do usuário
        for u in usuarios:
            if u["cpf"] == cpf:
                u["nome"] = nome
                u["tel"] = tel
                u["cpf"] = cpf
                u["email"] = email
                u["senha"] = senha
                flash("Edição realizada com sucesso!")
                print(usuarios)
                return redirect("/inicial_perfil")
            
            flash("Usuário não encontrado")
            return redirect("/editar_perfil")
        
    return render_template("editar_perfil.html")

# Rota para exibir histórico de transferências
@app.route("/historico_transferencia")
def historico_transferencia():
    total = sum(t[3] for t in transferencias)  # Calcula o total das transferências
    return render_template("historico_transferencia.html", transferencias=transferencias, total=total)

# Rota para adicionar nova transferência
@app.route('/adicionar_transferencia', methods=['GET', 'POST'])
def adicionar_transferencia():
    if request.method == 'POST':
        # Obtém dados da transferência e adiciona à lista
        data = request.form['data']
        entrada_saida = request.form['entrada_saida']
        valor = float(request.form['valor'])
        codigo = len(transferencias) + 1  # Gera um código único
        transferencias.append([codigo, data, entrada_saida, valor])
        return redirect('/historico_transferencia')  
    return render_template('adicionar_transferencia.html')  

# Rota para editar transferência existente
@app.route('/editar_transferencia/<int:codigo>', methods=['GET', 'POST'])
def editar_transferencia(codigo):
    if request.method == 'POST':
        global transferencias
        transferencia = transferencias[codigo]
        # Atualiza os dados da transferência
        transferencia[1] = request.form['data']
        transferencia[2] = request.form['entrada_saida']
        transferencia[3] = request.form["valor"]
        flash("Transferência editada com sucesso!")
        return redirect('/historico_transferencia')

    return render_template('editar_transferencia.html', transferencia=transferencia)

# Rota para apagar transferência
@app.route('/apagar_transferencia/<int:codigo>')
def apagar_transferencia(codigo):
    global transferencias
    # Remove a transferência com o código especificado
    transferencias = [t for t in transferencias if t[0] != codigo]
    return redirect('/historico_transferencia') 

# Rota para cálculo de reserva de emergência
@app.route("/reserva_emergencia", methods=["GET", "POST"])
def reserva_emergencia():
    if request.method == "POST":
        # Obtém os dados para cálculo da reserva
        media = float(request.form.get("media"))
        meses = float(request.form.get("meses"))
        prazo = float(request.form.get("prazo"))

        if all([media, meses, prazo]):
            # Calcula a reserva total e mensal
            reserva_total = media * meses
            reserva_mensal_recomendada = reserva_total / prazo
            flash(f"Reserva de emergência recomendada: R${reserva_total:.2f} (R${reserva_mensal_recomendada:.2f} por mês)")
            return redirect("/reserva_emergencia")
        flash("Preencha todos os campos!")
        return redirect("/reserva_emergencia")
    
    return render_template("reserva_emergencia.html")

# Inicia a aplicação quando o script é executado diretamente
if __name__ == "__main__":
    app.run(debug=True)
