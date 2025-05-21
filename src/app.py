from flask import Flask, render_template, request
from recomendador import cargar_datos, entrenar_modelo, recomendar_destinos

app = Flask(__name__)

# Cargar datos y entrenar modelo al arrancar
df, data_original = cargar_datos()
model, trainset = entrenar_modelo(df)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/recomendar', methods=["GET", "POST"])
def recomendar():
    usuarios = df["user"].unique()
    recomendaciones = []

    if request.method == "POST":
        usuario = request.form.get("usuario")
        if usuario:
            recomendaciones = recomendar_destinos(model, trainset, df, usuario)

    return render_template("recomendar.html", usuarios=usuarios, recomendaciones=recomendaciones)

@app.route('/destinos')
def destinos():
    valoraciones = df.groupby("item")["rating"].mean().sort_values(ascending=False)
    return render_template("destinos.html", valoraciones=valoraciones)

if __name__ == '__main__':
    app.run(debug=True)
