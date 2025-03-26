![image](https://github.com/user-attachments/assets/8cf79c54-d775-4f7c-ab8b-b26c161e5e25)


**Descrição do Projeto:**

Este projeto é uma implementação do clássico jogo "Flappy Bird" usando a biblioteca Pygame em Python. O jogo envolve um pássaro que o jogador controla, tentando voar através de canos sem colidir com eles. O objetivo é voar o máximo possível e acumular pontos.

**Funcionalidades Principais:**

* **Mecânica de Jogo:**
    * O jogador controla um pássaro que precisa voar através de canos gerados aleatoriamente.
    * O pássaro sobe quando o jogador pressiona a barra de espaço ou clica com o mouse.
    * O jogo termina se o pássaro colidir com um cano ou com o chão.
* **Pontuação:**
    * O jogador ganha pontos ao passar com sucesso por cada par de canos.
    * Exibe a pontuação na tela.
* **Elementos Visuais:**
    * Gráficos do pássaro com animação de batida de asas.
    * Gráficos dos canos com geração aleatória de altura.
    * Gráfico do chão com movimento contínuo.
    * Tela inicial com botão de iniciar.
    * Tela de fim de jogo com botão de reiniciar.
* **Interface do Usuário:**
    * Exibe a pontuação atual durante o jogo.
    * Exibe uma mensagem de "Game Over" e um botão de reiniciar quando o jogo termina.
* **Fontes Personalizadas:**
    * Usa fontes personalizadas para exibir a pontuação e mensagens do jogo.
* **Botões interativos:**
    * Botão iniciar, com gradiente e borda arredondada.
    * Botão reiniciar, com gradiente, sombra e borda arredondada.

**Estrutura do Código:**

* **Classes:**
    * `Passaro`: Representa o pássaro do jogador, com métodos para pular, mover e desenhar.
    * `Cano`: Representa os canos, com métodos para mover, desenhar e verificar colisões.
    * `Chao`: Representa o chão, com métodos para mover e desenhar.
    * `Jogo`: Controla a lógica do jogo, incluindo a inicialização, atualização e desenho dos elementos do jogo.
* **Funções:**
    * `carregar_imagem()`: Carrega e redimensiona imagens para o jogo.
* **Loop do Jogo:**
    * O loop principal do jogo gerencia eventos, atualiza a lógica do jogo e desenha os elementos na tela.

**Tecnologias Utilizadas:**

* **Python:** Linguagem de programação principal.
* **Pygame:** Biblioteca para criação de jogos em Python.
* **os:** Modulo para manipulação de caminhos de arquivos.
* **random:** Modulo para geração de números aleatórios.

**Observações:**

* O jogo utiliza imagens armazenadas em um diretório "imgs" e fontes personalizadas armazenadas em um diretório "fonts".
* A lógica do jogo é implementada de forma clara e organizada, facilitando a compreensão e modificação do código.
* O jogo possui um sistema de botões interativos, que facilitam a interação do jogador com o jogo.
* O jogo usa gradientes e sombras para melhorar a experiencia visual do jogador.

Este projeto demonstra um bom entendimento dos conceitos básicos de desenvolvimento de jogos usando Pygame.
