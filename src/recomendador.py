import json
import pandas as pd
import os
from surprise import Dataset, Reader, KNNBasic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(BASE_DIR, "..", "data", "MOCK_DATA.json")


# 1. Cargar los datos desde el archivo JSON
def cargar_datos():
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    ratings_list = []
    for user in data:
        for valoracion in user["valoraciones"]:
            ratings_list.append((user["usuario"], valoracion["destino"], valoracion["valoracion"]))
    return pd.DataFrame(ratings_list, columns=["user", "item", "rating"]), data


# 2. Entrenar modelo KNN colaborativo basado en usuarios
def entrenar_modelo(df):
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(df, reader)
    trainset = dataset.build_full_trainset()

    sim_options = {"name": "cosine", "user_based": True}
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)
    return model, trainset


# 3. Generar recomendaciones para un usuario
def recomendar_destinos(model, trainset, df, usuario_objetivo, top_n=5):
    destinos_usuario = df[df["user"] == usuario_objetivo]["item"].tolist()
    todos_destinos = df["item"].unique()
    destinos_no_vistos = [d for d in todos_destinos if d not in destinos_usuario]

    predicciones = []
    for destino in destinos_no_vistos:
        pred = model.predict(usuario_objetivo, destino)
        predicciones.append((destino, pred.est))

    recomendaciones = sorted(predicciones, key=lambda x: x[1], reverse=True)[:top_n]
    return recomendaciones


""" def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Recomendar destinos a un usuario")
    print("2. Ver todos los destinos disponibles y su valoración media")
    print("0. Salir")
    return input("Selecciona una opción: ")


def mostrar_valoracion_media_destinos(df):
    medias = df.groupby("item")["rating"].mean().sort_values(ascending=False)

    print("\n--- Valoración media por destino ---")
    for destino, media in medias.items():
        print(f"{destino}: {media:.2f}")


def main():
    df, data_original = cargar_datos(ruta_json)
    model, trainset = entrenar_modelo(df)

    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            usuarios = df["user"].unique()
            print("\nUsuarios disponibles:")
            for i, usuario in enumerate(usuarios, 1):
                print(f"{i}. {usuario}")
            seleccion = input("Selecciona el número del usuario: ")
            try:
                idx = int(seleccion) - 1
                if 0 <= idx < len(usuarios):
                    usuario_seleccionado = usuarios[idx]
                    print(f"\nGenerando recomendaciones para {usuario_seleccionado}...\n")
                    recomendaciones = recomendar_destinos(model, trainset, df, usuario_seleccionado)
                    for destino, score in recomendaciones:
                        print(f"- {destino}: puntuación estimada {score:.2f}")
                else:
                    print("Selección inválida.")
            except ValueError:
                print("Entrada no válida.")
        elif opcion == "2":
            mostrar_valoracion_media_destinos(df)
        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no reconocida.")


if __name__ == "__main__":
    main() """