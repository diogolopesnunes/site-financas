from flask import Flask, request, redirect, render_template, flash

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

        maiuscula = False  # Variavel que diz se tem letra maiuscula
        minuscula = False  # Variavel que diz se tem letra minuscula
        numero = False  # Variavel que diz se tem numero
        simbolo = False  # Variavel que diz se tem caractere especial
        # simbolos = "!@#$%^&*()<>,." #Variavel com a lista de simbolos válidos
        # numeros = "0123456789" #Variavel com a lista de números

        for c in senha:
            if c.upper():  # Verifica se tem letra maiuscula na senha
                maiuscula = True

            if c.lower():  # Verifica se tem letra minuscula na senha
                minuscula = True

            if c.isdigit():  # Verifica se tem numero na senha
                numero = True

            if c.isalnum():  # Verifica se tem caractere especial na senha
                simbolo = True

        print(senha)

        if not (maiuscula or minuscula or numero or simbolo):
            flash("A senha deve conter pelo menos uma letra maiuscula e minuscula, um número e um caractere especial")

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
                    print(f"Usuário {u['nome']} logado com sucesso")
                    return redirect('/inicial_usuario')
                else:
                    flash('Credenciais inválidas')
                    return redirect('/login')
        flash('Usuário não encontrado')
        return redirect('/login')
    return render_template('login.html')

@app.route("/inicial_usuario")
def inicial_usuario():
    return render_template("inicial_usuario.html")


@app.route("/editar_perfil")
def editar():
    if request.method == "POST":  # Faz o código rodar caso o usuário preencha e envie as informações no formulário
        nome = request.form.get("nome")  # Informação do nome
        tel = request.form.get("tel")  # Informação do telefone
        cpf = request.form.get("cpf")  # Informação do cpf
        email = request.form.get("email")  # Informação do email
        senha = request.form.get("senha")  # Informação da senha
        confirm_senha = request.form.get("confirm_senha")  # Informação da confirmação de senha

        if not all([nome, tel, cpf, email, senha, confirm_senha]):  # Caso não preencha todos os campos
            flash("Preencha todos os campos!")  # Essa mensagem aparece para o usuário
            return redirect("/editar_perfil")

        for u in usuarios:
            if u['cpf'] == cpf:
                flash("Cpf já cadastrado")
                return redirect("/editar_perfil")

        if senha != confirm_senha:  # Caso a senha não for igual a confirmação
            flash("Senhas não coincidem!")  # Essa mensagem aparece para o usuário
            return redirect("/editar_perfil")

        maiuscula = False  # Variavel que diz se tem letra maiuscula
        minuscula = False  # Variavel que diz se tem letra minuscula
        numero = False  # Variavel que diz se tem numero
        simbolo = False  # Variavel que diz se tem caractere especial

        for c in senha:
            if c.upper():  # Verifica se tem letra maiuscula na senha
                maiuscula = True

            if c.lower():  # Verifica se tem letra minuscula na senha
                minuscula = True

            if c.isdigit():  # Verifica se tem numero na senha
                numero = True

            if c.isalnum():  # Verifica se tem caractere especial na senha
                simbolo = True

        print(senha)

        if not (maiuscula or minuscula or numero or simbolo):
            flash("A senha deve conter pelo menos uma letra maiuscula e minuscula, um número e um caractere especial")

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


@app.route("/historico_transferencia")
def historico_transferencia():
    total = sum(t[3] for t in transferencias)
    return render_template("historico_transferencia.html", transferencias=transferencias, total=total)


@app.route('/adicionar_transferencia', methods=['GET', 'POST'])
def adicionar_transferencia():
    if request.method == 'POST':
        data = request.form['data']
        entrada_saida = request.form['entrada_saida']
        valor = float(request.form['valor'])
        codigo = len(transferencias) + 1
        transferencias.append([codigo, data, entrada_saida, valor])
        return redirect('/historico_transferencia')  
    return render_template('adicionar_transferencia.html')  


@app.route('/editar_transferencia/<int:codigo>', methods=['GET', 'POST'])
def editar_transferencia(codigo):
    if request.method == 'POST':
        global transferencias
        transferencia = transferencias[codigo]
        transferencia[1] = request.form['data']
        transferencia[2] = request.form['entrada_saida']
        transferencia[3] = request.form["valor"]
        flash("Transferência editada com sucesso!")
        return redirect('/historico_transferencia')

    return render_template('editar_transferencia.html', transferencia=transferencia)


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
