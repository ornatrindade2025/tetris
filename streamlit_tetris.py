import streamlit as st
import subprocess
import os

if 'scores' not in st.session_state:
    st.session_state.scores = []

def run_tetris():
    tetris_script = "tetris_game.py"
    subprocess.Popen(["python", tetris_script])

def save_score(name):
    try:
        if os.path.exists("score.txt"):
            with open("score.txt", "r") as f:
                score = int(f.read())
            st.session_state.scores.append({"name": name, "score": score})
            st.success(f"Pontuação de {score} salva para {name}!")
        else:
            st.warning("Jogo ainda não finalizado ou pontuação não encontrada.")
    except Exception as e:
        st.error(f"Erro ao salvar pontuação: {e}")

def display_scores():
    st.header("Pontuações dos Jogadores")
    if st.session_state.scores:
        for entry in st.session_state.scores:
            st.write(f"{entry['name']}: {entry['score']}")
    else:
        st.write("Nenhuma pontuação registrada ainda.")

def main():
    st.title("Tetris com Streamlit")

    name = st.text_input("Digite seu nome:")

    if st.button("Iniciar Jogo"):
        if name:
            run_tetris()
            st.success(f"Jogo iniciado! Boa sorte, {name}!")
        else:
            st.warning("Por favor, digite seu nome.")

    if st.button("Salvar Pontuação"):
        if name:
            save_score(name)
        else:
            st.warning("Por favor, digite seu nome.")

    display_scores()

if __name__ == "__main__":
    main()