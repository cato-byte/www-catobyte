## Agentes de IA en 2026: cómo funcionan y cómo usarlos bien, con Claude, Codex y otros

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Agentes de IA en 2026](../../images/ai_agents_how_to_use_them_title_img.png)

*Artículo técnico*

## De los chatbots a los agentes

Un chatbot responde y espera. Un agente recibe un objetivo, decide qué hacer, usa herramientas, mira los resultados y sigue hasta alcanzar el objetivo o quedarse atascado. Agentes de programación como Claude Code y Codex ya editan repositorios, ejecutan pruebas y abren pull requests por su cuenta, y cada proveedor de nube vende una plataforma para construir agentes de atención al cliente, operaciones y trabajo con datos.

En un [artículo anterior](ai_agents_and_data_engineering.html) analicé lo que los agentes significan para los equipos de ingeniería de datos: qué les delegan, los riesgos y cómo cambia el rol. Este es más práctico. Explica cómo funcionan los agentes y qué patrones de diseño recomiendan los principales laboratorios, y luego cómo usar bien las dos herramientas con las que trabajo a diario, Claude Code y Codex. Se basa en [Building effective agents](https://www.anthropic.com/research/building-effective-agents) de Anthropic, la [guía de agentes](https://developers.openai.com/api/docs/guides/agents) de OpenAI, la [visión general de IA agéntica](https://aws.amazon.com/ai/agentic-ai/) de AWS y la documentación oficial de cada herramienta. Los ejemplos de prompts y de archivos de configuración están en inglés, como suelen escribirse en los proyectos reales.

## Qué es un agente

Anthropic traza una línea útil entre dos tipos de sistemas "agénticos":

- **Flujos de trabajo** (workflows): sistemas en los que los modelos de lenguaje y las herramientas se orquestan mediante rutas de código predefinidas. Tu código decide los pasos; el modelo los completa.
- **Agentes**: sistemas en los que el modelo dirige dinámicamente su propio proceso y el uso de herramientas, y mantiene el control sobre cómo cumple la tarea.

La definición de OpenAI coincide con la segunda: sistemas capaces de planificar y completar tareas con herramientas, trabajar con otros agentes y mantener el contexto entre pasos. En el fondo, un agente es sorprendentemente simple. En palabras de Anthropic, los agentes son "normalmente solo LLMs que usan herramientas según la retroalimentación del entorno, en un bucle":

```python
def run_agent(goal: str, tools: dict, max_steps: int = 30) -> str:
    messages = [{"role": "user", "content": goal}]
    for _ in range(max_steps):                      # a stopping condition
        reply = call_model(messages, tools=list(tools))
        messages.append(reply)
        if not reply.tool_calls:                    # the model considers the goal reached
            return reply.text
        for call in reply.tool_calls:               # act, then observe the result
            result = tools[call.name](**call.arguments)
            messages.append({"role": "tool", "id": call.id, "content": result})
    return "Stopped: step limit reached"
```

Todo lo que hace bueno o malo a un agente real ocurre alrededor de ese bucle: qué herramientas existen y cómo se describen, qué ve el modelo en su contexto, cómo comprueba su propio trabajo, qué puede hacer sin preguntar y cuándo se detiene.

## Empieza simple: cuándo necesitas un agente

Anthropic y OpenAI dan el mismo primer consejo: usa la solución más simple que funcione. Una sola llamada al modelo, bien escrita, con recuperación de información y algunos ejemplos basta para muchas aplicaciones. Los agentes cambian latencia y costo por flexibilidad, y Anthropic advierte que su autonomía implica "costos más altos y el riesgo de errores que se acumulan": un paso equivocado al principio es la base de todos los siguientes.

Los agentes compensan su costo en problemas abiertos, en los que no se puede prever el número de pasos ni programar una ruta fija, y cuyos resultados se pueden comprobar. Por eso la programación es hoy el caso de uso más sólido: las pruebas y los builds le dicen al agente si lo logró. La atención al cliente es el otro que destaca Anthropic, porque el éxito se mide como una solicitud resuelta.

## Los patrones

El artículo de Anthropic describe una escalera de patrones, de los flujos fijos a los agentes autónomos. Son piezas para combinar, no un framework:

| Patrón | Cómo funciona | Úsalo cuando | Ejemplo en ingeniería de datos |
|---|---|---|---|
| LLM aumentado | Una llamada con recuperación, herramientas y memoria | La mayoría de las tareas; la base de todo lo demás | Responder preguntas sobre una tabla usando el catálogo |
| Encadenamiento de prompts | Secuencia fija de llamadas, con controles entre pasos | La tarea se divide limpiamente en pasos | Redactar la documentación dbt, contrastarla con el SQL, corregir |
| Enrutamiento | Clasificar la entrada y enviarla a una ruta especializada | Categorías distintas que se tratan de forma distinta | Enviar errores de esquema y de infraestructura a runbooks distintos |
| Paralelización | Subtareas independientes a la vez, o varios votos sobre una | Velocidad, o más confianza con varias miradas | Revisar una migración en corrección, rendimiento y seguridad en paralelo |
| Orquestador y trabajadores | Un modelo divide la tarea y delega las subtareas que decide | No se pueden conocer las subtareas de antemano | Renombrar una columna en todos los modelos y dashboards que la usan |
| Evaluador y optimizador | Un modelo produce, otro critica, en bucle | Criterios claros y mejoras medibles al iterar | Ajustar una consulta lenta hasta que pase el benchmark |
| Agente autónomo | El modelo planifica y actúa en bucle con herramientas | Tareas abiertas en un entorno confiable y comprobable | Investigar y corregir un job nocturno fallido |

Los tres principios de Anthropic para construirlos valen con cualquier herramienta: mantén el diseño **simple**, haz **transparente** la planificación del agente e invierte en la **interfaz agente-computador** documentando y probando las herramientas.

## Las herramientas son la interfaz del agente

Un agente no puede ser mejor que sus herramientas. Anthropic cuenta que, al construir su agente de programación para SWE-bench, el equipo dedicó más tiempo a optimizar las herramientas que el prompt general. Su consejo es diseñar las herramientas para el modelo como diseñarías una función para un desarrollador junior: un nombre claro, una descripción con ejemplos de uso y casos límite, y parámetros que hagan difíciles los errores (lo que llama *poka-yoke*). En un caso, el modelo se equivocaba con rutas relativas tras cambiar de directorio; exigir rutas absolutas lo resolvió por completo.

Una definición de herramienta escrita con ese cuidado:

```json
{
  "name": "run_sql_readonly",
  "description": "Run a read-only SQL query on the analytics warehouse and return at most 200 rows as CSV. Use it to inspect data, check row counts or validate a transformation. Only SELECT and WITH statements are accepted; anything else is rejected. Always filter large fact tables by date, because unfiltered scans time out after 60 seconds. Table names must be fully qualified, for example analytics.marts.fct_orders.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "A single SELECT or WITH statement with fully qualified table names."},
      "reason": {"type": "string", "description": "One sentence on what you expect to learn from this query."}
    },
    "required": ["query", "reason"]
  }
}
```

La restricción de solo lectura vive en la herramienta, no solo en la descripción; el límite de filas protege la ventana de contexto; el campo `reason` deja visible en los logs la intención del agente.

## Las piezas compartidas

Unos pocos estándares ya funcionan entre herramientas, y vale la pena aprenderlos una vez:

- **MCP (Model Context Protocol)** conecta a los agentes con herramientas y datos (gestores de incidencias, bases de datos, archivos de diseño, APIs internas) mediante servidores que cualquier agente compatible puede usar. Anthropic lo creó y en diciembre de 2025 lo donó a la nueva [Agentic AI Foundation](https://sdtimes.com/ai/linux-foundation-forms-agentic-ai-foundation-to-be-new-home-for-mcp-goose-and-agents-md/) de la Linux Foundation.
- **Los archivos de contexto** contienen las instrucciones que un agente lee al inicio de cada sesión: `CLAUDE.md` para Claude Code, `AGENTS.md` para Codex y muchos otros agentes. AGENTS.md, creado por OpenAI, pasó a la misma fundación.
- **Las skills** empaquetan conocimiento del dominio o un flujo repetible en una carpeta con un archivo `SKILL.md` que el agente carga solo cuando hace falta. Claude Code y Codex las soportan.
- **Los subagentes** ejecutan parte de una tarea en su propia ventana de contexto y devuelven un resumen, lo que mantiene enfocada la conversación principal.

Para construir agentes propios, cada laboratorio ofrece capas que cambian control por comodidad. Anthropic tiene la Messages API (tú escribes el bucle), el [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) (el bucle, las herramientas y la gestión de contexto de Claude Code, como biblioteca de Python o TypeScript) y [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) (un entorno alojado en el que Anthropic ejecuta el agente y su sandbox, para trabajos de larga duración). OpenAI tiene la Responses API, el Agents SDK (tu aplicación ejecuta el bucle, con herramientas y traspasos entre agentes) y la Agents API (un entorno Codex alojado con compactación y orquestación de varios agentes). AWS ofrece [Amazon Bedrock AgentCore](https://aws.amazon.com/ai/agentic-ai/) para ejecutar a escala agentes hechos con cualquier framework o modelo, con memoria, gobierno y seguridad, además del Strands Agents SDK de código abierto. La advertencia de Anthropic sobre los frameworks vale para todos: muchos patrones caben en unas pocas líneas sobre la API directa, y si usas un framework, entiende qué hace por debajo, porque las suposiciones erróneas sobre él son una fuente común de errores.

## Claude: usar bien Claude Code

Claude Code es la herramienta de programación agéntica de Anthropic, disponible en la terminal, los IDEs, una aplicación de escritorio y la web. Su [guía de buenas prácticas](https://code.claude.com/docs/en/best-practices) parte de una restricción que explica casi todos sus consejos: la ventana de contexto se llena rápido, y el rendimiento empeora a medida que se llena. Cada archivo leído y cada salida de comando ocupan espacio, así que gestionar el contexto es la habilidad central.

**Dale una forma de verificar su trabajo.** Es el hábito más importante. Sin una comprobación que pueda ejecutar, "parece terminado" es la única señal que tiene Claude, y tú te conviertes en el ciclo de verificación. Con pruebas, un build, un linter o una captura de pantalla para comparar, puede iterar hasta que la comprobación pase. Los ejemplos de la guía:

```text
Before: implement a function that validates email addresses

After:  write a validateEmail function. example test cases: user@example.com is
        true, invalid is false, user@.com is false. run the tests after implementing
```

```text
Before: the build is failing

After:  the build fails with this error: [paste error]. fix it and verify the build
        succeeds. address the root cause, don't suppress the error
```

En ejecuciones largas puedes hacer que la comprobación sea obligatoria: `/goal` mantiene a Claude trabajando hasta que se cumple una condición, un hook Stop puede impedir que termine hasta que pase un script, y un subagente de verificación puede intentar refutar el resultado con ojos nuevos. Pide evidencia, los comandos y su salida, en lugar de afirmaciones de éxito.

**Explora, planifica y luego programa.** Para cambios que tocan varios archivos o código que no conoces, usa el modo de planificación (`Shift+Tab`, o `claude --permission-mode plan`): Claude lee y propone un plan sin editar nada. Revisa y edita el plan, luego déjalo implementar y hacer el commit. La regla práctica de la guía para saltarse este paso: si puedes describir el diff en una frase, pídelo directamente.

**Sé específico.** Nombra archivos, escenarios y restricciones, y señala patrones existentes:

```text
users report that login fails after session timeout. check the auth flow in
src/auth/, especially token refresh. write a failing test that reproduces the
issue, then fix it
```

Para funcionalidades más grandes, la guía sugiere que Claude te entreviste primero y escriba una especificación en un archivo, y luego implementarla en una sesión nueva.

**Mantén CLAUDE.md corto y útil.** Claude lo lee al inicio de cada sesión. Ejecuta `/init` para generar una primera versión y conserva solo lo que Claude no puede deducir del código: comandos, reglas de estilo distintas de las habituales, instrucciones de pruebas, normas del repositorio, trampas propias del proyecto. Para cada línea, pregúntate si quitarla causaría errores. Un archivo largo hace que Claude ignore la mitad.

```markdown
# Commands
- Tests: ./kunturvenv/bin/pytest -q (builds the site first)
- Never run scripts/deploy.sh; deployment happens in CI from master

# Conventions
- Content is written in US English first, then translated to es and fr
- Study guides live in content/guides, articles in content/blog
```

**Usa cada punto de extensión para lo que sirve.** Los hooks son deterministas, a diferencia de las instrucciones: úsalos para lo que debe ocurrir siempre, como ejecutar un linter tras cada edición o bloquear escrituras en una carpeta de migraciones. Las skills (`.claude/skills/<nombre>/SKILL.md`) guardan conocimiento o flujos que solo se necesitan a veces. Los subagentes (`.claude/agents/`) investigan en un contexto separado ("use subagents to investigate how our authentication handles token refresh"). Los servidores MCP y herramientas de línea de comandos como `gh` o `aws` lo conectan con sistemas externos; la guía señala que las CLI son la forma más eficiente en contexto de hacerlo.

**Gestiona la sesión.** Pulsa `Esc` para detenerlo y redirigirlo; `Esc Esc` o `/rewind` restauran el código y la conversación desde puntos de control anteriores. Ejecuta `/clear` entre tareas no relacionadas. Si corregiste el mismo error dos veces, el contexto está lleno de intentos fallidos: límpialo y empieza de nuevo con un prompt mejor.

**Configura los permisos a conciencia.** Las versiones recientes arrancan en modo auto, en el que un clasificador aparte revisa las acciones y bloquea las riesgosas, como la escalada de alcance o las acciones inducidas por contenido hostil. Las listas de permitidos aprueban de antemano los comandos de confianza, y el sandbox restringe el acceso al sistema de archivos y a la red a nivel del sistema operativo. El modo manual pregunta antes de cada escritura o comando.

**Escala cuando estés listo.** `claude -p` corre de forma no interactiva en scripts y CI, con salida JSON. Puedes repartir una migración entre muchos archivos, ejecutar sesiones en paralelo en worktrees de git separados o usar una pareja escritor/revisor en la que una segunda sesión, con contexto limpio, revisa lo que escribió la primera:

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from Python 2 to Python 3. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)" \
    --permission-mode dontAsk
done
```

Prueba el prompt con dos o tres archivos primero, corrige lo que falle y luego ejecuta el resto. Antes de dar por terminado un trabajo desatendido, haz que un subagente revise el diff contra el plan y reporte solo las carencias que afecten la corrección o los requisitos, para que la revisión no empuje el código hacia el sobrediseño.

## Codex: usar bien el agente de programación de OpenAI

Codex es el agente de ingeniería de software de OpenAI, disponible en ChatGPT, una aplicación de escritorio, una CLI, una extensión para IDEs y Codex Cloud, con revisión de código en GitHub. Su [guía de prompting](https://learn.chatgpt.com/codex/prompting) recomienda los mismos hábitos de fondo, con su propio vocabulario.

**Nombra el comportamiento, el código y las restricciones.** Un buen prompt para Codex dice qué debe cambiar, señala los archivos o pasos de reproducción relevantes y dice qué no debe cambiar:

```text
Users get a 500 when exporting reports with more than 10,000 rows. Start by
reproducing the bug locally with the fixture in tests/fixtures/big_report.csv, then
propose a patch and run checks. Do not change the API shape. Keep the fix minimal
and add a regression test if feasible.
```

En la CLI, referencia rutas con `@`; en el IDE, los archivos abiertos se incluyen automáticamente y las líneas seleccionadas acotan la solicitud. Para trabajo de interfaz, adjunta capturas e indica el framework y las convenciones de componentes, que una imagen no muestra.

**Planifica y trabaja por hitos.** En tareas de varios pasos, `/plan` hace que Codex investigue y proponga un enfoque antes de editar; puedes pedir revisiones, como qué archivos se mueven en cada hito y una estrategia de reversión. `/goal` fija un objetivo persistente cuando está disponible. El trabajo grande avanza un hito a la vez, cada uno revisado antes del siguiente.

**Pídele que verifique y que reporte.** Los ejemplos de la guía: repetir la reproducción tras la corrección, ejecutar el linter y el conjunto de pruebas relevante más pequeño y reportar los comandos y resultados, arrancar el servidor de desarrollo y dar la URL para comprobar. Tras atender los comentarios de una revisión, vuelve a ejecutar `/review`.

**Escribe AGENTS.md.** Codex lee un archivo global de `~/.codex` y luego cada `AGENTS.md` desde la raíz del repositorio hasta el directorio actual; los archivos más cercanos a tu directorio de trabajo prevalecen sobre los anteriores, hasta 32 KiB por defecto. Pon en él los acuerdos de trabajo (gestor de paquetes, qué pruebas ejecutar), las expectativas del repositorio (linter antes de los pull requests) y las reglas de revisión de código cerca del código al que aplican; los archivos anidados pueden reemplazar comandos para un servicio concreto.

```markdown
# AGENTS.md
- Use uv; never pip install into the system Python.
- After changing pipeline code, run: uv run pytest tests/unit -q
- Run uv run ruff check . before opening a pull request.
- Never edit files under migrations/ by hand; generate them with make migration.

## Code Review Rules
- Flag any query on fct_* tables without a date filter.
```

**Elige el modo de permisos.** "Ask for approval" trabaja dentro del espacio de trabajo y se detiene antes de editar fuera de él o de usar internet; es el modo recomendado por defecto. "Approve for me" mantiene el mismo sandbox pero envía las solicitudes de aprobación a un revisor automático que solo se detiene ante acciones potencialmente inseguras. "Full access" quita las restricciones. El sandbox define a qué puede acceder Codex; las aprobaciones, cuándo se detiene.

**Delega en paralelo.** Codex Cloud ejecuta tareas en entornos aislados mientras sigues trabajando: planifica en local, luego entrega "Implement Milestone 1 from the plan", revisa el diff y abre un pull request. `codex exec` lo ejecuta de forma no interactiva desde scripts. Como pequeño ejemplo de primera mano, las imágenes de portada de este artículo y de los dos anteriores se generaron llamando a `codex exec` desde otro agente, con un prompt que describía cada artículo y un directorio temporal donde escribir, y se revisaron antes de añadirlas al sitio.

## Otros agentes que conviene conocer

Los mismos hábitos sirven para el resto del sector. GitHub Copilot tiene un modo agente en el editor y un agente de programación que va de las issues a los pull requests. Cursor es un editor centrado en IA con agentes en segundo plano. Gemini CLI de Google es un agente de terminal de código abierto. Kiro, de AWS, es un IDE construido alrededor del desarrollo guiado por especificaciones, en el que los requisitos y los documentos de diseño van antes que el código. Y las plataformas de datos traen sus propios agentes dentro del producto, como Cortex Code de Snowflake y las funciones agénticas de Lakeflow en Databricks, que trabajan con el catálogo y los permisos de la plataforma. La mayoría leen `AGENTS.md` o su propio archivo de contexto, soportan MCP y ofrecen alguna combinación de modo de planificación, niveles de permisos y ejecución en segundo plano.

## Prácticas que funcionan con cualquier agente

Entre el material de Anthropic, OpenAI y AWS y mi propio uso, estos son los hábitos que marcan la diferencia:

1. **Dale al agente una comprobación que pueda ejecutar.** Pruebas, builds, linters, validaciones de datos, capturas. Sin comprobación, no hay trabajo desatendido.
2. **Escribe el contexto, en poco espacio.** Un archivo de contexto corto con comandos y reglas no evidentes, más skills para el conocimiento ocasional. Recórtalo cuando el agente lo ignore.
3. **Planifica antes de los cambios grandes.** Separa la exploración de la edición y revisa el plan; corregirlo es más barato que corregir el diff.
4. **Sé específico sobre el alcance y las restricciones.** Archivos, escenarios, qué no debe cambiar, qué significa "terminado".
5. **Mantén limpio el contexto.** Una tarea por sesión, subagentes para investigar, un reinicio tras correcciones repetidas.
6. **Mínimo privilegio.** Sandboxes, credenciales de desarrollo, aprobación para todo lo que tenga efectos; nunca acceso de escritura a producción para un agente.
7. **Trata el contenido externo como no confiable.** Issues, páginas web y archivos pueden traer inyección de prompts; el límite real son los permisos del agente, no su prompt.
8. **Revisa con ojos nuevos.** Una segunda sesión o un subagente, o una persona, revisa el diff contra los requisitos antes de fusionarlo.
9. **Paraleliza el trabajo independiente.** Worktrees, tareas en la nube y scripts de reparto, cada uno con su comprobación.
10. **Mide el resultado.** Tiempo de entrega, defectos y retrabajo, no lo rápido que se siente. AWS cuenta que equipos internos que rediseñaron su forma de trabajar alrededor de los agentes entregaron en 76 días, con seis ingenieros, un proyecto dimensionado para 30 desarrolladores; resultados así vienen de cambiar el flujo de trabajo, no solo de añadir una herramienta.

La dirección es clara: los agentes pasan de ser asistentes a los que vigilas a colegas en los que delegas. Lo que hace segura la delegación es lo mismo que con las personas: una tarea clara, el contexto adecuado, permisos limitados, una forma de comprobar el resultado y una revisión antes de darlo por bueno.

## Fuentes

- Anthropic: [Building effective agents](https://www.anthropic.com/research/building-effective-agents), [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)
- OpenAI: [Agents guide](https://developers.openai.com/api/docs/guides/agents), [Codex prompting](https://learn.chatgpt.com/codex/prompting), [Codex AGENTS.md](https://learn.chatgpt.com/codex/agent-configuration/agents-md), [Codex permissions](https://learn.chatgpt.com/codex/permission-modes)
- AWS: [Agentic AI on AWS](https://aws.amazon.com/ai/agentic-ai/)
- Linux Foundation: [Agentic AI Foundation, new home for MCP and AGENTS.md (SD Times)](https://sdtimes.com/ai/linux-foundation-forms-agentic-ai-foundation-to-be-new-home-for-mcp-goose-and-agents-md/)
