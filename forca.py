import tkinter as tk
from tkinter import ttk
import json, random

class Forca:
    """
    Classe que representa o jogo da forca nele será passado o nome do arquivo que contém as palavras e o dicionário que será criado a partir do arquivo json
    """
    def __init__(self, nome_arquivo, dict=None):
        """Função que inicializa a classe Forca
        """
        self.nome_arquivo = nome_arquivo
        self.dict = dict

    def pega_arquivo(self):
        """
        Função responsável por pegar o arquivo json e transformar em um dicionário, além de verificar se o arquivo está presente e se o formato do arquivo é válido, caso não seja, retorna uma mensagem de erro e chama o menu novamente. E também verifica a quantidade de temas e palavras dentro dos temas, caso não tenha o mínimo de 5 temas ou 20 palavras, retorna uma mensagem de erro e chama o menu novamente.
        """
        try:
            with open(self.nome_arquivo, 'r') as arq:
                self.dict = json.load(arq)

        except FileNotFoundError:
            print(f'Erro ao abrir o arquivo. Verifique se o arquivo "{self.nome_arquivo}" está presente.')

        except json.JSONDecodeError:
            print(f'O arquivo "{self.nome_arquivo}" contém um formato inválido.')

        for tema in list(self.dict):
            if not self.dict[tema]:
                print(f'O tema "{tema}" não tem nenhuma palavra. Ele será removido do arquivo.')
                del self.dict[tema]

        temas = self.dict
        tema = random.choice(list(temas))
        
        if(len(temas) <= 5):
            print('O arquivo não tem o mínimo de 5 temas.')
            exit()
            
          
        elif(len(self.dict[tema]) <= 20):
            print(f'O tema "{tema}" não tem o mínimo de 20 palavras.\nPegando outro tema...')
            Forca.pega_arquivo(self)
            
        palavra = random.choice(list(self.dict[tema]))
        return tema, palavra
    
    def main():
        """"
        Função da tela inicial do Tkinter, que representa o menu do jogo, onde o jogador escolhe se quer jogar ou sair do jogo.
        """
        global frame_inicio
        frame_inicio = ttk.Frame(root, width=650, height=650, relief=tk.GROOVE, borderwidth=5)
        frame_inicio.propagate(False)
        frame_inicio.pack()

        texto_comeco = tk.Label(frame_inicio, text='Bem vindo ao jogo da forca!', font='Calibri 24')
        texto_comeco.pack()

        texto_regras = tk.Label(frame_inicio, text = """
    - Objetivo: O objetivo do jogo é descobrir a palavra oculta antes de cometer 5 erros.\n
    - Palavra Oculta: No início do jogo, uma palavra é selecionada aleatoriamente. \nOs jogadores não têm conhecimento da palavra, apenas do número de letras e um tema associado a ela.\n
    - Adivinhando as Letras: Os jogadores devem adivinhar letras uma de cada vez.\n Se a letra estiver presente na palavra oculta, ela será revelada nas posições corretas.\n
    - Contagem de Erros: Cada vez que um jogador adivinha uma letra que não está na palavra oculta, é cometido um erro. \nO número de erros permitidos é geralmente 5, mas pode variar.\n
    - Vencer ou Perder: O jogador vence se adivinhar corretamente todas as letras da palavra oculta antes de cometer 6 erros. \nO jogador perde se cometer 5 erros antes de adivinhar corretamente a palavra.\n
    - Dicas: Alguns jogos da forca podem fornecer dicas adicionais para ajudar os jogadores a adivinhar a palavra oculta. \nEssas dicas podem ser na forma de definições, sinônimos ou contexto relacionado ao tema.\n
    - Repetição de Letras: Geralmente, letras já adivinhadas não podem ser repetidas. \nO jogador deve escolher uma letra diferente se a mesma letra já tiver sido adivinhada anteriormente.\n
    - Registro de Letras Adivinhadas: As letras adivinhadas devem ser registradas para que o jogador possa \nacompanhar quais letras já foram tentadas e evitar repetições.\n
    - Reiniciar o Jogo: Após vencer ou perder, os jogadores podem optar por reiniciar o jogo e jogar \nnovamente com uma nova palavra oculta e um novo conjunto de letras para adivinhar.""")
        texto_regras.pack()

        botao_comeco = tk.Button(frame_inicio, text='Começar', command=tela_jogo)
        botao_comeco.pack(side = 'bottom')
    
