from llm.client import ask_gemma

def main():

    pergunta = input("Pergunte algo: ")

    resposta = ask_gemma(pergunta)

    print("\nResposta:\n")
    print(resposta)
    
if __name__ == "__main__":
    main()