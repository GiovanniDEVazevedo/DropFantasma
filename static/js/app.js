// =========================================
// INICIALIZAÇÃO
// =========================================

// Assim que a página carrega, buscamos os pontos atuais do jogador
document.addEventListener("DOMContentLoaded", () => {
    atualizarPontos();
    
    // Adiciona o evento de clique no botão "Ver coleção" que já existe no HTML
    const btnColecao = document.querySelector("#colecao button");
    if (btnColecao) {
        btnColecao.setAttribute("onclick", "verColecao()");
    }
});

// =========================================
// FUNÇÕES DE COMUNICAÇÃO COM A API (FLASK)
// =========================================

// Busca os pontos atuais ao carregar a página
async function atualizarPontos() {
    try {
        const resposta = await fetch("/colecao");
        const dados = await resposta.json();
        
        document.getElementById("pontos").innerText = dados.pontos || 0;
    } catch (erro) {
        console.error("Erro ao carregar pontos iniciais:", erro);
    }
}

// Roda quando clicamos em "Capturar Fantasma"
async function iniciarCaptura() {
    try {
        // Faz a requisição para a rota do Flask
        const resposta = await fetch("/capturar");
        const dados = await resposta.json();

        // 1. Atualiza a pontuação na tela principal
        document.getElementById("pontos").innerText = dados.pontos;

        // 2. Monta a mensagem de alerta para o usuário
        let mensagem = `👻 Você capturou: ${dados.fantasma.nome}!\n💎 Raridade: ${dados.fantasma.raridade}`;
        
        if (dados.duplicado) {
            mensagem += "\n\nVocê já tinha essa alma! Ela foi somada à sua coleção.";
        } else {
            mensagem += "\n\nNovo fantasma adicionado à sua coleção!";
        }

        alert(mensagem);

        // 3. Opcional: Se a coleção já estiver aberta na tela, atualiza ela na hora
        const divColecao = document.getElementById("colecao");
        if (divColecao.querySelector(".grid-fantasmas")) {
            verColecao();
        }

    } catch (erro) {
        console.error("Erro ao capturar fantasma:", erro);
        alert("Ocorreu um erro na conexão com o mundo espiritual. Tente novamente.");
    }
}

// Roda quando clicamos em "Ver coleção"
async function verColecao() {
    try {
        // Busca os dados da coleção no backend
        const resposta = await fetch("/colecao");
        const dados = await resposta.json();
        
        const divColecao = document.getElementById("colecao");
        
        // Limpa a div antes de recriar a lista, mantendo apenas o botão de atualizar
        divColecao.innerHTML = '<button onclick="verColecao()">Atualizar Coleção</button>';
        
        // Se o array de coleção estiver vazio
        if (!dados.colecao || dados.colecao.length === 0) {
            divColecao.innerHTML += "<p style='margin-top: 20px; color: #8b949e;'>Sua coleção de almas está vazia. Comece a caçar!</p>";
            return;
        }

        // Cria o container para a grade (grid) de cartas
        const grid = document.createElement("div");
        grid.className = "grid-fantasmas";

        // Passa por cada fantasma no array e cria o HTML dele
        dados.colecao.forEach(fantasma => {
            const card = document.createElement("div");
            
            // Garante que a classe vai bater com o CSS (comum, incomum, épico, lendário)
            const classeRaridade = fantasma.raridade.toLowerCase();
            card.className = `card-fantasma ${classeRaridade}`;
            
            // Preenche o conteúdo da carta
            card.innerHTML = `
                <img src="${fantasma.urlImagem}" alt="${fantasma.nome}" onerror="this.src='https://via.placeholder.com/120?text=?'">
                <h3>${fantasma.nome}</h3>
                <p class="raridade">${fantasma.raridade}</p>
                <p class="pontos-card">Valor: ${fantasma.pontos} pts</p>
                <p class="pontos-card">Quantidade: ${fantasma.quantidade || 1}</p>
            `;
            
            // Adiciona a carta na grade
            grid.appendChild(card);
        });

        // Adiciona a grade completa na tela
        divColecao.appendChild(grid);

    } catch (erro) {
        console.error("Erro ao carregar coleção:", erro);
        alert("Erro ao tentar acessar sua coleção de almas.");
    }
}