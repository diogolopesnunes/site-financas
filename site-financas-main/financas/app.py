from flask import Flask, request, redirect, render_template, flash

app = Flask(__name__)
app.secret_key = "senhanadasecreta"

usuarios = []


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inicial_usuario")
def pagina_inicial_usuario():
    return render_template("inicial_usuario.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        try:
            nome = request.form.get("nome")
            tel = request.form.get("tel")
            cpf = request.form.get("cpf")
            email = request.form.get("email")
            senha = request.form.get("senha")
            confirm_senha = request.form.get("confirm_senha")
            
            if not all([nome, tel, cpf, email, senha, confirm_senha]):
                flash("Preencha todos os campos!")
                return redirect("/cadastro")
                
            if senha != confirm_senha:
                flash("Senhas não coincidem!")
                return redirect("/cadastro")
                
            usuarios.append({"nome": nome, "tel": tel, "cpf": cpf, "email": email, "senha": senha})
            flash("Cadastro realizado com sucesso!")
            return redirect("/cadastro")
            
        except Exception as e:
            flash(f"Erro no cadastro: {str(e)}")
            return redirect("/cadastro")
    
    return render_template("cadastro.html")



if __name__ == "__main__":
    app.run(debug=True)
