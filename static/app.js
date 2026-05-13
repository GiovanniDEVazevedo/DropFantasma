// =========================
// INICIAR CAPTURA
// =========================

async function iniciarCaptura() {

    try {

        const resposta =
            await fetch("http://127.0.0.1:5000/capturar");

        const dados =
            await resposta.json();

        const fantasma =
            dados.fantasma;

        console.log(fantasma);

     
       

        document.querySelector(".ar-header h3")
            .innerText =
            `${fantasma.nome} Capturado!`;

        await abrirAR(fantasma.urlImagem);

    } catch (erro) {

        console.error(erro);

        alert("Erro ao capturar fantasma");
    }
}


// =========================
// ABRIR AR
// =========================

let streamDaCamera = null;

async function abrirAR(urlDaImagem) {

    const arContainer =
        document.getElementById("ar-container");

    const arVideo =
        document.getElementById("ar-video");

    const arGhostImg =
        document.getElementById("ar-ghost-img");

    arGhostImg.src = urlDaImagem;

    arContainer.classList.remove("escondido");

    try {

        const stream =
            await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: "environment"
                }
            });

        streamDaCamera = stream;

        arVideo.srcObject = stream;

    } catch (erro) {

        console.error(erro);

        alert("Erro ao acessar câmera");

        fecharAR();
    }
}


// =========================
// FECHAR AR
// =========================

function fecharAR() {

    const arContainer =
        document.getElementById("ar-container");

    const arVideo =
        document.getElementById("ar-video");

    arContainer.classList.add("escondido");

    if (streamDaCamera) {

        streamDaCamera
            .getTracks()
            .forEach(track => track.stop());

        streamDaCamera = null;
    }

    arVideo.srcObject = null;
}


// =========================
// CARREGAR COLEÇÃO
// =========================

async function carregarColecao() {

    const resposta =
        await fetch("http://127.0.0.1:5000/colecao");

    const dados =
        await resposta.json();

    const divColecao =
        document.getElementById("colecao");

    divColecao.innerHTML = "";

    dados.colecao.forEach(fantasma => {

        divColecao.innerHTML += `
        
        <div class="card-fantasma">
        
            <img 
                src="${fantasma.urlImagem}" 
                width="150"
            >

            <h3>${fantasma.nome}</h3>

            <p>${fantasma.raridade}</p>

        </div>
        `;
    });
}