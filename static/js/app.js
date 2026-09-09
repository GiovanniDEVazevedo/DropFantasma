// =========================================
// INICIALIZAÇÃO
// =========================================

document.addEventListener("DOMContentLoaded", () => {
    atualizarPontos();

    const btnColecao = document.querySelector("#colecao button");
    if (btnColecao) {
        btnColecao.onclick = verColecao;
    }
});

// =========================================
// FUNÇÕES DE COMUNICAÇÃO COM A API
// =========================================

function escapeHtml(texto) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(texto));
    return div.innerHTML;
}

async function atualizarPontos() {
    try {
        const resposta = await fetch("/colecao");
        const dados = await resposta.json();
        document.getElementById("pontos").innerText = dados.pontos || 0;
    } catch (erro) {
        console.error("Erro ao carregar pontos:", erro);
    }
}

function mostrarModal(fantasma, duplicado) {
    document.getElementById("modal-imagem").src = fantasma.urlImagem;
    document.getElementById("modal-imagem").alt = fantasma.nome;
    document.getElementById("modal-mensagem").innerText = duplicado
        ? `Voce ja tinha essa alma!\nRaridade: ${fantasma.raridade}\nEla foi somada a sua colecao.`
        : `Novo fantasma capturado!\nRaridade: ${fantasma.raridade}\nEla foi adicionada a sua colecao.`;
    document.getElementById("modal-captura").classList.add("ativo");
}

function fecharModal() {
    document.getElementById("modal-captura").classList.remove("ativo");
}

const overlayModal = document.getElementById("modal-captura");
if (overlayModal) {
    overlayModal.addEventListener("click", function(evento) {
        if (evento.target === overlayModal) {
            fecharModal();
        }
    });
}

async function iniciarCaptura() {
    try {
        const resposta = await fetch("/capturar", { method: "POST" });
        const dados = await resposta.json();

        document.getElementById("pontos").innerText = dados.pontos;

        mostrarModal(dados.fantasma, dados.duplicado);

        const divColecao = document.getElementById("colecao");
        if (divColecao.querySelector(".grid-fantasmas")) {
            verColecao();
        }
    } catch (erro) {
        console.error("Erro ao capturar fantasma:", erro);
        alert("Erro na conexao. Tente novamente.");
    }
}

async function verColecao() {
    try {
        const resposta = await fetch("/colecao");
        const dados = await resposta.json();

        const divColecao = document.getElementById("colecao");
        divColecao.innerHTML = '<button onclick="verColecao()">Atualizar Colecao</button>';

        if (!dados.colecao || dados.colecao.length === 0) {
            divColecao.innerHTML += "<p style='margin-top: 20px; color: #8b949e;'>Sua colecao esta vazia. Comece a cacar!</p>";
            return;
        }

        const grid = document.createElement("div");
        grid.className = "grid-fantasmas";

        dados.colecao.forEach(fantasma => {
            const card = document.createElement("div");
            const classeRaridade = escapeHtml(fantasma.raridade.toLowerCase());
            card.className = `card-fantasma ${classeRaridade}`;

            const img = document.createElement("img");
            img.src = fantasma.urlImagem;
            img.alt = fantasma.nome;
            img.onerror = function() {
                this.style.display = "none";
            };

            const titulo = document.createElement("h3");
            titulo.textContent = fantasma.nome;

            const raridade = document.createElement("p");
            raridade.className = "raridade";
            raridade.textContent = fantasma.raridade;

            const pontos = document.createElement("p");
            pontos.className = "pontos-card";
            pontos.textContent = `Valor: ${fantasma.pontos} pts`;

            const qtd = document.createElement("p");
            qtd.className = "pontos-card";
            qtd.textContent = `Quantidade: ${fantasma.quantidade || 1}`;

            card.appendChild(img);
            card.appendChild(titulo);
            card.appendChild(raridade);
            card.appendChild(pontos);
            card.appendChild(qtd);
            grid.appendChild(card);
        });

        divColecao.appendChild(grid);

    } catch (erro) {
        console.error("Erro ao carregar colecao:", erro);
        alert("Erro ao acessar sua colecao.");
    }
}
