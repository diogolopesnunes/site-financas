from flask import Flask, request, redirect, render_template, flash

app = Flask(__name__)
app.secret_key = "senhanadasecreta"

usuarios = []
logado = []
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
        return redirect("/cadastro")

    return render_template("cadastro.html")


@app.route('/abrir_login')
def abrir_login():
    return render_template('login.html')


@app.route("/login")
def login():
    cpf = request.form['cpf']  # Informação do nome
    senha = request.form['senha']  # Informação do telefone

    for u in usuarios:
        if u['cpf'] == cpf:
            if u['senha'] == senha:
                flash('Usuário logado com sucesso')
                return redirect('/inicial_usuario')
            flash('Credenciais inválidas')
            return redirect('/login')
        flash('Usuário nao encontrado')
        return redirect('/login')


@app.route("/inicial_usuario")
def inicial_usuario():
    return render_template("inicial_usuario.html")

@app.route("/editar")
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
            return redirect("/editar")

        for u in usuarios:
            if u['cpf'] == cpf:
                flash("Cpf já cadastrado")
                return redirect("/editar")

        if senha != confirm_senha:  # Caso a senha não for igual a confirmação
            flash("Senhas não coincidem!")  # Essa mensagem aparece para o usuário
            return redirect("/editar")

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
        flash("Edição realizada com sucesso!")
        print(usuarios)
        return redirect("/editar")

    return render_template("editar.html")


@app.route("/historico_transferencia")
def historico_transferencia():
    return render_template("historico_transferencia.html", transferencias=transferencias)


@app.route('/adicionar_transacao', methods=['GET', 'POST'])
def adicionar_contato():

    if request.method == 'POST':
        tipo = request.form['tipo']
        data = request.form['telefone']
        entrada_saida = request.form['entrada_saida']
        valor = request.form["entrada"]
        transferencias.append([tipo, data, entrada_saida, valor])
        return redirect('/historico_transferencia')  



if __name__ == "__main__":
    app.run(debug=True)
