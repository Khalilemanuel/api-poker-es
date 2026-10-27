import random

import pytest

from app.modules.motorpartida.baralho import Baralho, BaralhoVazioError
from app.modules.motorpartida.cartas import Carta, Naipe, ValorCarta
from app.modules.motorpartida.distribuicao import CARTAS_POR_JOGADOR, MaoJogador, distribuir_cartas


def test_baralho_novo_tem_52_cartas_distintas():
    baralho = Baralho()

    assert len(baralho) == 52
    assert len(set(baralho.cartas)) == 52


def test_baralho_tem_13_cartas_de_cada_naipe():
    baralho = Baralho()

    for naipe in Naipe:
        assert len([carta for carta in baralho.cartas if carta.naipe == naipe]) == 13


def test_embaralhar_muda_a_ordem_sem_perder_cartas():
    baralho = Baralho(random.Random(42))
    ordem_original = baralho.cartas

    baralho.embaralhar()

    assert baralho.cartas != ordem_original
    assert set(baralho.cartas) == set(ordem_original)


def test_embaralhamentos_diferentes_geram_ordens_diferentes():
    primeiro = Baralho(random.Random(1))
    segundo = Baralho(random.Random(2))

    primeiro.embaralhar()
    segundo.embaralhar()

    assert primeiro.cartas != segundo.cartas


def test_comprar_remove_a_carta_do_baralho():
    baralho = Baralho()

    carta = baralho.comprar()

    assert len(baralho) == 51
    assert carta not in baralho.cartas


def test_comprar_de_baralho_vazio_gera_erro():
    baralho = Baralho()
    for _ in range(52):
        baralho.comprar()

    with pytest.raises(BaralhoVazioError):
        baralho.comprar()


def test_distribuicao_entrega_duas_cartas_para_cada_jogador():
    baralho = Baralho(random.Random(7))
    baralho.embaralhar()

    maos = distribuir_cartas([10, 11, 12], baralho)

    assert list(maos) == [10, 11, 12]
    assert all(len(mao.visualizar_cartas()) == CARTAS_POR_JOGADOR for mao in maos.values())
    assert len(baralho) == 52 - 3 * CARTAS_POR_JOGADOR


def test_distribuicao_nao_repete_cartas_entre_jogadores():
    baralho = Baralho(random.Random(7))
    baralho.embaralhar()

    maos = distribuir_cartas([1, 2, 3, 4, 5, 6, 7, 8, 9], baralho)
    cartas_distribuidas = [carta for mao in maos.values() for carta in mao.visualizar_cartas()]

    assert len(cartas_distribuidas) == 18
    assert len(set(cartas_distribuidas)) == 18
    assert not set(cartas_distribuidas) & set(baralho.cartas)


def test_distribuicao_alterna_uma_carta_por_jogador_a_cada_volta():
    baralho = Baralho(random.Random(3))
    baralho.embaralhar()
    topo = list(reversed(baralho.cartas))

    maos = distribuir_cartas([10, 11], baralho)

    assert maos[10].visualizar_cartas() == [topo[0], topo[2]]
    assert maos[11].visualizar_cartas() == [topo[1], topo[3]]


def test_distribuicao_sem_jogadores_gera_erro():
    with pytest.raises(ValueError):
        distribuir_cartas([], Baralho())


def test_distribuicao_com_jogador_repetido_gera_erro():
    with pytest.raises(ValueError):
        distribuir_cartas([10, 10], Baralho())


def test_mao_nao_aceita_mais_de_duas_cartas():
    mao = MaoJogador(10)
    mao.receber_carta(Carta(naipe=Naipe.COPAS, valor=ValorCarta.AS))
    mao.receber_carta(Carta(naipe=Naipe.OUROS, valor=ValorCarta.REI))

    with pytest.raises(ValueError):
        mao.receber_carta(Carta(naipe=Naipe.PAUS, valor=ValorCarta.DAMA))
