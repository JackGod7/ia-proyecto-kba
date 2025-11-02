import streamlit as st
from experta import * # Importamos 'experta'

# --- FASE 3: EL "CEREBRO" (Motor y Hechos) ---

# 3.1 Definición de Hechos (El "Qué")
class Error(Fact):
    """Representa la PERCEPCIÓN inicial."""
    tipo = Field(str, mandatory=True)
    modulo = Field(str, default=None)  # Corregido para experta
    mensaje = Field(str, default=None) # Corregido para experta
    pass

class FaltaModulo(Fact):
    """Hecho INTERMEDIO, deducido por inferencia."""
    nombre = Field(str, mandatory=True)
    pass

class Sugerir(Fact):
    """Hecho FINAL, la acción/conclusión del agente."""
    accion = Field(str, mandatory=True)
    detalle = Field(str, mandatory=True)
    pass

# 3.2 Definición del Motor (El "Cómo")
class AgenteSoportePython(KnowledgeEngine):

    @Rule(Error(tipo='ModuleNotFoundError', modulo=MATCH.mod))
    def regla_detectar_modulo_faltante(self, mod):
        """REGLA 1: Error(ModuleNotFoundError, X) -> FaltaModulo(X)"""
        self.declare(FaltaModulo(nombre=mod))

    @Rule(FaltaModulo(nombre=MATCH.mod))
    def regla_sugerir_instalacion(self, mod):
        """REGLA 2: FaltaModulo(X) -> Sugerir(Instalar, ...)"""
        self.declare(Sugerir(accion='Instalar',
                             detalle=f"El módulo '{mod}' no está instalado. Ejecuta: pip install {mod}"))

    @Rule(Error(tipo='SyntaxError', mensaje=MATCH.msg))
    def regla_syntax_error_colon(self, msg):
        """REGLA 3: Error(SyntaxError, M) AND ":" in M -> Sugerir(...)"""
        if msg and 'expected' in msg.lower() and ':' in msg:
            self.declare(Sugerir(accion='Revisar',
                                 detalle="Detecté un SyntaxError. Revisa si olvidaste dos puntos ':' al final de una línea (ej. en un if, for, def)."))

    @Rule(Error(tipo='ImportError', mensaje=MATCH.msg))
    def regla_import_error_general(self, msg):
        """REGLA 4: Error(ImportError, M) -> Sugerir(...)"""
        self.declare(Sugerir(accion='Revisar',
                             detalle=f"Error al importar: '{msg}'. Verifica el nombre (¿es un typo?) o si es una importación circular."))

    @Rule(Error(tipo='Desconocido', mensaje=MATCH.msg))
    def regla_fallback_desconocido(self, msg):
        """REGLA 5: Regla "fallback" para errores no reconocidos."""
        detalle_msg = msg[:50] if msg else "desconocido"
        self.declare(Sugerir(accion='No Resuelto',
                             detalle=f"Lo siento, no tengo una regla en mi Base de Conocimiento para este error específico ({detalle_msg}...). Consulta a un tutor."))

# --- FASE 4: PERCEPTOR E INTERFAZ VISUAL ---

def parsear_error_a_hecho(raw_text: str) -> Fact:
    """
    Traduce el texto crudo del usuario en un Hecho (Fact) estructurado
    para la Base de Conocimiento del agente.
    """
    text = raw_text.strip()

    if "ModuleNotFoundError" in text:
        try:
            modulo = text.split("No module named")[-1].strip().replace("'", "").replace("\"", "")
            return Error(tipo='ModuleNotFoundError', modulo=modulo)
        except Exception:
            return Error(tipo='ModuleNotFoundError', modulo='desconocido')

    if "SyntaxError" in text and "expected" in text and ":" in text:
        return Error(tipo='SyntaxError', mensaje=text)

    if "ImportError" in text and "ModuleNotFoundError" not in text:
        return Error(tipo='ImportError', mensaje=text)

    # Si ninguna regla de parsing coincide, es Desconocido
    return Error(tipo='Desconocido', mensaje=text)

# 4.2 Código de la UI (Streamlit)
def main_app():
    """
    Función principal que construye la interfaz de usuario de Streamlit.
    """
    st.title("🤖 Agente Basado en Conocimiento")
    st.subheader("Soporte para Estudiantes de Python (AIMA Cap. 7)")
    st.caption(f"Implementación con `experta` (Motor de Inferencia) y `streamlit` (UI)")

    st.markdown("---")

    user_input = st.text_area("Pega tu mensaje de error de Python aquí:",
                              height=100,
                              placeholder="Ej: ModuleNotFoundError: No module named 'pandas'")

    if st.button("Pedir Ayuda al Agente"):
        if not user_input:
            st.warning("Por favor, ingresa un mensaje de error.")
            return

        agente = AgenteSoportePython()
        agente.reset()

        st.write("--- 1. Percepción (TELL) ---")
        hecho_percibido = parsear_error_a_hecho(user_input)
        agente.declare(hecho_percibido)
        st.info(f"Hecho percibido: `{hecho_percibido}`")

        st.write("--- 2. Inferencia (ASK) ---")
        agente.run()
        st.text("Motor de inferencia ejecutado (Forward Chaining).")

        st.write("--- 3. Conclusión (Acción) ---")
        sugerencia_final = None
        for fact in agente.facts.values():
            if isinstance(fact, Sugerir):
                sugerencia_final = fact
                break

        if sugerencia_final:
            if sugerencia_final['accion'] == 'No Resuelto':
                st.error(f"**Resultado:** {sugerencia_final['detalle']}")
            else:
                st.success(f"**Sugerencia del Agente:** {sugerencia_final['detalle']}")
        else:
            st.error("Error crítico: El agente no pudo llegar a una conclusión.")

        st.subheader("Memoria de Trabajo Final (Estado del Agente)")
        st.caption("Esto demuestra TODOS los hechos inferidos, incluyendo los pasos intermedios.")

        facts_list = [dict(f) for f in agente.facts.values()]
        st.json(facts_list)

if __name__ == "__main__":
    main_app()