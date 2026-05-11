from flask import Flask, request, render_template_string, redirect
import random
import json
import copy
from datetime import datetime, timedelta

app = Flask(__name__)

# ===================== HISTÓRICO =====================

ARQUIVO_HISTORICO = "historico.json"

ARQUIVO_JOGADORES = "jogadores.json"

ARQUIVO_PROXIMO_JOGO = "proximo_jogo.json"


def carregar_jogadores():

    with open(
        ARQUIVO_JOGADORES,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)

def salvar_jogadores(dados):

    with open(
        ARQUIVO_JOGADORES,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

def carregar_proximo_jogo():

    try:

        with open(
            ARQUIVO_PROXIMO_JOGO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except:

        return {}

def salvar_proximo_jogo(dados):

    with open(
        ARQUIVO_PROXIMO_JOGO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

def carregar_historico():

    try:

        with open(
            ARQUIVO_HISTORICO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except:

        return []



# ===================== MENU =====================

@app.route("/")
def index():

    html = """

    <html>

    <head>

        <title>Futebol de Sábado</title>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>

            body {
                font-family: Arial;
                padding: 30px;
                text-align: center;
                font-size: 24px;
            }

            h1 {
                color: #222;
                font-size: 42px;
                margin-bottom: 40px;
            }

            button {
                width: 320px;
                padding: 22px;
                margin-top: 20px;
                font-size: 28px;
                cursor: pointer;
                border-radius: 12px;
            }

        </style>

    </head>

    <body>

        <h1>Futebol de Sábado</h1>

        <a href="/sortear-times">
            <button>
                Sortear Times
            </button>
        </a>

        <br>

        <a href="/proximo-jogo">
            <button>
                Próximo Jogo
            </button>
        </a>

        <br>

        <a href="/historico">
            <button>
                Jogos Anteriores
            </button>
        </a>

        <br>

        <a href="/jogadores">
            <button>
                Jogadores Cadastrados
            </button>
        </a>

    </body>

    </html>

    """

    return render_template_string(html)


# ===================== PÁGINA DE SORTEIO =====================

@app.route("/sortear-times")
def pagina_sorteio():

    dados_jogadores = carregar_jogadores()

    goleiros = sorted(
        dados_jogadores["goleiros"]
    )

    zagueiros = sorted(
        dados_jogadores["zagueiros"]
    )

    atacantes = sorted(
        dados_jogadores["atacantes"]
    )

    html = """

    <html>

    <head>

        <title>Sorteador de Times</title>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>

            body {
                font-family: Arial;
                padding: 20px;
                text-align: center;
                font-size: 26px;
            }

            h1 {
                color: #222;
                font-size: 42px;
            }

            h2 {
                margin-top: 50px;
                font-size: 34px;
            }

            button {
                margin-top: 40px;
                padding: 20px 30px;
                font-size: 28px;
                cursor: pointer;
                border-radius: 12px;
            }

            input[type="checkbox"] {
                transform: scale(2);
                margin-right: 18px;
            }

            .linha-jogador {
                margin-top: 22px;
                margin-bottom: 22px;
            }

            input:disabled {
                opacity: 0.4;
            }

        </style>

    </head>

    <body>

        <h1>Sorteador de Times</h1>

        <form action="/sortear" method="POST">

            <h2>Goleiros</h2>

            {% for jogador in goleiros %}

                <div class="linha-jogador">

                    <input
                        type="checkbox"
                        name="goleiros"
                        value="{{ jogador }}"
                        class="goleiro"
                    >

                    {{ jogador }}

                </div>

            {% endfor %}



            <h2>Zagueiros</h2>

            {% for jogador in zagueiros %}

                <div class="linha-jogador">

                    <input
                        type="checkbox"
                        name="zagueiros"
                        value="{{ jogador }}"
                        class="jogador"
                    >

                    {{ jogador }}

                </div>

            {% endfor %}



            <h2>Atacantes</h2>

            {% for jogador in atacantes %}

                <div class="linha-jogador">

                    <input
                        type="checkbox"
                        name="atacantes"
                        value="{{ jogador }}"
                        class="jogador"
                    >

                    {{ jogador }}

                </div>

            {% endfor %}



            <button type="submit">
                Sortear Times
            </button>

        </form>

        <br><br>

        <a href="/">
            Voltar ao menu
        </a>


        <script>

        function atualizarLimites() {

            const goleiros =
                document.querySelectorAll('.goleiro')

            const todos =
                document.querySelectorAll(
                    'input[type="checkbox"]'
                )

            let goleirosMarcados = 0
            let totalMarcados = 0


            goleiros.forEach(g => {

                if (g.checked) {

                    goleirosMarcados++
                }
            })


            todos.forEach(j => {

                if (j.checked) {

                    totalMarcados++
                }
            })


            todos.forEach(j => {

                if (!j.checked) {

                    j.disabled = totalMarcados >= 14
                }
            })


            goleiros.forEach(g => {

                if (!g.checked) {

                    g.disabled =
                        goleirosMarcados >= 2
                }
            })


            if (totalMarcados < 14) {

                todos.forEach(j => {

                    if (
                        !j.classList.contains(
                            'goleiro'
                        )
                    ) {

                        j.disabled = false
                    }
                })


                goleiros.forEach(g => {

                    if (!g.checked) {

                        g.disabled =
                            goleirosMarcados >= 2
                    }
                })
            }
        }


        const checkboxes =
            document.querySelectorAll(
                'input[type="checkbox"]'
            )

        checkboxes.forEach(c => {

            c.addEventListener(
                'change',
                atualizarLimites
            )
        })

        </script>

    </body>

    </html>

    """

    return render_template_string(
        html,
        goleiros=goleiros,
        zagueiros=zagueiros,
        atacantes=atacantes
    )


# ===================== PROCESSAR SORTEIO =====================

@app.route("/sortear", methods=["POST"])
def sortear():

    goleiros_jogando = request.form.getlist(
        "goleiros"
    )

    zagueiros_jogando = request.form.getlist(
        "zagueiros"
    )

    atacantes_jogando = request.form.getlist(
        "atacantes"
    )

    todos_jogando = (
        goleiros_jogando
        + zagueiros_jogando
        + atacantes_jogando
    )


    if len(goleiros_jogando) != 2:

        return """

        <h1>Erro</h1>

        <p>
        Você precisa selecionar exatamente 2 goleiros.
        </p>

        <a href="/sortear-times">
        Voltar
        </a>
        """


    if len(todos_jogando) != 14:

        return """

        <h1>Erro</h1>

        <p>
        Você precisa selecionar exatamente 14 jogadores.
        </p>

        <a href="/sortear-times">
        Voltar
        </a>
        """


    time_1 = []
    time_2 = []


    goleiros_sorteio = goleiros_jogando.copy()

    goleiro_sorteado = random.choice(
        goleiros_sorteio
    )

    time_1.append("🥅 " + goleiro_sorteado)

    goleiros_sorteio.remove(goleiro_sorteado)

    time_2.append("🥅 " + goleiros_sorteio[0])


    zagueiros_sorteio = zagueiros_jogando.copy()

    while zagueiros_sorteio:

        sorteado = random.choice(
            zagueiros_sorteio
        )

        zagueiros_sorteio.remove(sorteado)

        if len(time_1) <= len(time_2):

            time_1.append(sorteado)

        else:

            time_2.append(sorteado)


    atacantes_sorteio = atacantes_jogando.copy()

    while len(time_1) < 7 or len(time_2) < 7:

        sorteado = random.choice(
            atacantes_sorteio
        )

        atacantes_sorteio.remove(sorteado)

        if len(time_1) <= len(time_2):

            time_1.append(sorteado)

        else:

            time_2.append(sorteado)


    html_resultado = """

    <html>

    <head>

        <title>Times Sorteados</title>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>

            body {
                font-family: Arial;
                padding: 20px;
                text-align: center;
                font-size: 26px;
            }

            h1 {
                font-size: 42px;
            }

            h2 {
                font-size: 34px;
            }

            .times {
                display: flex;
                justify-content: center;
                gap: 80px;
                flex-wrap: wrap;
            }

            ul {
                list-style-position: inside;
                padding: 0;
            }

            li {
                margin-top: 16px;
                margin-bottom: 16px;
            }

            button {
                padding: 20px 30px;
                font-size: 26px;
                cursor: pointer;
                border-radius: 12px;
            }

        </style>

    </head>

    <body>

        <h1>Times Sorteados</h1>

        <div class="times">

            <div>

                <h2>Time 1</h2>

                <ul>

                    {% for jogador in time_1 %}

                        <li>{{ jogador }}</li>

                    {% endfor %}

                </ul>

            </div>



            <div>

                <h2>Time 2</h2>

                <ul>

                    {% for jogador in time_2 %}

                        <li>{{ jogador }}</li>

                    {% endfor %}

                </ul>

            </div>

        </div>



        <br>

        <form
            action="/sortear"
            method="POST"
        >

            {% for jogador in goleiros_jogando %}

                <input
                    type="hidden"
                    name="goleiros"
                    value="{{ jogador }}"
                >

            {% endfor %}

            {% for jogador in zagueiros_jogando %}

                <input
                    type="hidden"
                    name="zagueiros"
                    value="{{ jogador }}"
                >

            {% endfor %}

            {% for jogador in atacantes_jogando %}

                <input
                    type="hidden"
                    name="atacantes"
                    value="{{ jogador }}"
                >

            {% endfor %}

            <button type="submit">

                Fazer novo sorteio

            </button>

        </form>

        <br>

        <form
            action="/salvar-proximo-jogo"
            method="POST"
        >

            <input
                type="hidden"
                name="time_1"
                value='{{ time_1 | tojson }}'
            >

            <input
                type="hidden"
                name="time_2"
                value='{{ time_2 | tojson }}'
            >

            <button type="submit">

                Salvar como próximo jogo

            </button>

        </form>

        <br>

        <a
            href="https://wa.me/?text={{ mensagem_whatsapp | urlencode }}"
            target="_blank"
        >

            <button
                style="
                    background-color: #25D366;
                    color: white;
                "
            >
                📲 Enviar times no WhatsApp
            </button>

        </a>

        <br><br>

        <a href="/">
            Voltar ao menu
        </a>

    </body>

    </html>

    """

    mensagem_whatsapp = f"""

    🏆 TIMES SORTEADOS — FUTEBOL DE SÁBADO

    🔵 TIME 1
    {chr(10).join(time_1)}

    🔴 TIME 2
    {chr(10).join(time_2)}

    """

    return render_template_string(
        html_resultado,
        time_1=time_1,
        time_2=time_2,
        goleiros_jogando=goleiros_jogando,
        zagueiros_jogando=zagueiros_jogando,
        atacantes_jogando=atacantes_jogando,
        mensagem_whatsapp=mensagem_whatsapp
    )


# ===================== SALVAR PRÓXIMO JOGO =====================

@app.route(
    "/salvar-proximo-jogo",
    methods=["POST"]
)
def salvar_proximo_jogo_rota():

    time_1_original = json.loads(
        request.form["time_1"]
    )

    time_2_original = json.loads(
        request.form["time_2"]
    )


    time_1 = []

    for jogador in time_1_original:

        time_1.append({

            "nome": jogador,

            "pagou": False
        })


    time_2 = []

    for jogador in time_2_original:

        time_2.append({

            "nome": jogador,

            "pagou": False
        })

    hoje = datetime.now()

    dias_ate_sabado = (5 - hoje.weekday()) % 7

    if dias_ate_sabado == 0:
        dias_ate_sabado = 7

    proximo_sabado = hoje + timedelta(
        days=dias_ate_sabado
    )

    data_formatada = proximo_sabado.strftime(
        "%d/%m/%Y"
    )


    dados = {

        "data": data_formatada,

        "time_1": time_1,

        "time_2": time_2
    }


    salvar_proximo_jogo(dados)


    return """

    <h1>
        Próximo jogo salvo com sucesso.
    </h1>

    <br><br>

    <a href="/proximo-jogo">
        Ver próximo jogo
    </a>

    <br><br>

    <a href="/">
        Voltar ao menu
    </a>

    """

# ===================== PRÓXIMO JOGO =====================

@app.route("/proximo-jogo")
def proximo_jogo():

    jogo = carregar_proximo_jogo()

    if not jogo:

        return """

        <h1>
            Nenhum próximo jogo definido.
        </h1>

        <br>

        <a href="/">
            Voltar
        </a>

        """


    html = """

    <html>

    <head>

        <title>Próximo Jogo</title>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>

            body {
                font-family: Arial;
                padding: 20px;
                text-align: center;
                font-size: 26px;
            }

            h1 {
                font-size: 40px;
            }

            h2 {
                font-size: 34px;
            }

            .times {
                display: flex;
                justify-content: center;
                gap: 80px;
                flex-wrap: wrap;
            }

            ul {
                list-style-position: inside;
                padding: 0;
            }

            li {
                margin-top: 18px;
                margin-bottom: 18px;
            }

            .pagar {
                cursor: pointer;
                text-decoration: none;
                font-weight: bold;
                margin-left: 12px;
                font-size: 28px;
            }

            .vermelho {
                color: red;
                -webkit-text-stroke: 0.8px black;
            }

            .verde {
                color: green;
                -webkit-text-stroke: 0.8px black;
            }

        </style>

    </head>

    <body>

        <h1>
            Próximo jogo — {{ jogo.data }}
        </h1>

        <div class="times">

            <div>

                <h2>Time 1</h2>

                <ul>

                    {% for jogador in jogo.time_1 %}

                        <li>

                            {{ jogador.nome }}

                            <a
                                href="/toggle-pagamento/time_1/{{ loop.index0 }}"
                                class="pagar
                                {% if jogador.pagou %}
                                    verde
                                {% else %}
                                    vermelho
                                {% endif %}"
                                title="Sinalizar pagamento da quadra"
                            >
                                $
                            </a>

                        </li>

                    {% endfor %}

                </ul>

            </div>



            <div>

                <h2>Time 2</h2>

                <ul>

                    {% for jogador in jogo.time_2 %}

                        <li>

                            {{ jogador.nome }}

                            <a
                                href="/toggle-pagamento/time_2/{{ loop.index0 }}"
                                class="pagar
                                {% if jogador.pagou %}
                                    verde
                                {% else %}
                                    vermelho
                                {% endif %}"
                                title="Sinalizar pagamento da quadra"
                            >
                                $
                            </a>

                        </li>

                    {% endfor %}

                </ul>

            </div>

        </div>

        <a
            href="https://wa.me/?text={{ mensagem_whatsapp | urlencode }}"
            target="_blank"
        >

            <button
                style="
                    background-color: #25D366;
                    color: white;
                    padding: 20px;
                    font-size: 26px;
                    border: none;
                    border-radius: 12px;
                    cursor: pointer;
                "
            >
                📲 ENVIAR TIMES NO WHATSAPP
            </button>

        </a>

        <br><br>

        <a
            href="/limpar-proximo-jogo"

            onclick="
                return confirm(
                    'Tem certeza que deseja descartar os times atuais?'
                )
            "
        >

            <button
                style="
                    background-color: red;
                    color: white;
                    padding: 20px;
                    font-size: 26px;
                    border: none;
                    border-radius: 12px;
                    cursor: pointer;
                "
            >
                🗑️ DESCARTAR TIMES
            </button>

        </a>


        <br><br>

        <a
            href="/finalizar-jogo"

            onclick="
                return confirm(
                    'Tem certeza que o jogo já foi realizado? Esta ação moverá os times para o histórico.'
                )
            "
        >

            <button
                style="
                    background-color: orange;
                    color: white;
                    padding: 24px;
                    font-size: 30px;
                    font-weight: bold;
                    border: none;
                    border-radius: 14px;
                    cursor: pointer;
                "
            >
                ⚠️ AVISAR QUE PARTIDA JÁ ACONTECEU
            </button>

        </a>

        <br><br>

        <a href="/">
            Voltar
        </a>

    </body>

    </html>

    """

    mensagem_whatsapp = f"""

    🏆 PRÓXIMO JOGO — FUTEBOL DE SÁBADO

    🔵 TIME 1
    {chr(10).join([j["nome"] for j in jogo["time_1"]])}

    🔴 TIME 2
    {chr(10).join([j["nome"] for j in jogo["time_2"]])}

    """

    return render_template_string(
        html,
        jogo=jogo,
        mensagem_whatsapp=mensagem_whatsapp
    )

# ===================== HISTÓRICO =====================

@app.route("/historico")
def historico():

    historico = carregar_historico()

    html = """

    <html>

    <head>

        <title>Jogos Anteriores</title>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>

            body {
                font-family: Arial;
                padding: 20px;
                text-align: center;
                font-size: 26px;
            }

            h1 {
                font-size: 42px;
            }

            .jogo {
                margin-bottom: 50px;
            }

        </style>

    </head>

    <body>

        <h1>Jogos Anteriores</h1>

        {% for jogo in historico %}

            <div class="jogo">

                <h3>
                    {{ jogo.data }}
                </h3>

                <b>Time 1:</b>

                {% for jogador in jogo.time_1 %}

                    {{ jogador.nome }}

                    <span
                        style="
                            color:
                            {% if jogador.pagou == true %}
                                green
                            {% else %}
                                red
                            {% endif %};

                            font-weight:bold;
                        "
                    >
                        $
                    </span>

                    {% if not loop.last %}
                        ,
                    {% endif %}

                {% endfor %}

                <br><br>

                <b>Time 2:</b>

                {% for jogador in jogo.time_2 %}

                    {{ jogador.nome }}

                    <span
                        style="
                            color:
                            {% if jogador.pagou == true %}
                                green
                            {% else %}
                                red
                            {% endif %};

                            font-weight:bold;
                        "
                    >
                        $
                    </span>
                    {% if not loop.last %}
                        ,
                    {% endif %}

                {% endfor %}

            </div>

            <hr>

        {% endfor %}

        <br>

        <a href="/">
            Voltar
        </a>

    </body>

    </html>

    """

    return render_template_string(
        html,
        historico=historico
    )


# ===================== JOGADORES =====================

@app.route("/jogadores")
def jogadores():

    dados_jogadores = carregar_jogadores()

    for categoria in dados_jogadores:

        dados_jogadores[categoria].sort(
            key=str.lower
        )

    html = """

    <html>

    <head>

        <title>Jogadores</title>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>

            body {
                font-family: Arial;
                padding: 20px;
                text-align: center;
                font-size: 26px;
            }

            h1 {
                font-size: 42px;
            }

            h2 {
                margin-top: 50px;
            }

            .jogador {
                margin-top: 18px;
                margin-bottom: 18px;
            }

            button {
                padding: 4px 10px;
                font-size: 14px;
                margin-left: 10px;
                cursor: pointer;
            }

            a {
                text-decoration: none;
            }

            .novo {
                margin-top: 40px;
            }

        </style>

    </head>

    <body>

        <h1>Jogadores Cadastrados</h1>

        {% for categoria, lista in dados.items() %}

            <h2>
                {{ categoria.title() }}
            </h2>

            {% for jogador in lista %}

                <div class="jogador">

                    {{ jogador }}

                    <a href="/editar-jogador/{{ categoria }}/{{ jogador }}">

                        <button>
                            ✏️ Editar
                        </button>

                    </a>

                    <a href="/excluir-jogador/{{ categoria }}/{{ jogador }}">

                        <button>
                            🗑️ Excluir
                        </button>

                    </a>

                </div>

            {% endfor %}

        {% endfor %}

        <div class="novo">

            <a href="/novo-jogador">

                <button
                    style="
                        padding: 10px 18px;
                        font-size: 20px;
                    "
                >
                    ➕ Cadastrar novo jogador
                </button>

            </a>

        </div>

        <br><br>

        <a href="/">
            Voltar
        </a>

    </body>

    </html>

    """

    return render_template_string(
        html,
        dados=dados_jogadores
    )

@app.route("/novo-jogador", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":

        nome = request.form["nome"].strip()

        categoria = request.form["categoria"]

        dados = carregar_jogadores()

        dados[categoria].append(nome)

        salvar_jogadores(dados)

        return redirect("/jogadores")


    html = """

    <html>

    <body style="font-family: Arial; text-align:center; padding:40px; font-size:26px;">

        <h1>Cadastrar Jogador</h1>

        <form method="POST">

            <input
                type="text"
                name="nome"
                placeholder="Nome do jogador"
                required
                style="font-size:24px; padding:10px;"
            >

            <br><br>

            <select
                name="categoria"
                style="font-size:24px; padding:10px;"
            >

                <option value="goleiros">
                    Goleiro
                </option>

                <option value="zagueiros">
                    Zagueiro
                </option>

                <option value="atacantes">
                    Atacante
                </option>

            </select>

            <br><br>

            <button
                type="submit"
                style="font-size:24px; padding:14px;"
            >
                Salvar
            </button>

        </form>

    </body>

    </html>

    """

    return render_template_string(html)

@app.route("/excluir-jogador/<categoria>/<path:nome>")
def excluir_jogador(categoria, nome):

    dados = carregar_jogadores()

    dados[categoria].remove(nome)

    salvar_jogadores(dados)

    return redirect("/jogadores")

@app.route(
    "/editar-jogador/<categoria>/<path:nome>",
    methods=["GET", "POST"]
)
def editar_jogador(categoria, nome):

    dados = carregar_jogadores()

    if request.method == "POST":

        novo_nome = request.form["novo_nome"].strip()

        nova_categoria = request.form["nova_categoria"]


        dados[categoria].remove(nome)

        dados[nova_categoria].append(novo_nome)

        salvar_jogadores(dados)

        return redirect("/jogadores")


    html = """

    <html>

    <body style="font-family: Arial; text-align:center; padding:40px; font-size:26px;">

        <h1>Editar Jogador</h1>

        <form method="POST">

            <input
                type="text"
                name="novo_nome"
                value="{{ nome }}"
                style="font-size:24px; padding:10px;"
            >

            <br><br>

            <select
                name="nova_categoria"
                style="font-size:24px; padding:10px;"
            >

                <option
                    value="goleiros"
                    {% if categoria == "goleiros" %}
                        selected
                    {% endif %}
                >
                    Goleiro
                </option>

                <option
                    value="zagueiros"
                    {% if categoria == "zagueiros" %}
                        selected
                    {% endif %}
                >
                    Zagueiro
                </option>

                <option
                    value="atacantes"
                    {% if categoria == "atacantes" %}
                        selected
                    {% endif %}
                >
                    Atacante
                </option>

            </select>

            <br><br>

            <button
                type="submit"
                style="font-size:24px; padding:14px;"
            >
                Salvar alterações
            </button>

        </form>

    </body>

    </html>

    """

    return render_template_string(
        html,
        nome=nome,
        categoria=categoria
    )

@app.route(
    "/toggle-pagamento/<time>/<int:indice>"
)
def toggle_pagamento(time, indice):

    jogo = carregar_proximo_jogo()

    jogador = jogo[time][indice]

    jogador["pagou"] = not jogador["pagou"]

    salvar_proximo_jogo(jogo)

    return redirect("/proximo-jogo")

@app.route("/finalizar-jogo")
def finalizar_jogo():

    jogo = carregar_proximo_jogo()


    if not jogo:

        return """

        <h1>
            Não existe próximo jogo definido.
        </h1>

        <br>

        <a href="/">
            Voltar
        </a>

        """


    historico = carregar_historico()


    historico.insert(0, copy.deepcopy(jogo))


    with open(
        ARQUIVO_HISTORICO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            historico,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


    salvar_proximo_jogo({})


    return """

    <html>

    <body
        style="
            font-family: Arial;
            text-align: center;
            padding: 40px;
            font-size: 28px;
        "
    >

        <h1>
            ✅ Jogo movido para o histórico
        </h1>

        <br><br>

        <a href="/">

            <button
                style="
                    padding: 20px;
                    font-size: 24px;
                    cursor: pointer;
                "
            >
                Voltar ao menu
            </button>

        </a>

    </body>

    </html>

    """

@app.route("/limpar-proximo-jogo")
def limpar_proximo_jogo():

    salvar_proximo_jogo({})

    return """

    <html>

    <body
        style="
            font-family: Arial;
            text-align: center;
            padding: 40px;
            font-size: 28px;
        "
    >

        <h1>
            🗑️ Times descartados com sucesso
        </h1>

        <br><br>

        <a href="/">

            <button
                style="
                    padding: 20px;
                    font-size: 24px;
                    cursor: pointer;
                "
            >
                Voltar ao menu
            </button>

        </a>

    </body>

    </html>

    """


# ===================== EXECUÇÃO =====================

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )