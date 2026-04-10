
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Protocol




LIMITES_SEGUROS = {
    "temperatura": 700,
    "pressao": 100,
    "potencia": 80,
}

@dataclass
class LeituraSensor:
    instante: str
    temperatura: float
    pressao: float
    potencia: float


@dataclass
class Incidente:
    instante: str
    severidade: str
    motivo: str
    leitura: Dict[str, float]
    acao: str


class OuvinteEvento(Protocol):
    def notificar(self, incidente: Incidente) -> None:
        ...


class CentralAlertas:
    def notificar(self, incidente: Incidente) -> None:
        print("\n[ALERTA CRITICO]")
        print(f"Severidade: {incidente.severidade}")
        print(f"Motivo: {incidente.motivo}")
        print(f"Acao: {incidente.acao}")


class RegistroIncidentes:
    def __init__(self, caminho_arquivo: str = "incident_log.json") -> None:
        self.caminho = Path(caminho_arquivo)

    def notificar(self, incidente: Incidente) -> None:
        historico = []
        if self.caminho.exists():
            try:
                historico = json.loads(self.caminho.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                historico = []
        historico.append(asdict(incidente))
        self.caminho.write_text(
            json.dumps(historico, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Incidente registrado em: {self.caminho.resolve()}")


class EstrategiaResposta(Protocol):
    def executar(self, leitura: LeituraSensor, motivo: str) -> Incidente:
        ...


class RespostaEmergencialPadrao:
    def executar(self, leitura: LeituraSensor, motivo: str) -> Incidente:
        return Incidente(
            instante=leitura.instante,
            severidade="alta",
            motivo=motivo,
            leitura={
                "temperatura": leitura.temperatura,
                "pressao": leitura.pressao,
                "potencia": leitura.potencia,
            },
            acao="Teste interrompido e protocolo de emergencia acionado.",
        )


class ValidadorSeguranca:
    def __init__(self, limites: Dict[str, float], estrategia: EstrategiaResposta) -> None:
        self.limites = limites
        self.estrategia = estrategia

    def validar(self, leitura: LeituraSensor) -> Incidente | None:
        violacoes: List[str] = []

        if leitura.temperatura > self.limites["temperatura"]:
            violacoes.append(
                f"Temperatura acima do limite ({leitura.temperatura} > {self.limites['temperatura']})"
            )
        if leitura.pressao > self.limites["pressao"]:
            violacoes.append(
                f"Pressao acima do limite ({leitura.pressao} > {self.limites['pressao']})"
            )
        if leitura.potencia > self.limites["potencia"]:
            violacoes.append(
                f"Potencia acima do limite ({leitura.potencia} > {self.limites['potencia']})"
            )

        if not violacoes:
            return None

        motivo = " | ".join(violacoes)
        return self.estrategia.executar(leitura, motivo)


class BarramentoEventos:
    def __init__(self) -> None:
        self.ouvintes: List[OuvinteEvento] = []

    def inscrever(self, ouvinte: OuvinteEvento) -> None:
        self.ouvintes.append(ouvinte)

    def publicar(self, incidente: Incidente) -> None:
        for ouvinte in self.ouvintes:
            ouvinte.notificar(incidente)


class SimuladorSensores:
    def gerar_leituras(self) -> List[LeituraSensor]:
        agora = datetime.now()
        dados = [
            (620, 82, 52),
            (655, 87, 60),
            (690, 94, 74),
            (735, 108, 91),
        ]
        leituras: List[LeituraSensor] = []
        for indice, (temperatura, pressao, potencia) in enumerate(dados, start=1):
            instante = agora.replace(microsecond=0).isoformat()
            leituras.append(
                LeituraSensor(
                    instante=instante,
                    temperatura=temperatura,
                    pressao=pressao,
                    potencia=potencia,
                )
            )
        return leituras


class OrquestradorTeste:
    def __init__(
        self,
        simulador: SimuladorSensores,
        validador: ValidadorSeguranca,
        barramento: BarramentoEventos,
    ) -> None:
        self.simulador = simulador
        self.validador = validador
        self.barramento = barramento

    def iniciar_teste(self) -> None:
        print("INICIANDO TESTE OPERACIONAL SIMULADO")
        print("-" * 60)
        print("Limites seguros:")
        for chave, valor in LIMITES_SEGUROS.items():
            print(f"- {chave.capitalize()}: {valor}")

        for numero, leitura in enumerate(self.simulador.gerar_leituras(), start=1):
            print("\nLeitura", numero)
            print(f"Horario: {leitura.instante}")
            print(f"Temperatura: {leitura.temperatura}")
            print(f"Pressao: {leitura.pressao}")
            print(f"Potencia: {leitura.potencia}")

            incidente = self.validador.validar(leitura)
            if incidente is None:
                print("Status: operacao dentro dos limites.")
                continue

            self.barramento.publicar(incidente)
            print("\n[PROTOCOLO DE SEGURANCA]")
            print("Procedimento bloqueado para evitar continuidade da operacao insegura.")
            return

        print("\nTeste finalizado sem incidentes.")
