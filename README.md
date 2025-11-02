# 🤖 Agente Basado en Conocimiento - Soporte Python (MIA-103)
![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)

Este repositorio contiene el código fuente del proyecto final para el curso "Fundamentos de Inteligencia Artificial". El software es un **Agente Basado en Conocimiento (KBA)** visual e interactivo, diseñado para diagnosticar errores comunes de Python que enfrentan los estudiantes, basándose en los principios del **Capítulo 7 de "Artificial Intelligence: A Modern Approach" (AIMA)** de Russell y Norvig.

## 🏛️ Arquitectura del Agente

Este no es un agente de IA neuronal (como un LLM). Es un agente de **IA Simbólica** puro que opera con lógica explícita.

* **Agente:** Agente Basado en Conocimiento (KBA).
* **Motor de Inferencia:** `experta`, que implementa un motor de **Encadenamiento Hacia Adelante (Forward Chaining)**.
* **Base de Conocimiento (KB):** Un conjunto de `Fact` (Hechos) y `@Rule` (Reglas) definidos en la clase `AgenteSoportePython`.
* **Perceptor:** La función `parsear_error_a_hecho` que traduce el texto de error del usuario en un `Fact` estructurado.
* **Actuador:** La interfaz de Streamlit que muestra la `Sugerir` (conclusión) al usuario.

### Flujo Lógico del Ciclo (TELL/ASK)

Cuando un usuario presiona el botón, ocurre el siguiente ciclo:

1.  **Percepción:** El `st.text_area` captura el `string` del error.
2.  **`TELL` (Decir):**
    * El **Perceptor** (`parsear_error_a_hecho`) convierte el `string` en un `Fact` (ej. `Error(tipo='ModuleNotFoundError', ...)`).
    * Este `Fact` inicial se declara (`agente.declare()`) en la Memoria de Trabajo (WM).
3.  **`ASK` (Preguntar):**
    * `agente.run()` inicia el motor de **Encadenamiento Hacia Adelante**.
    * El motor "dispara" las reglas cuyas premisas coinciden con los hechos en la WM.
    * Por ejemplo, `Error(...)` dispara la `regla_detectar_modulo_faltante`.
    * Esta regla *añade un nuevo hecho* (`FaltaModulo(...)`) a la WM.
    * Este *nuevo hecho* dispara la `regla_sugerir_instalacion`.
    * El ciclo se detiene cuando no hay más reglas que disparar.
4.  **Acción:** La interfaz busca el `Fact` final (`Sugerir(...)`) en la WM y muestra el resultado al usuario.

---

## 🚀 Guía de Instalación y Ejecución

Esta guía está diseñada para ser a prueba de fallos, basándose en los problemas de compatibilidad de librerías encontrados.

### 1. Prerrequisitos

* Tener **Git** instalado.
* Tener **Anaconda/Miniconda** instalado (usaremos `conda` para gestionar el entorno).

### 2. Clonar el Repositorio

```bash
git clone [https://github.com/JackGod7/ia-proyecto-kba.git](https://github.com/JackGod7/ia-proyecto-kba.git)
cd ia-proyecto-kba
```

### 3. Configuración del Entorno (Paso Crucial)

**No** intentes usar `venv` o una versión de Python más nueva (como 3.10+). La librería `experta` y sus dependencias (`frozendict==1.2`) requieren una versión de Python específica para funcionar sin errores. Usaremos **Python 3.9**.

**a. Crear el Entorno Conda**
Abre una terminal de Anaconda y ejecuta:

```bash
# Crea un nuevo entorno llamado 'ia_proyecto' con Python 3.9
conda create -n ia_proyecto python=3.9 -y
```

**b. Activar el Entorno**
(Debes hacer esto cada vez que abras una nueva terminal para trabajar en el proyecto).

```bash
conda activate ia_proyecto
```
*Tu prompt de terminal ahora debe empezar con `(ia_proyecto)`.*

**c. Instalar Dependencias**
Usa el archivo `requirements.txt` para instalar `streamlit` y `experta`:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

Una vez que tu entorno `(ia_proyecto)` esté activado y las librerías estén instaladas, ejecuta:

```bash
streamlit run agente_app.py
```

Se abrirá una pestaña en tu navegador en `http://localhost:8501` con la aplicación funcionando.

---

## 🧪 Escenarios de Prueba (Para el Informe)

Usa estos 3 escenarios para probar el agente y generar las capturas de pantalla y el análisis para las secciones 9, 10 y 11 del informe.

| Escenario | Entrada (Pega esto en la app) | Objetivo y Qué Analizar |
| :--- | :--- | :--- |
| **1. Éxito (Encadenamiento)** | `ModuleNotFoundError: No module named 'pandas'` | **Objetivo:** Demostrar el Encadenamiento Hacia Adelante (Regla 1 -> Regla 2).<br>**Captura:** Toma un screenshot del JSON de "Memoria de Trabajo Final".<br>**Análisis:** Explica cómo `Fact-1` (Error) llevó a `Fact-2` (FaltaModulo), que a su vez llevó a `Fact-3` (Sugerir). |
| **2. Éxito (Regla Simple)** | `if True SyntaxError: expected ':'` | **Objetivo:** Demostrar otra regla en la KB (Regla 3).<br>**Captura:** Toma un screenshot del mensaje de éxito: `Sugerencia del Agente: Detecté un SyntaxError...`<br>**Análisis:** Explica que esta es una regla simple (Percepción -> Acción) que no requiere encadenamiento. |
| **3. Fallo Controlado (Robustez)** | `ValueError: x not in list` | **Objetivo:** Demostrar la robustez del agente (Regla 5, "fallback").<br>**Captura:** Toma un screenshot del mensaje de error: `Resultado: Lo siento, no tengo una regla en mi Base de Conocimiento...`<br>**Análisis:** Explica que esta regla asegura que el agente siempre dé una respuesta, cumpliendo su ciclo de racionalidad. |

---

### Autores

* **Jack Aguilar** (`jack.aguilar.c@uni.pe`)
* **Mitzuko Quispe** (`mitzuko.quispe.c@uni.pe`)
* **Segundo Sigüeñas** (`segundo.siguenas.g@uni.pe`)
