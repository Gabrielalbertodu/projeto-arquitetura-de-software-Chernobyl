from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Protocol

from classes import (Incidente, LeituraSensor, OuvinteEvento, CentralAlertas, RegistroIncidentes, EstrategiaResposta)
from classes import ValidadorSeguranca, RespostaEmergencialPadrao
from classes import BarramentoEventos, OrquestradorTeste, SimuladorSensores, LIMITES_SEGUROS



if __name__ == "__main__":
    barramento = BarramentoEventos()
    barramento.inscrever(CentralAlertas())
    barramento.inscrever(RegistroIncidentes())

    orquestrador = OrquestradorTeste(
        simulador=SimuladorSensores(),
        validador=ValidadorSeguranca(
            limites=LIMITES_SEGUROS,
            estrategia=RespostaEmergencialPadrao(),
        ),
        barramento=barramento,
    )
    orquestrador.iniciar_teste()
