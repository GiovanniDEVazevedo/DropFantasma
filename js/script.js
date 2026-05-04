const bancoDeFantasmas = [
    { 
        nome: "Fantasma Comum", 
        chance: 50, 
        raridade: "Comum",
        urlImagem: "./img/fantasma-comum.png" 
    },
    { 
        nome: "Fantasma Incomum (Gravata)", 
        chance: 25, 
        raridade: "Incomum",
        urlImagem: "./img/fantasma-incomum.png" 
    },
    { 
        nome: "Fantasma Épico (Ceifador)", 
        chance: 8, 
        raridade: "Épico",
        urlImagem: "./img/fantasma-epico.png" 
    },
    { 
        nome: "Lorde Fantasma (Lendário)", 
        chance: 2, 
        raridade: "Lendário",
        urlImagem: "./img/fantasma-lendario.png" 
    }
    // ... manter os outros conforme a nova tabela acima
];
// Variável global para a câmera
let streamDaCamera = null;

// 2. A Função que faz o sorteio matemático
function sortearPersonagem() {
    // Sorteia um número decimal de 0 até 100
    const numeroSorteado = Math.random() * 100;
    
    let chanceAcumulada = 0;

    // Passa por cada fantasma no JSON
    for (let i = 0; i < bancoDeFantasmas.length; i++) {
        const fantasmaAtual = bancoDeFantasmas[i];
        
        // Empilha a chance
        chanceAcumulada += fantasmaAtual.chance;

        // Se o número sorteado for menor ou igual à chance acumulada, este é o vencedor!
        if (numeroSorteado <= chanceAcumulada) {
            return fantasmaAtual;
        }
    }
}

// 3. A Função principal acionada pelo botão
async function iniciarCaptura() {
    // Faz o sorteio
    const personagemSorteado = sortearPersonagem();
    
    // Mostra no console para você conferir quem saiu
    console.log(`Você tirou: ${personagemSorteado.nome} (${personagemSorteado.raridade})`);
    
    // Atualiza o texto do header do AR com o nome e raridade
    document.querySelector('.ar-header h3').innerText = `${personagemSorteado.nome} Capturado!`;

    // Chama a função de AR passando a URL sorteada
    await abrirAR(personagemSorteado.urlImagem);
}

// 4. A Função de AR (que você já tinha)
async function abrirAR(urlDaImagem) {
    const arContainer = document.getElementById('ar-container');
    const arVideo = document.getElementById('ar-video');
    const arGhostImg = document.getElementById('ar-ghost-img');

    // Define a imagem baseada no sorteio
    arGhostImg.src = urlDaImagem;
    arContainer.classList.remove('escondido');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { 
                facingMode: 'environment',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        });
        streamDaCamera = stream;
        arVideo.srcObject = stream;
    } catch (erro) {
        console.error('Erro ao acessar a câmera:', erro);
        alert('Não foi possível acessar a câmera.');
        fecharAR();
    }
}

function fecharAR() {
    const arContainer = document.getElementById('ar-container');
    const arVideo = document.getElementById('ar-video');

    arContainer.classList.add('escondido');

    if (streamDaCamera) {
        streamDaCamera.getTracks().forEach(track => track.stop());
        streamDaCamera = null;
    }
    arVideo.srcObject = null;
}