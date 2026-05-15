// =========================
// static/js/app.js
// =========================

async function iniciarCaptura() {

    const resposta =
        await fetch("/capturar");

    const dados =
        await resposta.json();

    const fantasma =
        dados.fantasma;

    document
        .getElementById("pontos")
        .innerText =
        dados.pontos;

    if (dados.duplicado) {

    

    } else {

        alert(
            `${fantasma.nome} capturado!`
        );
    }

    carregarColecao();
}


async function carregarColecao() {

    const resposta =
        await fetch("/colecao");

    const dados =
        await resposta.json();

    const colecao =
        document.getElementById(
            "colecao"
        );

    colecao.innerHTML = "";

    dados.colecao.forEach(fantasma => {

        colecao.innerHTML += `

        <div>

            <img
                src="${fantasma.urlImagem}"
                width="120"
            >

            <h3>${fantasma.nome}</h3>

            <p>${fantasma.raridade}</p>

        </div>
        `;
    });
}


carregarColecao();