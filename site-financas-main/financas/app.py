from flask import Flask, request, redirect, render_template, flash

app = Flask(__name__)
app.secret_key = "senhanadasecreta"

usuarios = []
logado = []


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST": # Faz o código rodar caso o usuário preencha e envie as informações no formulário
            nome = request.form.get("nome") #Informação do nome
            tel = request.form.get("tel") #Informação do telefone
            cpf = request.form.get("cpf") #Informação do cpf
            email = request.form.get("email") #Informação do email
            senha = request.form.get("senha") #Informação da senha
            confirm_senha = request.form.get("confirm_senha") #Informação da confirmação de senha
            
            if not all([nome, tel, cpf, email, senha, confirm_senha]): #Caso não preencha todos os campos
                flash("Preencha todos os campos!") #Essa mensagem aparece para o usuário
                return redirect("/cadastro")
                
            if senha != confirm_senha:#Caso a senha não for igual a confirmação
                flash("Senhas não coincidem!") #Essa mensagem aparece para o usuário
                return redirect("/cadastro")

            maiuscula = False #Variavel que diz se tem letra maiuscula
            minuscula = False #Variavel que diz se tem letra minuscula
            numero = False #Variavel que diz se tem numero
            simbolo = False #Variavel que diz se tem caractere especial
            simbolos = "!@#$%^&*()<>,." #Variavel com a lista de simbolos válidos
            numeros = "0123456789" #Variavel com a lista de números

            for c in senha:
                if c == c.upper(): #Verifica se tem letra maiuscula na senha
                    maiuscula = True

                elif c == c.lower(): #Verifica se tem letra minuscula na senha
                    minuscula = True

                elif c in numeros: #Verifica se tem numero na senha
                    numero = True

                elif c in simbolos: #Verifica se tem caractere especial na senha
                    simbolo = True

            if maiuscula or minuscula or numero or simbolo == False:
                flash("A senha deve conter pelo menos uma letra maiuscula e minuscula, um número e um caractere especial")
            if maiuscula and minuscula and numero and simbolo == True:
                usuarios.append({"nome": nome, "tel": tel, "cpf": cpf, "email": email, "senha": senha})
                flash("Cadastro realizado com sucesso!")
            return redirect("/cadastro")
    
    return render_template("cadastro.html")


@app.route("/login")
def login():
    if request.method == "POST": # Faz o código rodar caso o usuário preencha e envie as informações no formulário
            cpf = request.form.get("cpf") #Informação do nome
            senha = request.form.get("senha") #Informação do telefone


@app.route("/inicial_usuario")
def pagina_inicial_usuario():
    return render_template("inicial_usuario.html")


if __name__ == "__main__":
    app.run(debug=True)
