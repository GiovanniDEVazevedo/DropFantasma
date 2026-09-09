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

function mostrarModalFalha(fantasma) {
    document.getElementById("modal-imagem").style.display = "block";
    document.getElementById("modal-imagem").src = fantasma.urlImagem;
    document.getElementById("modal-imagem").alt = fantasma.nome;
    document.getElementById("modal-mensagem").innerText =
        `O fantasma escapou!\nRaridade: ${fantasma.raridade}\nTente novamente...`;
    document.getElementById("modal-captura").classList.add("ativo");
}

function mostrarModal(fantasma, duplicado) {
    document.getElementById("modal-imagem").style.display = "block";
    document.getElementById("modal-imagem").src = fantasma.urlImagem;
    document.getElementById("modal-imagem").alt = fantasma.nome;
    document.getElementById("modal-mensagem").innerText = duplicado
        ? `Voce ja tinha essa alma!\nRaridade: ${fantasma.raridade}\nEla foi somada a sua colecao.`
        : `Novo fantasma capturado!\nRaridade: ${fantasma.raridade}\nEla foi adicionada a sua colecao.`;
    document.getElementById("modal-captura").classList.add("ativo");
}

function mostrarModalTroca(trocados, pontosGanhos, pontosTotais) {
    document.getElementById("modal-imagem").style.display = "none";
    document.getElementById("modal-mensagem").innerText = trocados > 0
        ? `Voce trocou ${trocados} fantasma(s) repetido(s)!\nGanhou ${pontosGanhos} pontos.\nSaldo atual: ${pontosTotais} pontos.`
        : `Nenhum fantasma repetido para trocar.\nSaldo atual: ${pontosTotais} pontos.`;
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

        if (dados.capturado) {
            mostrarModal(dados.fantasma, dados.duplicado);
        } else {
            mostrarModalFalha(dados.fantasma);
        }

        const divColecao = document.getElementById("colecao");
        if (divColecao.querySelector(".grid-fantasmas")) {
            verColecao();
        }
    } catch (erro) {
        console.error("Erro ao capturar fantasma:", erro);
        alert("Erro na conexao. Tente novamente.");
    }
}

async function abrirMercado() {
    try {
        const resposta = await fetch("/mercado");
        const dados = await resposta.json();

        document.getElementById("mercado-pontos").innerText =
            `Saldo: ${dados.pontos} pontos`;

        const lista = document.getElementById("mercado-lista");
        lista.innerHTML = "";

        dados.itens.forEach(item => {
            const card = document.createElement("div");
            card.className = "mercado-item";

            const info = document.createElement("div");
            info.className = "mercado-info";

            const nome = document.createElement("p");
            nome.className = "mercado-nome";
            nome.textContent = `${item.nome} - ${item.preco} pts`;

            const descricao = document.createElement("p");
            descricao.className = "mercado-descricao";
            descricao.textContent = item.descricao;

            const estoque = document.createElement("p");
            estoque.className = "mercado-estoque";
            estoque.textContent = `Voce tem: ${dados.inventario[item.id] || 0}`;

            info.appendChild(nome);
            info.appendChild(descricao);
            info.appendChild(estoque);

            const btn = document.createElement("button");
            btn.textContent = "Comprar";
            btn.onclick = () => comprarItem(item.id);

            card.appendChild(info);
            card.appendChild(btn);
            lista.appendChild(card);
        });

        document.getElementById("modal-mercado").classList.add("ativo");
    } catch (erro) {
        console.error("Erro ao abrir mercado:", erro);
        alert("Erro ao acessar o mercado.");
    }
}

function fecharMercado() {
    document.getElementById("modal-mercado").classList.remove("ativo");
}

const overlayMercado = document.getElementById("modal-mercado");
if (overlayMercado) {
    overlayMercado.addEventListener("click", function(evento) {
        if (evento.target === overlayMercado) {
            fecharMercado();
        }
    });
}

async function comprarItem(itemId) {
    try {
        const resposta = await fetch("/comprar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item: itemId })
        });
        const dados = await resposta.json();

        if (resposta.status === 400) {
            alert(dados.erro);
            return;
        }

        document.getElementById("pontos").innerText = dados.pontos;
        abrirMercado();
    } catch (erro) {
        console.error("Erro ao comprar item:", erro);
        alert("Erro na conexao. Tente novamente.");
    }
}

async function trocarRepetidos() {
    try {
        const resposta = await fetch("/trocar", { method: "POST" });
        const dados = await resposta.json();

        document.getElementById("pontos").innerText = dados.pontos;
        mostrarModalTroca(dados.trocados, dados.pontos_ganhos, dados.pontos);

        const divColecao = document.getElementById("colecao");
        if (divColecao.querySelector(".grid-fantasmas")) {
            verColecao();
        }
    } catch (erro) {
        console.error("Erro ao trocar repetidos:", erro);
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