root = tk.Tk()
root.geometry('850x850')
frame_fim = ''
frame_venceu = ''
retangulos_amarelos = []
    
def tela_jogo():
    """"
    Função responsável por criar a tela do jogo, onde ocorre a lógica do jogo, verificando se a palavra foi descoberta ou se o jogador perdeu, também verifica se a letra já foi utilizada e se a palavra inteira foi inserida. Ao final do jogo a função retorna para o menu para verificar se o jogador quer jogar novamente ou sair do jogo.
    """
    global palavra
    letras = []
    forca = Forca('palavras.txt')
    tema, palavra = forca.pega_arquivo()
    palavra_preenchendo = list(len(palavra)*"-")
    erros = 0
    frame_inicio.pack_forget()
    if frame_fim != '':
        frame_fim.pack_forget()        
    if frame_venceu != '':
        frame_venceu.pack_forget()   

    def verificar_Letra(event):
        """"
        Função que verifica se a letra inserida está seguindo os padrões propostos.
        """
        letra = entryString.get().lower()
        if(letra.isalpha() or letra == '-') and len(letra) == 1:
            return letra
        else:
            if(len(letra)>1):
                texto_erro_acerto.configure(text = "Entrada inválida: a entrada deve ser apenas uma letra.")
            texto_erro_acerto.configure(text = "Entrada inválida: a entrada deve ser uma letra.")
            texto_erro_acerto.after(2000, lambda: texto_erro_acerto.configure(text = ""))
            verificar_Letra(event)

    def jogo(event):
        """"
        Função responsável pelas validações da letra passada, se a letra já foi utilizada, se a letra está na palavra, se a palavra foi descoberta e se o jogador perdeu.
        """
        nonlocal erros
        letra = verificar_Letra(event)
        if letra not in letras:
            letras.append(letra)
        letras_inseridas.configure(text = f'Letras utilizadas:\n{"-".join(sorted(letras))}\n') 
        if(letra not in palavra.lower()):
            texto_erro_acerto.configure(text = 'Você errou, tente novamente!')
            erros += 1
            canvas.itemconfig(erros, fill = 'red')
            if(erros == 6):
                fim_de_jogo()
        else:
            texto_erro_acerto.configure(text = 'Você acertou!')
            atualizar_palavra(letra)
            posicoes = [i for i, value in enumerate(palavra.lower()) if value == letra]
            
            for i in posicoes:
                palavra_preenchendo[i] = letra

            if("".join(palavra_preenchendo).lower() == palavra.lower()):
                venceu()
        texto_erro_acerto.after(2000, lambda: texto_erro_acerto.configure(text = ' '))
        entry.delete(0, 'end')
                    
    def atualizar_palavra(letra):
        """"
        Função que atualiza a palavra na tela, inserindo a letra na posição correta e mudando a cor dos quadrados.
        """
        for i, char in enumerate(palavra):
            if char.lower() == letra:
                canvas_quadrado.itemconfig(retangulos_amarelos[i][0], fill='white')
                canvas_quadrado.itemconfig(retangulos_amarelos[i][1], text=letra)


    global frame_jogo
    frame_jogo = ttk.Frame(root, width = 650, height = 650, relief = tk.GROOVE, borderwidth = 5)
    frame_jogo.propagate(False)
    frame_jogo.pack()
    texto_tema = tk.Label(frame_jogo, text = f'Tema: {tema}')
    texto_tema.pack()

    frame_direito = ttk.Frame(frame_jogo, width = 200, height = 650, relief = tk.GROOVE, borderwidth = 5)
    frame_direito.pack(side = 'right')
    
    frame_esquerdo = ttk.Frame(frame_jogo, width = 200, height = 650, relief = tk.GROOVE, borderwidth = 5)
    frame_esquerdo.pack(side = 'left')
    
    largura_retangulo_principal = 400
    altura_retangulo_principal = 200

    canvas_quadrado = tk.Canvas(frame_esquerdo, width=largura_retangulo_principal, height=altura_retangulo_principal)
    canvas_quadrado.pack()

    largura_retangulo_amarelo = 30
    altura_retangulo_amarelo = 30
    espacamento_horizontal = 10

    posicao_x = (largura_retangulo_principal - (largura_retangulo_amarelo * len(palavra) + espacamento_horizontal * (len(palavra) - 1))) / 2
    posicao_y = altura_retangulo_principal / 2 - altura_retangulo_amarelo / 2

    for i in palavra:
        retangulo = canvas_quadrado.create_rectangle(posicao_x, posicao_y, posicao_x + largura_retangulo_amarelo, posicao_y + altura_retangulo_amarelo, fill="yellow")
        texto = canvas_quadrado.create_text(posicao_x + largura_retangulo_amarelo / 2, posicao_y + altura_retangulo_amarelo / 2, text="", fill="black")
        retangulos_amarelos.append((retangulo, texto))
        posicao_x += largura_retangulo_amarelo + espacamento_horizontal


    texto_palavra = tk.Label(frame_esquerdo, text = f'A palavra tem: {len(palavra)} letras')
    texto_palavra.pack()
    
    
    letras_inseridas = tk.Label(frame_esquerdo, text = ' ')
    letras_inseridas.pack()

    texto_erro_acerto = tk.Label(frame_esquerdo, text = ' ')
    texto_erro_acerto.pack()

    canvas = tk.Canvas(frame_direito, width = 250, height = 250)
    canvas.create_oval(100, 50, 150, 100, outline='gray')
    canvas.create_line(125, 100, 125, 180, fill = 'gray')
    canvas.create_line(70, 160, 125, 110, fill = 'gray')
    canvas.create_line(175, 160, 125, 110, fill = 'gray')
    canvas.create_line(150, 250, 125, 180, fill = 'gray')
    canvas.create_line(100, 250, 125, 180, fill = 'gray')
    canvas.pack()
    
    entryString = tk.StringVar()
    entry = tk.Entry(frame_esquerdo, textvariable = entryString)
    entry.pack()

    botao_insere = tk.Button(frame_esquerdo, text = 'Inserir')
    botao_insere.bind('<Button>', jogo)
    botao_insere.pack(side='left', padx=10)

    botao_limpar = tk.Button(frame_esquerdo, text = 'Limpar')
    botao_limpar.bind('<Button>', lambda event: entry.delete(0, 'end'))
    botao_limpar.pack(side = 'right', padx = 10)

    botao_saida = tk.Button(frame_esquerdo, text = 'Sair do jogo', command = lambda: root.destroy())
    botao_saida.pack(side = 'bottom')
    
