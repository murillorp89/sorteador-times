from flask import Flask, request, render_template_string
import random

app = Flask(__name__)


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


# ===================== PÁGINA INICIAL =====================

@app.route("/")
def index():

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
                >

                {{ jogador }}

                <br>

            {% endfor %}



            <button type="submit">
                Sortear Times
            </button>

        </form>

    </body>

    </html>

    """

    return render_template_string(
        html,
        goleiros=goleiros,
        zagueiros=zagueiros,
        atacantes=atacantes
    )


# ===================== SORTEIO =====================

@app.route("/sortear", methods=["POST"])
def sortear():

    goleiros_jogando = request.form.getlist("goleiros")

    zagueiros_jogando = request.form.getlist("zagueiros")

    atacantes_jogando = request.form.getlist("atacantes")



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

        <a href="/">
        Voltar
        </a>
        """



    if len(todos_jogando) != 14:

        return """
        <h1>Erro</h1>

        <p>
        Você precisa selecionar exatamente 14 jogadores.
        </p>

        <a href="/">
        Voltar
        </a>
        """



    time_1 = []
    time_2 = []



    # ===================== GOLEIROS =====================

    goleiros_sorteio = goleiros_jogando.copy()

    goleiro_sorteado = random.choice(goleiros_sorteio)

    time_1.append(goleiro_sorteado)

    goleiros_sorteio.remove(goleiro_sorteado)

    time_2.append(goleiros_sorteio[0])



    # ===================== ZAGUEIROS =====================

    zagueiros_sorteio = zagueiros_jogando.copy()

    while zagueiros_sorteio:

        sorteado = random.choice(zagueiros_sorteio)

        zagueiros_sorteio.remove(sorteado)

        if len(time_1) <= len(time_2):

            time_1.append(sorteado)

        else:

            time_2.append(sorteado)



    # ===================== ATACANTES =====================

    atacantes_sorteio = atacantes_jogando.copy()

    while len(time_1) < 7 or len(time_2) < 7:

        sorteado = random.choice(atacantes_sorteio)

        atacantes_sorteio.remove(sorteado)

        if len(time_1) <= len(time_2):

            time_1.append(sorteado)

        else:

            time_2.append(sorteado)



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

        <a href="/">
            Fazer novo sorteio
        </a>

    </body>

    </html>

    """



    return render_template_string(
        html_resultado,
        time_1=time_1,
        time_2=time_2
    )



# ===================== EXECUÇÃO =====================

if __name__ == "__main__":
    app.run(debug=True)