## 🚀 Funcionalidades

- **Sistema de Drops Dinâmico**: Sorteio de personagens baseado em probabilidades de raridade.
- **Visualização em AR**: Veja seu fantasma no mundo real através da câmera do celular (Fallback Web AR).
- **Lógica de Cooldown**: Sistema de espera de 2 horas entre capturas para garantir o engajamento.(desenvolvimento)
- **Geração por IA**: Personagens e acessórios gerados via Nano Banana com camadas de personalização.(desenvolvimento)

## 📊 Tabela de Raridades

| Nível | Chance | Acessórios | Estética |
| :--- | :--- | :--- | :--- |
| **Comum** | 50% | Base | Chibi simples e fofo |
| **Incomum** | 25% | 1 Item | Detalhes como gravatas ou laços |
| **Raro** | 15% | 2 Itens | Chapéus e varinhas mágicas |
| **Épico** | 8% | 3 Itens | Mini-foices e chamas de alma |
| **Lendário** | 2% | 4 Itens | Aura dourada e a Lua icônica |

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3 (Animações @keyframes) e Vanilla JavaScript.
- **Backend**: Python com Flask (Controle de API e Cooldown).(desenvolvimento)
- **Processamento de Imagem**: Pillow (PIL) para montagem dinâmica das camadas PNG.
- **Câmera**: API `getUserMedia` para integração de Realidade Aumentada no navegador.

## 📂 Estrutura do Projeto

```text

├── index.html          # Interface principal e container de vídeo
├── style.css           # Estilização e animações de flutuação
├── script.js           # Lógica de sorteio, probabilidade e acesso à câmera

