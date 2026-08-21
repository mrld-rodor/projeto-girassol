// ============================================================
// DADOS DOS SERVIÇOS (APENAS UMA VEZ)
// ============================================================
const servicesData = {
    cristaloterapia: {
        nome: "Cristaloterapia",
        resumo: "A Cristaloterapia é uma terapia integrativa que utiliza a energia dos cristais para harmonizar os centros energéticos do corpo, promovendo equilíbrio físico, emocional e espiritual.",
        objetivo: "Auxiliar na redução do estresse, ansiedade, cansaço e no fortalecimento da energia vital.",
        comoFunciona: "No Espaço Girassol, o atendimento é personalizado, com a escolha dos cristais de acordo com as necessidades de cada pessoa.",
        duracao: "Aproximadamente 60 minutos.",
        formato: "Presencial",
        paraQuem: "Pessoas que buscam equilíbrio energético, redução do estresse e bem-estar geral.",
        cuidados: "Não há contraindicações, mas recomenda-se informar ao terapeuta sobre condições de saúde pré-existentes."
    },
    radiestesia: {
        nome: "Radiestesia",
        resumo: "A Radiestesia é uma terapia integrativa que utiliza instrumentos como o pêndulo para identificar e avaliar desequilíbrios energéticos, auxiliando na harmonização do corpo, da mente e das emoções.",
        objetivo: "Promover autoconhecimento, equilíbrio energético e bem-estar.",
        comoFunciona: "No Espaço Girassol, o atendimento é personalizado, com uma avaliação energética para direcionar o tratamento de acordo com as necessidades de cada pessoa.",
        duracao: "Aproximadamente 60 minutos.",
        formato: "Presencial",
        paraQuem: "Pessoas que desejam autoconhecimento, equilíbrio energético e harmonização.",
        cuidados: "Não há contraindicações, mas recomenda-se informar ao terapeuta sobre condições de saúde pré-existentes."
    },
    reiki: {
        nome: "Reiki",
        resumo: "O Reiki é uma terapia integrativa de origem japonesa que promove o equilíbrio energético por meio da imposição das mãos.",
        objetivo: "Auxiliar na redução do estresse, ansiedade, dores, fadiga e favorecer o relaxamento profundo, o bem-estar e o fortalecimento da energia vital.",
        comoFunciona: "No Espaço Girassol, cada atendimento é realizado de forma personalizada, respeitando as necessidades físicas, emocionais e energéticas de cada pessoa.",
        duracao: "Aproximadamente 60 minutos.",
        formato: "Presencial",
        paraQuem: "Pessoas que buscam relaxamento, redução do estresse e equilíbrio energético.",
        cuidados: "Não há contraindicações, mas recomenda-se informar ao terapeuta sobre condições de saúde pré-existentes."
    },
    florais: {
        nome: "Florais",
        resumo: "A Terapia Floral utiliza essências naturais para promover o equilíbrio emocional e auxiliar no enfrentamento de sentimentos como ansiedade, estresse, medo, tristeza e insegurança.",
        objetivo: "Favorecer o autoconhecimento e o bem-estar através de uma abordagem suave e natural.",
        comoFunciona: "No Espaço Girassol, o atendimento é personalizado, com uma avaliação para indicar a combinação de florais mais adequada às necessidades de cada pessoa.",
        duracao: "Aproximadamente 60 minutos.",
        formato: "Presencial",
        paraQuem: "Pessoas que buscam equilíbrio emocional, autoconhecimento e bem-estar.",
        cuidados: "Não há contraindicações, mas recomenda-se informar ao terapeuta sobre condições de saúde pré-existentes."
    },
    taro: {
        nome: "Tarô Terapêutico",
        resumo: "O Tarô Terapêutico é uma ferramenta de autoconhecimento que auxilia na compreensão de desafios, emoções e padrões de comportamento.",
        objetivo: "Promover clareza, reflexão e apoio na tomada de decisões, favorecendo o desenvolvimento pessoal e o equilíbrio emocional.",
        comoFunciona: "No Espaço Girassol, o atendimento é realizado de forma acolhedora e personalizada, respeitando o momento e as necessidades de cada pessoa.",
        duracao: "Aproximadamente 60 minutos.",
        formato: "Presencial",
        paraQuem: "Pessoas que buscam autoconhecimento, clareza e equilíbrio emocional.",
        cuidados: "Não há contraindicações, mas recomenda-se informar ao terapeuta sobre condições de saúde pré-existentes."
    },
    arteterapia: {
        nome: "Arteterapia",
        resumo: "A Arteterapia é uma prática integrativa que utiliza a expressão artística como instrumento de autoconhecimento, equilíbrio emocional e desenvolvimento pessoal.",
        objetivo: "Auxiliar na redução do estresse, da ansiedade e no fortalecimento da autoestima.",
        comoFunciona: "No Espaço Girassol, o atendimento é personalizado, respeitando o tempo e a individualidade de cada pessoa.",
        duracao: "Aproximadamente 60 minutos.",
        formato: "Presencial",
        paraQuem: "Pessoas que buscam expressão criativa, autoconhecimento e equilíbrio emocional.",
        cuidados: "Não há contraindicações, mas recomenda-se informar ao terapeuta sobre condições de saúde pré-existentes."
    },
    eft: {
        nome: "EFT – Técnica de Libertação Emocional",
        resumo: "A EFT (Emotional Freedom Techniques) é uma terapia integrativa que combina estímulos em pontos energéticos do corpo com técnicas de foco emocional.",
        objetivo: "Auxiliar na liberação de bloqueios, redução da ansiedade, estresse, medos e emoções negativas.",
        comoFunciona: "No Espaço Girassol, o atendimento é personalizado, proporcionando acolhimento e equilíbrio emocional de forma natural e segura.",
        duracao: "Aproximadamente 30 minutos.",
        formato: "Presencial",
        paraQuem: "Pessoas que buscam liberar bloqueios emocionais, reduzir ansiedade e estresse.",
        cuidados: "Não há contraindicações, mas recomenda-se informar ao terapeuta sobre condições de saúde pré-existentes."
    }
};

