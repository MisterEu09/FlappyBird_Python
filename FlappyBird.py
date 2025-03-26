import pygame
import os
import random

# Inicializar o módulo de fontes
pygame.font.init()

# Constantes
TELA_LARGURA = 500
TELA_ALTURA = 800
VELOCIDADE_JOGO = 5
# Carregar fontes
FONTE_PONTOS = pygame.font.Font('./fonts/sourgummy.ttf', 50)  # Carregar fonte personalizada
FONTE_REINICIAR = pygame.font.Font('./fonts/flappybirdy.ttf', 40)  # Carregar fonte personalizada
FONTE_GET_READY = pygame.font.Font('./fonts/flappybirdy.ttf', 60)  # Carregar fonte personalizada


# Carregar imagens
def carregar_imagem(nome):
    caminho = os.path.join('imgs', nome)
    return pygame.transform.scale2x(pygame.image.load(caminho))

IMAGEM_CANO = carregar_imagem('pipe.png')
IMAGEM_CHAO = carregar_imagem('base.png')
IMAGEM_BACKGROUND = carregar_imagem('bg.png')
IMAGENS_PASSARO = [carregar_imagem(f'bird{i}.png') for i in range(1, 4)]


class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))




class Jogo:
    def __init__(self):
        self.passaros = [Passaro(230, 350)]
        self.chao = Chao(730)
        self.canos = [Cano(700)]
        self.tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
        self.pontos = 0
        self.relogio = pygame.time.Clock()
        self.jogo_acabou = False
        self.jogo_iniciado = False # Novo estado para controlar se o jogo começou

    def reiniciar(self):
        self.passaros = [Passaro(230, 350)]
        self.chao = Chao(730)
        self.canos = [Cano(700)]
        self.pontos = 0
        self.jogo_acabou = False
        self.jogo_iniciado = True # Reiniciar o jogo, mas manter iniciado

    def desenhar_botao_iniciar(self):
        texto_iniciar = FONTE_REINICIAR.render("Iniciar", True, (255, 255, 255))
        retangulo_iniciar = texto_iniciar.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 + 100))
        retangulo_botao = retangulo_iniciar.inflate(20, 10)  # Retângulo maior para o botão

        # Criar um gradiente
        gradiente = pygame.Surface((retangulo_botao.width, retangulo_botao.height))
        for y in range(gradiente.get_height()):
            cor = (0, 100 + y // 2, 200)  # Exemplo de gradiente azul
            pygame.draw.line(gradiente, cor, (0, y), (gradiente.get_width(), y))

        # Desenhar o gradiente no retângulo do botão
        self.tela.blit(gradiente, retangulo_botao)

        # Desenhar a borda arredondada
        pygame.draw.rect(self.tela, (0, 0, 0), retangulo_botao, border_radius=5, width=2)  # Borda preta

        # Desenhar o texto
        self.tela.blit(texto_iniciar, retangulo_iniciar)

        return retangulo_iniciar


    def desenhar_botao_reiniciar(self):
        texto_reiniciar = FONTE_REINICIAR.render("Reiniciar", True, (255, 255, 255))
        retangulo_reiniciar = texto_reiniciar.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 + 50))
        retangulo_botao = retangulo_reiniciar.inflate(40, 20)  # Aumentar o tamanho do botão

        # Criar um gradiente
        gradiente = pygame.Surface((retangulo_botao.width, retangulo_botao.height))
        for y in range(gradiente.get_height()):
            cor = (200, 50 + y // 2, 0)  # Exemplo de gradiente vermelho
            pygame.draw.line(gradiente, cor, (0, y), (gradiente.get_width(), y))

        # Desenhar o gradiente no retângulo do botão
        self.tela.blit(gradiente, retangulo_botao)

        # Desenhar a borda arredondada
        pygame.draw.rect(self.tela, (0, 0, 0), retangulo_botao, border_radius=10, width=3)  # Borda preta

        # Desenhar o texto com sombra
        sombra_texto = FONTE_REINICIAR.render("Reiniciar", True, (0, 0, 0))
        self.tela.blit(sombra_texto, retangulo_reiniciar.move(2, 2))  # Sombra deslocada

        self.tela.blit(texto_reiniciar, retangulo_reiniciar)

        return retangulo_reiniciar
    
    def desenhar_tela_inicial(self):
        self.tela.blit(IMAGEM_BACKGROUND, (0, 0))
        texto_get_ready = FONTE_GET_READY.render("Get Ready", True, (255, 255, 255))
        sombra_texto = FONTE_GET_READY.render("Get Ready", True, (0, 0, 0))
        retangulo_get_ready = texto_get_ready.get_rect(center=(TELA_LARGURA // 2 + 2, TELA_ALTURA // 2 - 48))  # Sombra deslocada
        self.tela.blit(sombra_texto, retangulo_get_ready)

        retangulo_get_ready = texto_get_ready.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 - 50))
        self.tela.blit(texto_get_ready, retangulo_get_ready)
        self.desenhar_botao_iniciar()
        pygame.display.update()


    def desenhar_tela(self):
        self.tela.blit(IMAGEM_BACKGROUND, (0, 0))
        for passaro in self.passaros:
            passaro.desenhar(self.tela)
        for cano in self.canos:
            cano.desenhar(self.tela)
        texto = FONTE_PONTOS.render(f"Pontuação: {self.pontos}", 1, (255, 255, 255))
         # Desenhar o texto com sombra
        sombra_texto = FONTE_PONTOS.render(f"Pontuação: {self.pontos}", True, (0, 0, 0))
        self.tela.blit(sombra_texto, (TELA_LARGURA - 8 - texto.get_width(), 12))  # Sombra deslocada

        self.tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

        self.chao.desenhar(self.tela)
        if self.jogo_acabou:
            self.desenhar_botao_reiniciar()
        pygame.display.update()

    def atualizar_jogo(self):
        if self.jogo_iniciado and not self.jogo_acabou:
            for passaro in self.passaros:
                passaro.mover()
            self.chao.mover()

            adicionar_cano = False
            remover_canos = []
            for cano in self.canos:
                for i, passaro in enumerate(self.passaros):
                    if cano.colidir(passaro):
                        self.passaros.pop(i)
                        if not self.passaros:
                            self.jogo_acabou = True
                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        adicionar_cano = True
                cano.mover()
                if cano.x + cano.CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)

            if adicionar_cano:
                self.pontos += 1
                self.canos.append(Cano(600))
            for cano in remover_canos:
                self.canos.remove(cano)

            for i, passaro in enumerate(self.passaros):
                if (passaro.y + passaro.imagem.get_height()) > self.chao.y or passaro.y < 0:
                    self.passaros.pop(i)
                    if not self.passaros:
                        self.jogo_acabou = True

    def executar(self):
        rodando = True
        while rodando:
            self.relogio.tick(30)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    if not self.jogo_iniciado:
                        if self.desenhar_botao_iniciar().collidepoint(pos_mouse):
                            self.jogo_iniciado = True
                    elif self.jogo_acabou:
                        if self.desenhar_botao_reiniciar().collidepoint(pos_mouse):
                            self.reiniciar()
                if evento.type == pygame.KEYDOWN and self.jogo_iniciado and not self.jogo_acabou:
                    if evento.key == pygame.K_SPACE:
                        for passaro in self.passaros:
                            passaro.pular()

            if not self.jogo_iniciado:
                self.desenhar_tela_inicial()
            else:
                self.atualizar_jogo()
                self.desenhar_tela()

        pygame.quit()

if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()



















