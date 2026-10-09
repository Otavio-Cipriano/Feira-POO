import os
import sys

def run_checks():
    print("Iniciando verificação do projeto Feira-POO...")
    checks_passed = 0

    try:
        # 1. Verifica se app/models existe
        assert os.path.exists('app/models'), "Diretório app/models não encontrado."
        checks_passed += 1

        # 2. Verifica se app/controllers existe
        assert os.path.exists('app/controllers'), "Diretório app/controllers não encontrado."
        checks_passed += 1

        # 3. Importa os models principais para confirmar sua existência
        from app.models.barraca import Barraca, BarracaAlimentacao, BarracaGourmet
        from app.models.feirante import Feirante
        from app.models.reserva import Reserva
        checks_passed += 1

        # 4. Valida constante Feirante.LIMITE_RESERVAS
        assert hasattr(Feirante, "LIMITE_RESERVAS"), "Constante LIMITE_RESERVAS ausente em Feirante."
        assert Feirante.LIMITE_RESERVAS == 2, "LIMITE_RESERVAS deve ser 2."
        checks_passed += 1

        # 5. Validação de documento no model Feirante (disparando erro)
        f = Feirante(999, "Teste", "12345678901", "11999999999")
        try:
            f.alterar_documento("123")
            assert False, "Deveria ter disparado ValueError ao passar documento com 3 dígitos."
        except ValueError:
            pass # Sucesso, a regra de negócio funcionou
        checks_passed += 1

        # 6. Instancia Barraca e verifica TAXA_BASE
        b = Barraca(999, "B99", 10.0)
        assert b.calcular_taxa_diaria() == 50.0, "Taxa diária de Barraca base incorreta."
        checks_passed += 1

        # 7. Instancia BarracaAlimentacao e verifica TAXA_BASE
        ba = BarracaAlimentacao(998, "BA99", 15.0)
        assert ba.calcular_taxa_diaria() == 80.0, "Taxa diária de BarracaAlimentacao incorreta."
        checks_passed += 1

        # 8. Instancia BarracaGourmet e verifica TAXA_BASE
        bg = BarracaGourmet(997, "BG99", 20.0)
        assert bg.calcular_taxa_diaria() == 120.0, "Taxa diária de BarracaGourmet incorreta."
        checks_passed += 1

        # 9. Verifica se a carga mock no controller retorna dados
        from app.controllers.feirante_controller import listar_feirantes
        assert len(listar_feirantes()) >= 5, "O mock de feirantes deve ter pelo menos 5 registros."
        checks_passed += 1

        # 10. Teste de conflito de Reserva (limite de 2 ou data)
        from app.controllers.reserva_controller import registrar_reserva
        try:
            # Tenta registrar uma reserva com a mesma barraca na mesma data já existente no mock
            # No mock temos a barraca 1 reservada em 2026-10-15 pelo feirante 1.
            # Vamos tentar reservar a barraca 1 novamente no mesmo dia para o feirante 2
            registrar_reserva(1, 2, "2026-10-15")
            assert False, "Deveria ter disparado ValueError ao reservar barraca já reservada na mesma data."
        except ValueError as e:
            pass # Sucesso, a regra de negócio funcionou
        checks_passed += 1

        # 11. Verifica registro de rotas no arquivo main.py
        with open('main.py', 'r', encoding='utf-8') as f_main:
            content = f_main.read()
            assert "app.include_router(" in content, "main.py não está incluindo as rotas (app.include_router não encontrado)."
        checks_passed += 1

        # 12. Confirmação dos pacotes exigidos no requirements.txt
        with open('requirements.txt', 'r', encoding='utf-8') as f_req:
            content = f_req.read()
            assert "fastapi" in content.lower(), "fastapi não encontrado em requirements.txt."
            assert "uvicorn" in content.lower(), "uvicorn não encontrado em requirements.txt."
        checks_passed += 1

    except Exception as e:
        print(f"\n[ERRO] A checagem {checks_passed + 1} falhou!")
        print(f"Detalhes: {e}")
        sys.exit(1)

    print(f"\n[SUCESSO] Todas as {checks_passed} checagens passaram.")
    sys.exit(0)

if __name__ == "__main__":
    run_checks()
