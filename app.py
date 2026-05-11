from flask import Flask, request, render_template_string
import random
import json

app = Flask(__name__)

# ===================== HISTÓRICO =====================

ARQUIVO_HISTORICO = "historico.json"


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


def salvar_historico(time_1, time_2, data_jogo):

    historico = carregar_historico()

    novo_jogo = {

        "data": data_jogo,

        "time_1": time_1,

        "time_2": time_2
    }

    historico.insert(0, novo_jogo)

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


# ===================== DADOS =====================

goleiros = ["Júlio", "Fernando", "Júnior"]

zagueiros = [
    "Wellinton",
    "Airton",
    "Fabricio",
    "Diogo",
    "Roberson"
]

atacantes = [
    "Daniel",
    "Henry",
    "Du",
    "Hudson",
    "Dênis",
    "Lucas",
    "Scott",
    "Caio",
    "Val",
    "Renan",
    "Hermes",
    "Douglas"
]


# ===================== MENU =====================

@app.route("/")
def index():

    html = """

    <html>

    <head>

        <title>FutSábado</title>

        <style>

            body {
                font-family: Arial;
                padding: 30px;
            }

            h1 {
                color: #222;
            }

            button {
                width: 250px;
                padding: 15px;
                margin-top: 15px;
                font-size: 16px;
                cursor: pointer;
            }

        </style>

    </head>

    <body>

        <h1>FutSábado</h1>

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

    html = """

    <html>

    <head>

        <title>Sorteador de Times</title>

        <style>

            body {
                font-family: Arial;
                padding: 20px;
            }

            h1 {
                color: #222;
            }

            h2 {
                margin-top: 30px;
            }

            button {
                margin-top: 30px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
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

                <input
                    type="checkbox"
                    name="goleiros"
                    value="{{ jogador }}"
                    class="goleiro"
                >

                {{ jogador }}

                <br>

            {% endfor %}



            <h2>Zagueiros</h2>

            {% for jogador in zagueiros %}

                <input
                    type="checkbox"
                    name="zagueiros"
                    value="{{ jogador }}"
                    class="jogador"
                >

                {{ jogador }}

                <br>

            {% endfor %}



            <h2>Atacantes</h2>

            {% for jogador in atacantes %}

                <input
                    type="checkbox"
                    name="atacantes"
                    value="{{ jogador }}"
                    class="jogador"
                >

                {{ jogador }}

                <br>

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


    # ===================== GOLEIROS =====================

    goleiros_sorteio = goleiros_jogando.copy()

    goleiro_sorteado = random.choice(
        goleiros_sorteio
    )

    time_1.append(goleiro_sorteado)

    goleiros_sorteio.remove(goleiro_sorteado)

    time_2.append(goleiros_sorteio[0])


    # ===================== ZAGUEIROS =====================

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


    # ===================== ATACANTES =====================

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


    # ===================== RESULTADO =====================

    html_resultado = """

    <html>

    <head>

        <title>Times Sorteados</title>

        <style>

            body {
                font-family: Arial;
                padding: 20px;
            }

            .times {
                display: flex;
                gap: 60px;
            }

            button {
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
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

        <a href="/sortear-times">

            <button>
                Fazer novo sorteio
            </button>

        </a>

        <br><br>

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

        <br><br>

        <a href="/">
            Voltar ao menu
        </a>

    </body>

    </html>

    """

    return render_template_string(
        html_resultado,
        time_1=time_1,
        time_2=time_2
    )


# ===================== SALVAR PRÓXIMO JOGO =====================

@app.route(
    "/salvar-proximo-jogo",
    methods=["POST"]
)
def salvar_proximo_jogo():

    time_1 = json.loads(
        request.form["time_1"]
    )

    time_2 = json.loads(
        request.form["time_2"]
    )


    proximo_sabado = "16/05/2026"


    salvar_historico(
        time_1,
        time_2,
        proximo_sabado
    )


    return """

    <h1>

        Próximo jogo salvo com sucesso.

    </h1>

    <br>

    <a href='/'>
        Voltar ao menu
    </a>

    """


# ===================== PRÓXIMO JOGO =====================

@app.route("/proximo-jogo")
def proximo_jogo():

    historico = carregar_historico()

    if not historico:

        return """

        <h1>
            Nenhum próximo jogo definido.
        </h1>

        <br>

        <a href="/">
            Voltar
        </a>

        """

    jogo = historico[0]

    html = """

    <html>

    <head>

        <title>Próximo Jogo</title>

        <style>

            body {
                font-family: Arial;
                padding: 20px;
            }

            .times {
                display: flex;
                gap: 60px;
            }

            .pagar {
                cursor: pointer;
                color: red;
                font-weight: bold;
                margin-left: 8px;
                font-size: 18px;
            }

            .pago {
                color: green;
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

                            {{ jogador }}

                            <span
                                class="pagar"
                                title="Sinalizar pagamento da quadra"
                            >
                                $
                            </span>

                        </li>

                    {% endfor %}

                </ul>

            </div>



            <div>

                <h2>Time 2</h2>

                <ul>

                    {% for jogador in jogo.time_2 %}

                        <li>

                            {{ jogador }}

                            <span
                                class="pagar"
                                title="Sinalizar pagamento da quadra"
                            >
                                $
                            </span>

                        </li>

                    {% endfor %}

                </ul>

            </div>

        </div>

        <br>

        <a href="/">
            Voltar
        </a>


        <script>

        const botoesPagamento =
            document.querySelectorAll(
                '.pagar'
            )

        botoesPagamento.forEach(botao => {

            botao.addEventListener(
                'click',
                () => {

                    botao.classList.toggle(
                        'pago'
                    )
                }
            )
        })

        </script>

    </body>

    </html>

    """

    return render_template_string(
        html,
        jogo=jogo
    )


# ===================== HISTÓRICO =====================

@app.route("/historico")
def historico():

    historico = carregar_historico()

    html = """

    <html>

    <head>

        <title>Jogos Anteriores</title>

        <style>

            body {
                font-family: Arial;
                padding: 20px;
            }

            .jogo {
                margin-bottom: 40px;
            }

        </style>

    </head>

    <body>

        <h1>Jogos Anteriores</h1>

        {% for jogo in historico[1:] %}

            <div class="jogo">

                <h3>
                    {{ jogo.data }}
                </h3>

                <b>Time 1:</b>

                {{ jogo.time_1 | join(', ') }}

                <br><br>

                <b>Time 2:</b>

                {{ jogo.time_2 | join(', ') }}

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

    html = """

    <html>

    <head>

        <title>Jogadores</title>

        <style>

            body {
                font-family: Arial;
                padding: 20px;
            }

        </style>

    </head>

    <body>

        <h1>Jogadores Cadastrados</h1>

        <h2>Goleiros</h2>

        <ul>

            {% for jogador in goleiros %}

                <li>{{ jogador }}</li>

            {% endfor %}

        </ul>



        <h2>Zagueiros</h2>

        <ul>

            {% for jogador in zagueiros %}

                <li>{{ jogador }}</li>

            {% endfor %}

        </ul>



        <h2>Atacantes</h2>

        <ul>

            {% for jogador in atacantes %}

                <li>{{ jogador }}</li>

            {% endfor %}

        </ul>

        <br>

        <a href="/">
            Voltar
        </a>

    </body>

    </html>

    """

    return render_template_string(
        html,
        goleiros=goleiros,
        zagueiros=zagueiros,
        atacantes=atacantes
    )


# ===================== EXECUÇÃO =====================

if __name__ == "__main__":
    app.run(debug=True)