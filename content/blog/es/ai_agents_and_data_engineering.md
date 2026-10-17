## Agentes de IA e ingeniería de datos en 2026: lo que los equipos hacen de verdad, lo que cuesta y lo que cambia

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Agentes de IA e ingeniería de datos en 2026](../../images/ai_agents_and_data_engineering_title_img.png)

*Artículo técnico*

## Del autocompletado a los agentes

Hace dos años, "IA para desarrolladores" significaba sobre todo autocompletado y una ventana de chat. En 2026 la herramienta por defecto es un **agente**: Claude Code, OpenAI Codex, el modo agente de GitHub Copilot, Cursor, Gemini CLI y herramientas similares que leen un repositorio, ejecutan comandos y pruebas, editan muchos archivos y abren pull requests, repitiendo el ciclo hasta terminar la tarea o atascarse.

La adopción ha sido rápida. En la [encuesta de desarrolladores de Stack Overflow 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) (más de 30.000 respuestas), el 66 % de los desarrolladores que usan herramientas de IA usa agentes de código, Claude Code (66 %) y GitHub Copilot (59 %) son los agentes más usados, y el 73 % de quienes usan estas herramientas lo hace todos los días. La investigación Developer Ecosystem 2026 de JetBrains, con más de 15.000 desarrolladores profesionales, reporta que [la adopción de Claude Code en el trabajo se duplicó en el primer semestre y Codex creció unas cinco veces](https://dev.to/jamilxt/claude-code-overtakes-github-copilot-what-jetbrains-survey-of-15000-developers-says-about-ai-3nhc). Las cifras exactas varían entre encuestas, pero la dirección no.

Las plataformas de datos siguieron el mismo camino. Snowflake, Databricks y Google ya incluyen agentes en sus productos ([Cortex Code de Snowflake](https://www.snowflake.com/en/blog/cortex-code-governed-agent-data-stack/), [las funciones agénticas de Databricks en Lakeflow](https://www.databricks.com/blog/lakeflow-new-era-agentic-data-engineering) y el agente de ingeniería de datos de BigQuery), que escriben SQL, construyen pipelines y explican el linaje usando el catálogo y los permisos de la plataforma.

Este artículo trata de lo que eso significa para la ingeniería de datos en particular: qué delegan de verdad los equipos a los agentes, las ventajas y desventajas, los riesgos de seguridad y privacidad, lo que esperan ahora las empresas y las prácticas que recomiendo para adoptarlos. Uso agentes a diario en mi propio trabajo, incluido el [lakehouse de registros mercantiles europeos](../projects/eu-company-registry.html) y este sitio, así que algunos ejemplos son de primera mano.

## Para qué usan de verdad los equipos de datos los agentes

Las encuestas a desarrolladores en general dicen que la mayor parte del uso de IA sigue siendo escribir código en áreas conocidas (67 % en la encuesta de Stack Overflow) y depurar (61 %), y que solo un 20 % usa IA para desplegar, operar o diagnosticar sistemas en producción. En el trabajo con datos, las tareas que rinden de forma constante son estas:

**Escribir y refactorizar código de transformación.** Los jobs de PySpark, los modelos de dbt, las migraciones SQL y los DAG de Airflow se prestan bien a los agentes: los patrones son conocidos, el código se puede probar y el ciclo de retroalimentación (ejecutar las pruebas, leer el error, corregir) es justo lo que los agentes hacen bien. Refactorizaciones que antes tomaban una semana, como pasar cuarenta modelos a una nueva convención de nombres o reemplazar una API obsoleta en todo el código, ahora toman una tarde más la revisión.

**Escribir pruebas y datos de prueba.** Los agentes son buenos generando pruebas unitarias, datos sintéticos que reproducen las particularidades de una fuente y los casos límite que una persona cansada se salta (nulls, archivos vacíos, claves duplicadas, zonas horarias). Es donde he visto el mejor retorno: más pruebas significa cambios más seguros, lo que también hace más segura cada tarea posterior del agente.

**Investigar fallas.** "El job nocturno falló; aquí está el log" es un excelente prompt para un agente. Puede leer el stack trace, abrir el código, revisar los commits recientes, consultar la tabla que se rompió y proponer una corrección en minutos. Es especialmente útil para las tediosas: problemas de codificación, un cambio en el orden de las columnas de un archivo fuente, un error de tipos después de un cambio de esquema.

**Entender código y datos desconocidos.** Pedirle a un agente que explique cómo funciona un pipeline heredado, que rastree de dónde viene una columna o que resuma un procedimiento almacenado de 3.000 líneas ahorra horas de lectura. Con acceso al catálogo (a través del agente de una plataforma o un servidor MCP), también puede perfilar tablas, encontrar claves de unión y detectar distribuciones sospechosas.

**Infraestructura y CI/CD.** Los módulos de Terraform, los workflows de GitHub Actions, las políticas IAM y los Dockerfiles tienen mucho código repetitivo, así que los agentes los escriben rápido. También son lo que necesita la revisión más cuidadosa, porque un error aquí es un incidente de seguridad, no un número equivocado.

**Documentación y contratos de datos.** Descripciones de modelos, documentación de columnas, runbooks, ADR y README que nadie quería escribir ahora se escriben, y se mantienen más cerca del código.

**Analítica en lenguaje natural.** Las interfaces texto a SQL construidas sobre una capa semántica permiten que los usuarios de negocio hagan preguntas directamente. Funciona bien cuando las métricas están definidas una sola vez (en una capa semántica o en vistas de métricas gobernadas) y mal cuando el agente tiene que adivinar a partir de tablas crudas qué significa "cliente activo".

Lo que los equipos en general *todavía no* delegan a los agentes: cambios desatendidos en datos de producción, decisiones de modelado y arquitectura sin revisión, cualquier cosa con datos personales sin controles estrictos, y la última palabra sobre si un número es correcto.

## Por qué el trabajo con datos es distinto para los agentes

Casi toda la discusión pública sobre agentes de código trata del código de aplicaciones. La ingeniería de datos agrega problemas que un agente no puede ver leyendo el repositorio:

- **La exactitud vive en los datos, no en el código.** Un agente puede escribir un join que compila, pasa las pruebas unitarias y duplica filas en producción sin avisar porque una clave no es única en los datos reales. La revisión de código no lo detecta; las pruebas de datos y la conciliación sí.
- **Estado y radio de impacto.** Un despliegue equivocado de un servicio web se revierte. Un `MERGE` equivocado en una tabla de historia escribe datos incorrectos que hay que reparar, y es posible que las tablas posteriores ya los hayan consumido.
- **Costo.** Un agente que itera sobre una consulta contra un data warehouse o un clúster gasta dinero real en cada intento. Un bucle que ejecuta veinte veces una lectura completa de una tabla puede costar más que el tiempo de ingeniería que ahorró.
- **Datos sensibles.** Los ingenieros de datos trabajan cerca de los datos de los clientes. Un agente que puede consultar tablas de producción también puede leer información personal (y enviarla a un proveedor de modelos, o dejarla en un log).
- **Semántica.** Las definiciones de negocio, los problemas de calidad conocidos y las razones detrás de filtros raros suelen vivir en la cabeza de las personas o en documentos dispersos. Sin ese contexto, un agente producirá una lógica segura de sí misma, plausible y equivocada.

El hilo común: los agentes son excelentes en las partes de la ingeniería de datos que se parecen a la ingeniería de software, y necesitan mucha más guía y verificación en las partes que tratan de los datos.

## Ventajas y desventajas

### Velocidad frente a comprensión

Los agentes producen código más rápido de lo que las personas pueden entenderlo. El riesgo no es el código malo en sí; es el código que nadie del equipo entiende del todo, lo que se vuelve un problema la primera vez que falla a las 3 de la mañana. Los equipos a los que les va bien mantienen una regla: eres dueño de lo que fusionas y debes poder explicarlo.

### Productividad percibida frente a medida

La evidencia sobre productividad es más mixta que el marketing. En el [estudio aleatorizado de METR de 2025](https://scienceblog.com/t-a-randomized-trial-by-metr-found-that-experienced-developers-completed-real-coding-tasks-19-slower-when-allowed-to-use-ai-tools-yet-afterwards-they-estimated-on-average-that-ai-had-made-them-20-fast/), desarrolladores experimentados de código abierto fueron un 19 % más lentos con herramientas de IA en sus propios proyectos, aunque creían haber sido un 20 % más rápidos. METR ahora describe ese resultado como histórico: cuando intentó repetir el experimento con herramientas más nuevas en 2026, muchos desarrolladores se negaron a trabajar sin IA, lo que hizo poco confiable la nueva medición. Ambos hechos son informativos. Las herramientas han mejorado mucho, pero las personas juzgan mal su propia velocidad, así que mide resultados (tiempo de entrega, incidentes, retrabajo), no impresiones.

### Amplificador, no solución

El [informe DORA 2025 de Google sobre desarrollo de software asistido por IA](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/), basado en casi 5.000 profesionales, describe la IA como un **amplificador**: magnifica las fortalezas de los equipos con buenas plataformas, flujos de trabajo claros y pruebas sólidas, y las disfunciones de los equipos que no las tienen. Coincide con lo que veo en los equipos de datos. Con una suite de pruebas rápida, CI, revisión de código y convenciones claras, los agentes multiplican lo que se entrega. Sin ellas, los agentes producen más código sin probar, más rápido.

### Costo

Usar agentes no es gratis: suscripciones o costos por tokens, más los costos de cómputo cuando los agentes ejecutan consultas y jobs. La encuesta de Stack Overflow 2026 encontró que el 38 % de las organizaciones ya pone límites de uso y el 21 % reporta un mayor gasto en IA. Para los equipos de datos, el cómputo es la palanca más grande: da a los agentes conjuntos de datos de desarrollo pequeños y warehouses baratos, no del tamaño de producción.

### Dependencia

Los equipos que construyen su flujo de trabajo alrededor del agente de un solo proveedor, su formato de configuración y sus integraciones se exponen a la dependencia del proveedor, a cambios de precio y a caídas del servicio. Mantén el conocimiento (convenciones, archivos de contexto, pruebas, CI) en el repositorio, en formatos que cualquier herramienta pueda usar, y conserva la capacidad de trabajar sin el agente.

## Riesgos de seguridad

Los agentes combinan tres cosas que los especialistas en seguridad llevan décadas manteniendo separadas: acceso a datos privados, exposición a contenido no confiable y capacidad de actuar y comunicarse con el exterior. Simon Willison llama a esta combinación la **tríada letal**; la "Regla de dos para agentes" de Meta sugiere que un agente que actúa sin aprobación humana tenga como máximo dos de las tres. El [informe 2026 del OWASP GenAI Security Project](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/) señala que los riesgos de los agentes pasaron de la teoría a los incidentes documentados, y que la inyección de prompts interviene en seis de las diez categorías de su Top 10 para aplicaciones agénticas.

Los riesgos principales, con ejemplos reales:

**Inyección de prompts.** Todo lo que lee un agente puede contener instrucciones: el título de un pull request, un issue, el README de una dependencia, una página web, un valor en una tabla. En abril de 2026, unos investigadores mostraron que [un título de pull request malicioso hacía que agentes de revisión de Anthropic, Google y GitHub filtraran sus propias claves de API](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) en un workflow de GitHub Actions. Los ingenieros de datos tienen una superficie adicional: los datos mismos. Un campo de texto libre en un sistema fuente puede llevar instrucciones para un agente que después perfile esa tabla.

**Exposición de secretos.** Los agentes se ejecutan con tu entorno: credenciales de la nube, contraseñas de bases de datos, tokens en archivos `.env`. Todo lo que está en su contexto puede terminar en un log, un commit, un comentario o una solicitud al proveedor del modelo. El malware que roba credenciales también ha empezado a [buscar archivos de configuración y tokens de agentes](https://botmonster.com/ai/ai-coding-agent-insider-threat-prompt-injection-mcp-exploits/) en las máquinas de los desarrolladores.

**Acciones destructivas.** El ejemplo más conocido es el incidente de Replit en 2025, en el que un agente de código borró la base de datos de producción de una empresa durante un congelamiento de código. Para los equipos de datos, el equivalente es un agente con acceso de escritura a producción que ejecuta `DROP`, `TRUNCATE`, `DELETE` sin filtro o `terraform destroy`.

**Riesgos de herramientas y de la cadena de suministro.** Los servidores MCP, los plugins y las extensiones de agentes son código que se ejecuta con los permisos del agente. En junio de 2026, unos investigadores mostraron el ["agentjacking"](https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/): instrucciones plantadas en eventos de error que agentes de código (Claude Code, Cursor, Codex) leían a través del servidor MCP oficial de Sentry y luego obedecían, ejecutando comandos con los privilegios del desarrollador. El mismo año trajo paquetes maliciosos y una falla crítica de ejecución remota de código en la infraestructura MCP. Para los equipos de datos la lección es directa: los logs, los mensajes de error y el contenido de las tablas son entradas que un atacante puede controlar. Los agentes también sugieren dependencias, incluso algunas que no existen (y que los atacantes registran).

**Código generado inseguro.** SQL construido concatenando cadenas, políticas IAM demasiado amplias (`"Action": "*"`), buckets públicos y verificaciones TLS desactivadas son cosas que los agentes producen cuando optimizan para "que funcione".

## Privacidad del código y de los datos

Usar un agente implica enviar código, y a menudo datos, a un proveedor de modelos. Preguntas que todo equipo debería responder antes de adoptarlo:

- **¿Se usan nuestros datos para entrenar?** Los términos empresariales y de API de los principales proveedores en general excluyen por defecto los datos de los clientes del entrenamiento, mientras que los planes para consumidores pueden no hacerlo. Revisa los términos del plan exacto que usas, no el marketing general del proveedor.
- **¿Cuánto tiempo se conservan y dónde?** Los periodos de retención, las opciones de retención cero y la residencia de los datos (procesamiento en la UE, por ejemplo) varían según el plan y el proveedor. Para datos regulados por el RGPD o por la ley colombiana de protección de datos personales (Ley 1581 de 2012), necesitas un acuerdo de tratamiento de datos y saber dónde ocurre el procesamiento.
- **¿Qué ve realmente el agente?** Un agente que ejecuta `SELECT * ... LIMIT 10` sobre una tabla de clientes envía al proveedor los datos personales de diez clientes. Dale acceso a datos de desarrollo, a muestras anonimizadas o sintéticas y a metadatos (esquemas, estadísticas) en lugar de filas crudas de producción.
- **¿La herramienta está aprobada?** La "IA en la sombra", ingenieros que usan cuentas personales con código de la empresa, es común. El informe de OWASP cita datos de IBM según los cuales solo el 37 % de las organizaciones tiene una política para detectarla. Ofrecer una herramienta autorizada con reglas claras funciona mejor que prohibir herramientas que la gente usará de todas formas.
- **¿Necesitamos ejecutar los modelos nosotros mismos?** Para entornos muy sensibles, las opciones incluyen modelos alojados en tu propia cuenta de nube (Amazon Bedrock, Azure, Vertex AI) bajo tus acuerdos existentes, los agentes integrados de la plataforma que respetan los permisos del catálogo, o modelos de pesos abiertos en tu propia infraestructura, con menor capacidad como contrapartida.

## Lo que esto significa para el rol

El trabajo está cambiando, no desapareciendo. Escribir código repetitivo ahora es barato; lo costoso es saber qué construir, especificarlo con claridad, verificarlo y operarlo de forma confiable. En la práctica, el tiempo de un ingeniero de datos se desplaza hacia:

- **Especificación y descomposición:** convertir una solicitud vaga en tareas bien definidas con entradas, salidas y criterios de aceptación claros. Es lo que hace útiles a los agentes, y siempre fue la parte difícil.
- **Revisión y verificación:** leer los diffs con espíritu crítico, revisar los planes de consulta y, sobre todo, validar los resultados contra los datos. Las pruebas a nivel de datos se vuelven más importantes, no menos.
- **Ingeniería de plataforma y de contexto:** construir el entorno en el que trabajan los agentes, incluidas pruebas rápidas, CI, convenciones, capas semánticas, documentación y límites de permisos. Los equipos de datos con una buena plataforma sacan más provecho de los agentes.
- **Modelado de datos y arquitectura:** los agentes pueden escribir un esquema en estrella, pero decidir el grano, la estrategia de historia y los límites entre dominios todavía requiere entender el negocio.
- **Gobierno:** el control de acceso, el linaje, la privacidad y el control de costos importan más cuando actores no humanos consultan y modifican datos.

La parte incómoda es el nivel de entrada. Los agentes ahora hacen muchas de las tareas con las que aprendían los perfiles junior, y varios análisis de contratación reportan una contratación de nivel inicial más débil desde 2023. Las habilidades que consiguen empleo cambian en consecuencia: demostrar criterio (proyectos con pruebas, ventajas y desventajas claras, decisiones documentadas) importa más que demostrar que sabes escribir un `GROUP BY`. Los equipos que dejen de formar juniors por completo descubrirán en unos años que los seniors no aparecen de la nada.

## Lo que esperan ahora las empresas

A partir de ofertas de empleo, entrevistas y conversaciones con responsables de contratación, las expectativas para los ingenieros de datos en 2026 se ven así:

- **Se da por sentado el manejo de agentes.** Varias empresas convirtieron el uso de IA en una expectativa explícita desde 2025 (el CEO de Shopify escribió que el uso reflexivo de IA era una expectativa básica; Coinbase exigió a sus ingenieros incorporar herramientas de IA). No usarlas se ve cada vez más como no usar control de versiones.
- **Más entregas, con el mismo nivel de calidad.** Los equipos esperan más resultados por ingeniero, pero las caídas y los números equivocados se juzgan con la misma dureza de siempre. "Lo escribió el agente" no es una excusa.
- **Criterio por encima de la sintaxis.** Las entrevistas evalúan cada vez más el diseño, la depuración y la revisión de código (a menudo generado por IA) en lugar de escribir algoritmos de memoria.
- **Conciencia de seguridad y costos.** Saber dar a un agente acceso de mínimo privilegio, mantener los secretos fuera de su alcance e impedir que queme cómputo se está volviendo parte del trabajo.
- **Comunicación.** Escribir especificaciones precisas, ADR y comentarios de revisión es ahora una habilidad de productividad, porque así se delega el trabajo, a personas y a agentes.

## Buenas prácticas para adoptar agentes

Estas son las prácticas que recomendaría a un equipo de datos que adopta agentes, más o menos en orden:

1. **Empieza por la plataforma, no por la herramienta.** Una suite de pruebas rápida, CI en cada pull request, revisión de código y una ejecución de extremo a extremo con datos sintéticos son lo que hace confiable lo que produce un agente. Si solo haces una cosa, haz esta.
2. **Escribe el contexto.** Mantén en el repositorio un archivo de contexto (`CLAUDE.md`, `AGENTS.md` o equivalente) con las convenciones, la arquitectura, los comandos para ejecutar las pruebas y lo que el agente nunca debe hacer. Enlaza los ADR y los contratos de datos. Los agentes siguen mucho mejor las convenciones escritas que las no escritas.
3. **Mínimo privilegio por defecto.** Los agentes trabajan con credenciales de desarrollo, catálogos de desarrollo y conjuntos de datos pequeños. Nada de acceso de escritura a producción, roles de administrador ni claves de nube de larga duración en el entorno. Los cambios en producción pasan por el mismo pipeline de CI/CD que los cambios humanos.
4. **Aísla la ejecución.** Ejecuta los agentes en contenedores, dev containers o sandboxes en la nube con acceso de red restringido cuando sea posible. Usa los modos de permisos de la herramienta: permite leer y probar libremente, y exige aprobación para escrituras, borrados, llamadas de red y todo lo que toque la infraestructura.
5. **Trata toda entrada como no confiable.** No des a los agentes en CI acceso a secretos que no necesitan, evita `pull_request_target` en workflows con agentes en repositorios públicos, usa tokens de solo lectura para los agentes de revisión, y exige aprobación humana para cualquier acción con efectos secundarios.
6. **Revisa herramientas y dependencias.** Instala servidores MCP y extensiones solo de fuentes confiables, fija sus versiones, revisa qué permisos obtienen y verifica cada dependencia nueva que agregue un agente.
7. **Verifica con datos, no solo con revisión de código.** Toda transformación escrita por un agente recibe pruebas de datos (unicidad, no nulos, valores aceptados, conciliación del número de filas) y, en los cambios importantes, una comparación de las salidas antes y después.
8. **Mantén responsables a las personas.** Quien fusiona es dueño del cambio. Los pull requests grandes generados por agentes se dividen en partes revisables; un "LGTM" sobre 2.000 líneas no es una revisión.
9. **Controla el costo.** Define límites de gasto por usuario o equipo, da a los agentes warehouses o clústeres pequeños con apagado automático, y vigila los bucles que vuelven a ejecutar consultas costosas.
10. **Mide.** Sigue el tiempo de entrega, la tasa de fallas de cambios, los incidentes y el retrabajo antes y después de la adopción. Las encuestas sobre qué tan rápido se siente la gente no son evidencia.
11. **Decide sobre la privacidad de forma explícita.** Usa planes empresariales con términos de datos claros, documenta qué datos pueden enviarse a qué proveedor, ofrece herramientas aprobadas y enseña a las personas qué no deben pegar.

## Hacia dónde va esto

La dirección es clara aunque el ritmo no lo sea: agentes más autónomos trabajando en segundo plano en tareas bien definidas (actualizar dependencias, aumentar la cobertura de pruebas, clasificar fallas), agentes integrados en todas las plataformas de datos con acceso gobernado por el catálogo, y una parte creciente del tiempo de cada ingeniero dedicada a definir, revisar y verificar el trabajo en lugar de teclearlo.

En la ingeniería de datos, creo que los equipos que más se beneficiarán serán los que ya hicieron el trabajo poco vistoso: pruebas, CI, documentación, modelos claros y gobierno. Los agentes no reemplazan esa base; la recompensan. La mejor preparación para la próxima generación de agentes es la misma que para un nuevo colega: un código y una plataforma que hagan fácil hacer lo correcto y difícil hacer lo incorrecto.
