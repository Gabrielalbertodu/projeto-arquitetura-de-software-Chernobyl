# Simulação de Monitoramento e Segurança do Reator — Caso Chernobyl

## Descrição

Este projeto apresenta uma **simulação em Python** de um sistema de monitoramento e resposta a incidentes em um ambiente crítico, inspirado na análise arquitetural do desastre de Chernobyl.

A proposta do sistema é demonstrar, de forma didática, como uma arquitetura moderna pode:

- monitorar leituras de sensores;
- validar limites operacionais de segurança;
- emitir alertas críticos;
- registrar incidentes em log;
- interromper automaticamente procedimentos inseguros.

O foco do projeto não está em reproduzir o desastre real, mas em **simular uma solução arquitetural mais segura**, alinhada aos princípios estudados em **Arquitetura de Software**. 

---

## Objetivo

Demonstrar, por meio de uma implementação parcial e simulada, como um sistema arquitetado com separação de responsabilidades, validação de segurança e tratamento orientado a eventos pode reduzir riscos operacionais em sistemas críticos. 

---

## Funcionalidades

- Simulação de leituras de sensores de:
  - temperatura
  - pressão
  - potência
- Validação automática de limites seguros
- Geração de alerta crítico quando há violação
- Registro do incidente em arquivo JSON
- Bloqueio automático da continuação do teste
- Organização do fluxo com componentes desacoplados

---

## Estrutura Arquitetural da Simulação

O código foi organizado em componentes com responsabilidades específicas:

### `SimuladorSensores`
Responsável por gerar leituras simuladas dos sensores.

### `ValidadorSeguranca`
Compara as leituras com os limites definidos como seguros.

### `RespostaEmergencialPadrao`
Define a ação executada quando uma condição insegura é detectada.

### `BarramentoEventos`
Publica incidentes para os ouvintes cadastrados, permitindo comunicação orientada a eventos.

### `CentralAlertas`
Exibe o alerta crítico no terminal.

### `RegistroIncidentes`
Salva os incidentes detectados em um arquivo `incident_log.json`.

### `OrquestradorTeste`
Coordena toda a execução da simulação, desde o início do teste até a interrupção em caso de incidente.

---

## Padrões e Conceitos Aplicados

Este projeto utiliza conceitos compatíveis com a proposta arquitetural do trabalho acadêmico:

- **Strategy**: usado para definir a resposta ao incidente por meio da estratégia `RespostaEmergencialPadrao`
- **Observer / Event-driven**: usado no `BarramentoEventos`, que notifica os ouvintes inscritos
- **Separação de responsabilidades**: cada classe possui uma função bem definida
- **Auditabilidade**: incidentes são registrados em arquivo JSON
- **Fail-safe**: ao detectar condição insegura, o sistema interrompe imediatamente a operação 

---

## Tecnologias Utilizadas

- **Python 3.10+**
- Biblioteca padrão do Python:
  - `json`
  - `dataclasses`
  - `datetime`
  - `pathlib`
  - `typing`

Não há dependências externas.

---

## Estrutura do Projeto

```bash
.
├── chernobyl_simulacao.py
├── classes.py 
├── incident_log.json   # gerado automaticamente após a execução
└── README.md