from flask import Flask, request, redirect, render_template, flash

app = Flask(__name__)
app.secret_key = "senhanadasecreta"

usuarios = []


@app.route('/')
def home():
    return "Bem-vindo ao meu site!"

@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        tel = request.form["tel"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirm_senha = request.form["confirm_senha"]
        if senha == confirm_senha:
            usuarios.append([nome, tel, cpf, email, senha])
            flash("Cadastro feito com sucesso!")
            return redirect("/inicial_usuario")
    return render_template("cadastro.html")



if __name__ == '__main__':
    app.run(debug=True)