def fim_de_jogo():
    """"
    Tela que aparece quando o jogador perde o jogo, onde ele pode escolher se quer jogar novamente ou sair do jogo.
    """
    global frame_fim
    frame_jogo.pack_forget()
    
    frame_fim = ttk.Frame(root, width = 650, height = 650, relief = tk.GROOVE, borderwidth = 5)
    frame_fim.propagate(False)
    frame_fim.pack()
    
    label_fim = tk.Label(frame_fim, text = 'Fim de jogo')
    label_fim.pack()
    
    label_pergunta = tk.Label(frame_fim, text = 'Deseja jogar novamente?')
    label_pergunta.pack()
    
    botao_jogar = tk.Button(frame_fim, text='Jogar novamente', command=tela_jogo)
    botao_jogar.pack()
    
    botao_saida = tk.Button(frame_fim, text = 'Sair do jogo', command = lambda: root.destroy())
    botao_saida.pack()
    
def venceu():
    """"
    Tela que aparece quando o jogador vence o jogo, onde ele pode escolher se quer jogar novamente ou sair do jogo.
    """
    global frame_venceu
    frame_jogo.pack_forget()
    
    frame_venceu = ttk.Frame(root, width = 650, height = 650, relief = tk.GROOVE, borderwidth = 5)
    frame_venceu.propagate(False)
    frame_venceu.pack()
    
    label_venceu = tk.Label(frame_venceu, text = f'Parabéns você venceu!\nVocê descobriu a palavra: {palavra}')
    label_venceu.pack()
    
    label_pergunta = tk.Label(frame_venceu, text = 'Deseja jogar novamente?')
    label_pergunta.pack()
    
    botao_jogar = tk.Button(frame_venceu, text='Jogar novamente', command=tela_jogo)
    botao_jogar.pack()
    
    botao_saida = tk.Button(frame_venceu, text = 'Sair do jogo', command = lambda: root.destroy())
    botao_saida.pack()
    

Forca.main()
root.mainloop()