// ============================================================
// LÓGICA DO MODAL
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('service-modal');
    const modalBody = document.getElementById('modal-body');
    const modalClose = document.getElementById('modal-close');
    const modalOverlay = document.getElementById('modal-overlay');
    const modalContactBtn = document.getElementById('modal-contact-btn');

    if (!modal) {
        console.error("ERRO: Modal não encontrado!");
        return;
    }

    let closingTimeout = null; // Variável para controlar o timeout

    function openModal(serviceKey) {
        // Limpa timeout pendente de fechamento
        if (closingTimeout) {
            clearTimeout(closingTimeout);
            closingTimeout = null;
        }

        const data = servicesData[serviceKey];
        if (!data) return;

        modalBody.innerHTML = `
            <h3>${data.nome}</h3>
            <p class="sg-service-summary-modal">${data.resumo}</p>
            
            <div class="sg-service-detail">
                <strong>Objetivo de bem-estar</strong>
                <p>${data.objetivo}</p>
            </div>
            
            <div class="sg-service-detail">
                <strong>Como funciona</strong>
                <p>${data.comoFunciona}</p>
            </div>
            
            <div class="sg-service-detail">
                <strong>Duração aproximada</strong>
                <p>${data.duracao}</p>
            </div>
            
            <div class="sg-service-detail">
                <strong>Formato</strong>
                <p>${data.formato}</p>
            </div>
            
            <div class="sg-service-detail">
                <strong>Para quem pode ser indicado</strong>
                <p>${data.paraQuem}</p>
            </div>
            
            <div class="sg-service-detail">
                <strong>Cuidados e contraindicações</strong>
                <p>${data.cuidados}</p>
            </div>
        `;

        modalContactBtn.dataset.service = serviceKey;
        modalContactBtn.textContent = `Pedir informações sobre ${data.nome}`;

        modal.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        // Limpa qualquer timeout pendente
        if (closingTimeout) {
            clearTimeout(closingTimeout);
            closingTimeout = null;
        }

        modal.classList.remove('visible');
        modal.classList.remove('closing');
        document.body.style.overflow = '';
    }

    document.querySelectorAll('.sg-service-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const service = this.dataset.service;
            openModal(service);
        });
    });

    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('visible')) {
            closeModal();
        }
    });

    modalContactBtn.addEventListener('click', function() {
        const service = this.dataset.service;
        const data = servicesData[service];
        
        closeModal();
        
        // CORREÇÃO: 'contacto' em vez de 'contato'
        const contactSection = document.getElementById('contacto');
        if (contactSection) {
            contactSection.scrollIntoView({ behavior: 'smooth' });
            
            const interesseField = document.getElementById('interesse');
            if (interesseField && data) {
                interesseField.value = data.nome;
            }
        }
    });
});