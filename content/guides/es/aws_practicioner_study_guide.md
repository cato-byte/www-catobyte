## Guía de estudio AWS Certified Cloud Practitioner

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio AWS Certified Cloud Practitioner: unas 200 preguntas](../../images/aws_practicioner_guide_title_img.png)

Unas 200 preguntas con respuestas breves que usé para preparar el examen AWS Certified Cloud Practitioner (CLF-C02), que aprobé en octubre de 2026. Siguen los cuatro dominios del examen: conceptos de la nube, seguridad y cumplimiento, tecnología y servicios de la nube, y facturación, precios y soporte.

La guía sigue una ruta de aprendizaje en cuatro etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones. Los servicios y los precios cambian, así que consulta la documentación de AWS antes de fiarte de una cifra.

<!-- QA -->
<!-- stage: Fundamentos de la nube -->

### Conceptos de la nube

<!-- unit: Por qué la nube -->

<!-- goals -->

- Explicar el argumento económico de la computación en la nube.
- Conectar las seis ventajas de AWS con beneficios concretos para el negocio.

<!-- concept -->

Tener tu propio centro de datos significa comprar para el pico que esperas en años, y luego pagar capacidad ociosa hasta llegar ahí. La nube invierte eso: alquilas capacidad por segundo a un proveedor cuya escala abarata cada unidad más de lo que podrías comprarla tú. El dinero pasa de inversión inicial a gasto operativo.

La velocidad viene del mismo cambio. Cuando un servidor está a una llamada de API, probar una idea cuesta minutos, y lanzar en otro continente es un cambio de configuración, no una obra de construcción.

<!-- example -->

| Pregunta | On-premises | AWS |
|---|---|---|
| Capacidad para el Black Friday | Comprar servidores para el pico | Escalar durante la semana |
| Nueva región para clientes de la UE | Alquilar espacio, enviar hardware | Desplegar en eu-west-3 |
| Modelo de costos | CapEx por adelantado | OpEx, pago por uso |

#### ¿Qué es la computación en la nube?

La entrega bajo demanda de recursos de TI (cómputo, almacenamiento, bases de datos, red, software) a través de internet, con pago por uso. En lugar de comprar y gestionar centros de datos, alquilas capacidad a un proveedor y la liberas cuando ya no la necesitas.

#### ¿Cuáles son las seis ventajas de la computación en la nube según AWS?

1. Cambiar gasto fijo (inversión de capital) por gasto variable.
2. Beneficiarse de enormes economías de escala.
3. Dejar de adivinar la capacidad.
4. Aumentar la velocidad y la agilidad.
5. Dejar de gastar dinero en operar y mantener centros de datos.
6. Llegar a todo el mundo en minutos.

#### ¿Qué ventajas tiene usar AWS en lugar de una infraestructura local?

Sin compra inicial de hardware, pago solo por lo que usas, capacidad en minutos en lugar de meses, alcance global, servicios gestionados que eliminan trabajo sin valor diferencial (parches, copias de seguridad), seguridad y certificaciones de cumplimiento integradas, y la posibilidad de experimentar barato y cerrar lo que no funciona.

#### ¿Qué diferencia hay entre CapEx y OpEx?

El gasto de capital (CapEx) es una inversión inicial en activos físicos, como servidores, que se amortiza durante años. El gasto operativo (OpEx) es el gasto continuo en servicios. La nube convierte la mayor parte del CapEx de TI en OpEx.

#### ¿Qué significa "economías de escala" en la nube?

AWS compra hardware, energía y red a una escala que ningún cliente alcanza por separado, así que su costo por unidad es menor. Parte del ahorro se traslada a los clientes con bajadas de precio, que AWS ha aplicado muchas veces.

#### ¿Qué es la agilidad en el contexto de la nube?

La velocidad a la que puedes disponer de recursos y probar ideas nuevas. Recursos que tardaban semanas en llegar están disponibles en minutos, así que el costo y el tiempo de experimentar bajan mucho.

#### ¿Qué significa "llegar a todo el mundo en minutos"?

Que puedes desplegar una aplicación en regiones de AWS de todo el mundo con unos pocos clics o llamadas a la API, y dar menor latencia a los usuarios sin construir centros de datos en otros países.

<!-- challenge -->

El CFO de una startup pregunta por qué no comprar servidores, ya que "alquilar siempre sale más caro al final". Da dos argumentos en términos simples.

<!-- solution -->

Pagarían por adelantado capacidad que quizá nunca usen, y equivocarse en cualquier dirección sale caro. Con AWS pagan lo que usan, escalan con la demanda y guardan caja para el negocio; los savings plans bajan aún más los precios cuando el uso es predecible.

<!-- takeaways -->

- La nube cambia CapEx inicial por OpEx variable.
- Las economías de escala bajan los precios unitarios de AWS.
- Agilidad: recursos en minutos, regiones en todo el mundo.

<!-- unit: Modelos de servicio y de despliegue -->

<!-- goals -->

- Distinguir IaaS, PaaS y SaaS con ejemplos de AWS.
- Comparar despliegues en la nube, híbridos y on-premises.

<!-- concept -->

Los servicios en la nube difieren en cuánto opera AWS por ti. Con servicios de infraestructura recibes máquinas virtuales y administras todo lo que corre en ellas. Con servicios de plataforma traes el código y AWS opera los servidores. Con software como servicio solo usas la aplicación. Los servicios gestionados y serverless quedan del lado de la plataforma: menos que operar, menos que controlar.

Los modelos de despliegue responden otra pregunta: dónde corren las cosas. Muchas empresas combinan nube y on-premises durante años en una migración.

<!-- example -->

| Tú administras | IaaS (EC2) | PaaS (Elastic Beanstalk) | SaaS |
|---|---|---|---|
| Código de la aplicación | Sí | Sí | No |
| Parches del sistema operativo | Sí | No | No |
| Hardware | No | No | No |

#### ¿Qué modelos de implementación de la nube admite AWS?

- **Nube (nativo de la nube):** todo se ejecuta en la nube pública.
- **Local (nube privada):** recursos en tu propio centro de datos, a menudo con virtualización y herramientas de gestión. AWS Outposts lleva la infraestructura de AWS a tus instalaciones.
- **Híbrido:** recursos en la nube conectados a infraestructura local, por ejemplo durante una migración o para datos que deben quedarse en casa.

#### ¿Qué significan IaaS, PaaS y SaaS? Da ejemplos de AWS.

- **IaaS (infraestructura como servicio):** obtienes máquinas virtuales, almacenamiento y redes, y gestionas el sistema operativo y todo lo que está por encima. Ejemplo: Amazon EC2.
- **PaaS (plataforma como servicio):** el proveedor gestiona la infraestructura y la plataforma, tú despliegas código. Ejemplo: AWS Elastic Beanstalk.
- **SaaS (software como servicio):** una aplicación completa que se usa por internet. Ejemplos: Amazon WorkMail, Amazon Chime, Amazon QuickSight.

#### ¿Qué es un servicio gestionado?

Un servicio en el que AWS opera la infraestructura y el software subyacentes (aprovisionamiento, parches, copias de seguridad, escalado) y tú solo lo usas. Amazon RDS es una base de datos gestionada. Ejecutar una base de datos en EC2 no lo es: todo eso lo haces tú.

#### ¿Qué significa "serverless" (sin servidor)?

Ejecutas código o usas un servicio sin aprovisionar ni gestionar servidores. La capacidad escala automáticamente y pagas por el uso real. Ejemplos: AWS Lambda, Amazon S3, Amazon DynamoDB, AWS Fargate, Amazon Athena.

<!-- challenge -->

Un equipo corre PostgreSQL en EC2 y pierde horas en parches y backups. ¿Qué cambio de modelo ayudaría y a qué renuncian?

<!-- solution -->

Pasar a una base gestionada (Amazon RDS for PostgreSQL), donde AWS se encarga de parches, backups y failover. Renuncian al acceso al sistema operativo y a parte de la configuración de bajo nivel.

<!-- takeaways -->

- IaaS, PaaS y SaaS difieren en lo que tú administras.
- Los servicios gestionados y serverless trasladan la operación a AWS.
- Lo híbrido combina nube y on-premises.

<!-- unit: Elasticidad y escalado -->

<!-- goals -->

- Distinguir elasticidad de escalabilidad.
- Elegir entre escalado vertical y horizontal.

<!-- concept -->

La escalabilidad es la capacidad de atender más carga sumando recursos. La elasticidad agrega una dimensión temporal: los recursos crecen y se reducen automáticamente con la demanda, así no pagas el pico todo el año.

Cómo escalas importa. Una máquina más grande es simple, pero tiene techo y sigue siendo un único punto de fallo. Más máquinas detrás de un balanceador escalan más lejos y sobreviven a fallos, pero la aplicación debe permitir que cualquier instancia atienda cualquier petición.

<!-- example -->

```text
Vertical:   t3.large ─► m7i.2xlarge         (bigger box, restart, limit)
Horizontal: 2 × m7i.large ─► 8 × m7i.large  (more boxes, load balancer, no limit)
```

#### ¿Qué es la elasticidad?

La capacidad de obtener recursos cuando los necesitas y liberarlos cuando no, siguiendo la demanda de forma automática. Ejemplo: un grupo de Auto Scaling que añade instancias EC2 durante un pico de tráfico y las retira después.

#### ¿Qué es la escalabilidad?

La capacidad de un sistema de soportar una carga creciente añadiendo recursos. Escalar verticalmente significa recursos más grandes, escalar horizontalmente significa más recursos. La elasticidad es escalabilidad que además reduce los recursos automáticamente.

#### ¿Qué diferencia hay entre escalar vertical y horizontalmente?

Escalar verticalmente sustituye un recurso por otro más grande (un tipo de instancia mayor). Es sencillo, pero tiene un límite y suele requerir un reinicio. Escalar horizontalmente añade más recursos del mismo tamaño detrás de un balanceador de carga. No tiene límite práctico y mejora la disponibilidad.

<!-- challenge -->

El tráfico de una tienda en línea se triplica cada tarde y cae de noche. ¿Qué enfoque sugieres?

<!-- solution -->

Escalado horizontal con EC2 Auto Scaling detrás de un balanceador: agregar instancias en la tarde y quitarlas de noche. Eso es elasticidad, y significa pagar la capacidad pico solo cuando se usa.

<!-- takeaways -->

- La escalabilidad atiende el crecimiento; la elasticidad sigue la demanda.
- Vertical es simple pero limitado; horizontal escala más lejos.
- Los diseños elásticos evitan pagar capacidad pico ociosa.

<!-- unit: Disponibilidad y recuperación -->

<!-- goals -->

- Definir alta disponibilidad, tolerancia a fallos y recuperación ante desastres.
- Elegir una estrategia de DR a partir del RTO y el RPO.

<!-- concept -->

Los fallos son seguros; la pregunta es cuánto cuestan. La alta disponibilidad acorta la caída cuando fallan piezas; la tolerancia a fallos mantiene el sistema funcionando sin ninguna interrupción, a mayor precio. La recuperación ante desastres cubre los eventos grandes, como perder una región entera.

Dos números enmarcan cada decisión de DR: cuánto tiempo puedes estar caído (RTO) y cuántos datos puedes perder (RPO). Números más bajos exigen más recursos en espera, así que el costo sube a medida que bajan.

<!-- example -->

| Estrategia | RTO / RPO | Costo |
|---|---|---|
| Backup y restauración | Horas / horas | $ |
| Pilot light | Decenas de minutos | $$ |
| Warm standby | Minutos | $$$ |
| Multi-sitio activo/activo | Casi cero | $$$$ |

#### ¿Qué es la alta disponibilidad?

La capacidad de un sistema de seguir funcionando con un tiempo de inactividad mínimo cuando fallan componentes. En AWS suele significar ejecutar en varias zonas de disponibilidad, para que la pérdida de un centro de datos no detenga la aplicación.

#### ¿Qué es la tolerancia a fallos?

La capacidad de seguir funcionando sin interrupción cuando falla un componente, normalmente con componentes redundantes que toman el relevo automáticamente. Es una propiedad más fuerte que la alta disponibilidad, que puede aceptar una interrupción breve.

#### ¿Qué es la recuperación ante desastres, y qué son el RTO y el RPO?

La recuperación ante desastres (DR) es el conjunto de planes para restaurar una carga de trabajo tras un fallo grave. El RTO (Recovery Time Objective) es el tiempo máximo de inactividad aceptable. El RPO (Recovery Point Objective) es la pérdida de datos máxima aceptable, medida en tiempo.

#### ¿Cuáles son las cuatro estrategias de recuperación ante desastres en AWS, de la más barata a la más rápida?

1. **Copia de seguridad y restauración:** se hacen copias de los datos y la infraestructura se crea tras el desastre. RTO de horas.
2. **Piloto encendido (pilot light):** un núcleo mínimo (por ejemplo una base de datos replicada) funciona siempre, el resto se arranca bajo demanda.
3. **Espera en caliente (warm standby):** una copia reducida pero completamente funcional se ejecuta y se amplía al conmutar.
4. **Multisitio activo/activo:** producción completa en dos o más regiones. RTO casi nulo, costo máximo.

<!-- challenge -->

Un sistema de nómina puede estar caído 8 horas y perder como máximo 1 hora de datos. ¿Qué estrategia de DR encaja y por qué no una más cara?

<!-- solution -->

Backup y restauración con backups cada hora (o pilot light si las restauraciones tardan mucho) cumple un RTO de 8 horas y un RPO de 1 hora. Warm standby o multi-sitio costarían mucho más por una velocidad de recuperación que el negocio no necesita.

<!-- takeaways -->

- La alta disponibilidad limita la caída; la tolerancia a fallos la evita.
- El RTO es el tiempo para recuperarse; el RPO, los datos que puedes perder.
- Recuperarse más rápido cuesta más recursos en espera.

<!-- unit: Planear una migración -->

<!-- goals -->

- Describir el AWS Cloud Adoption Framework.
- Elegir una estrategia de migración entre las 7 R.

<!-- concept -->

Mudarse a la nube es tanto un cambio organizacional como técnico. El Cloud Adoption Framework estructura el trabajo en perspectivas, del negocio y las personas a la seguridad y la operación, para que habilidades y procesos cambien junto con los servidores.

Para cada aplicación, las 7 R dan las opciones, de dejarla como está a reescribirla. La mayoría de empresas usa varias: rehost rápido para salir de un centro de datos y luego refactorizar los sistemas donde las funciones de la nube compensan.

<!-- example -->

| Aplicación | Estrategia |
|---|---|
| Herramienta vieja de reportes que nadie usa | Retire |
| ERP con una restricción de licencia rígida | Retain (por ahora) |
| App web en VMs | Rehost a EC2 |
| MySQL autogestionado | Replatform a RDS |
| Monolito que necesita escalar | Refactor |

#### ¿Qué es el AWS Cloud Adoption Framework (AWS CAF)?

Una guía que ayuda a las organizaciones a planificar su transformación a la nube. Agrupa las capacidades en seis perspectivas: Negocio, Personas, Gobernanza (orientadas al negocio) y Plataforma, Seguridad, Operaciones (técnicas).

#### ¿Qué son las 7 R de la migración?

Retirar (Retire), Conservar (Retain), Realojar (Rehost, "lift and shift"), Reubicar (Relocate, por ejemplo VMware Cloud on AWS), Recomprar (Repurchase, pasar a SaaS), Redefinir la plataforma (Replatform, "lift, tinker and shift", como pasar a RDS) y Refactorizar o rediseñar (Refactor, reconstruir de forma nativa para la nube).

<!-- challenge -->

Una empresa debe dejar su centro de datos en 6 meses y tiene 300 aplicaciones. ¿Qué estrategia usarías para la mayoría y qué viene después?

<!-- solution -->

Rehost para la mayoría (lift and shift), porque es lo más rápido, y retire o retain para el resto. Tras la salida, refactorizar o hacer replatform de las aplicaciones donde los servicios gestionados o el escalado den beneficios claros.

<!-- takeaways -->

- El CAF cubre negocio, personas, gobierno, plataforma, seguridad y operación.
- Las 7 R van de retire a refactor.
- Primero rehost, luego optimizar es un camino común.

### Infraestructura global y Well-Architected Framework

<!-- unit: Regiones y zonas de disponibilidad -->

<!-- goals -->

- Describir regiones, zonas de disponibilidad y servicios globales frente a regionales.
- Elegir una región según cumplimiento, latencia, servicios y precio.

<!-- concept -->

AWS construye su infraestructura en capas de aislamiento. Una región es un área geográfica; dentro, las zonas de disponibilidad son centros de datos separados con su propia energía y red, lo bastante cerca para conexiones rápidas pero lo bastante lejos para que un evento no los afecte a todos.

Ese diseño guía la arquitectura: repartir entre zonas protege contra la caída de un centro de datos, y repartir entre regiones contra un evento regional. Elegir la región empieza por los requisitos legales, luego latencia, disponibilidad de servicios y precio.

<!-- example -->

```text
Region eu-west-3 (Paris)
 ├─ AZ eu-west-3a ── app + DB primary
 ├─ AZ eu-west-3b ── app + DB standby
 └─ AZ eu-west-3c ── app
```

#### ¿Cómo está estructurada la infraestructura global de AWS?

En regiones (zonas geográficas separadas), cada una formada por varias zonas de disponibilidad (grupos aislados de centros de datos). Las ubicaciones de borde (edge locations) y las cachés de borde regionales sirven CloudFront y Route 53 cerca de los usuarios. Las Local Zones, las Wavelength Zones y Outposts acercan AWS a los usuarios o a sus instalaciones.

#### ¿Qué diferencia hay entre una región de AWS y una zona de disponibilidad?

Una región es una zona geográfica, como eu-west-3 (París), que contiene varias zonas de disponibilidad. Una zona de disponibilidad (AZ) es uno o varios centros de datos con energía, red y conectividad redundantes, físicamente separados de las demás AZ de la región pero unidos a ellas por una red de baja latencia.

#### ¿Cuántas zonas de disponibilidad tiene una región?

Al menos tres en la mayoría de las regiones (las regiones nuevas se construyen con tres o más). Desplegar en al menos dos AZ es la base de la alta disponibilidad.

#### ¿Qué cuatro factores hay que tener en cuenta al elegir una región?

1. **Cumplimiento y residencia de datos:** la ley puede obligar a que los datos se queden en un país.
2. **Proximidad a los usuarios:** menor latencia.
3. **Disponibilidad de servicios:** no todos los servicios o funciones están en todas las regiones.
4. **Precio:** el mismo servicio puede costar distinto según la región.

#### ¿Los servicios son globales o regionales?

La mayoría son regionales: los recursos viven en una región. Algunos son globales: IAM, Route 53, CloudFront, AWS Organizations y WAF para CloudFront. Otros, como las subredes de EC2 y los volúmenes EBS, están limitados a una zona de disponibilidad.

<!-- challenge -->

Una empresa francesa de salud quiere baja latencia para usuarios franceses y debe mantener los datos de pacientes en Francia. ¿Qué región y qué diseño sugieres?

<!-- solution -->

París (eu-west-3), que cumple la residencia de datos, con la aplicación y la base repartidas en al menos dos zonas de disponibilidad para alta disponibilidad. Confirmar que los servicios necesarios estén disponibles ahí.

<!-- takeaways -->

- Las regiones contienen varias zonas de disponibilidad aisladas.
- Reparte entre zonas para disponibilidad y entre regiones para desastres.
- El cumplimiento va primero al elegir región.

<!-- unit: Infraestructura en el borde y on-premises -->

<!-- goals -->

- Explicar edge locations, Local Zones, Wavelength y Outposts.
- Asociar cada uno a una necesidad de latencia o ubicación.

<!-- concept -->

No todo puede correr en una región. El contenido y las respuestas DNS son más rápidos desde edge locations cerca de los usuarios. Algunas aplicaciones necesitan latencias de un dígito de milisegundos hacia una ciudad o una red 5G, que dan Local Zones y Wavelength. Otras deben quedarse en tu edificio por regulación o latencia, y Outposts lleva hardware de AWS hasta ti.

Cada opción extiende los mismos servicios y APIs de AWS a un lugar nuevo.

<!-- example -->

| Necesidad | Opción |
|---|---|
| Cachear imágenes cerca de usuarios en todo el mundo | Edge locations (CloudFront) |
| Edición de video cerca de Los Ángeles | Local Zone |
| Juego móvil sobre 5G | Wavelength |
| Sistemas de fábrica en sitio | Outposts |

#### ¿Qué es una ubicación de borde (edge location)?

Un emplazamiento que ejecuta las cachés de CloudFront y el DNS de Route 53 (y servicios como Lambda@Edge) cerca de los usuarios finales. Hay muchas más ubicaciones de borde que regiones.

#### ¿Qué es una Local Zone?

Una extensión de una región situada cerca de una gran ciudad, que ejecuta algunos servicios (como EC2 y EBS) para dar una latencia de milisegundos de un dígito a los usuarios de esa zona.

#### ¿Qué es AWS Wavelength?

Infraestructura integrada en las redes 5G de los operadores de telecomunicaciones, para que las aplicaciones lleguen a los dispositivos móviles con una latencia muy baja.

#### ¿Qué es AWS Outposts?

Racks de hardware gestionado por AWS instalados en tu propio centro de datos, que ejecutan servicios de AWS con las mismas API y herramientas. Se usan para baja latencia con sistemas locales, procesamiento local de datos o residencia de datos.

<!-- challenge -->

Un banco debe mantener un sistema de trading en su propio centro de datos pero quiere las APIs y herramientas de AWS. ¿Qué servicio encaja?

<!-- solution -->

AWS Outposts: racks gestionados por AWS instalados on-premises que corren servicios de AWS con las mismas APIs, conectados a una región principal.

<!-- takeaways -->

- Las edge locations sirven CloudFront y Route 53 cerca de los usuarios.
- Local Zones y Wavelength acercan el cómputo a ciudades y 5G.
- Outposts corre AWS en tu centro de datos.

<!-- unit: Los pilares de Well-Architected -->

<!-- goals -->

- Nombrar los seis pilares del Well-Architected Framework.
- Resumir qué le pide cada pilar a una carga de trabajo.

<!-- concept -->

El Well-Architected Framework es una forma estructurada de preguntar si una carga está bien construida. Divide "bien" en seis preocupaciones que a menudo tiran en direcciones opuestas: operarla con fluidez, mantenerla segura, hacerla confiable, usar los recursos con eficiencia, gastar con criterio y reducir el impacto ambiental.

El valor está en los equilibrios. Una revisión con los pilares los hace explícitos, por ejemplo pagar más por confiabilidad multi-AZ o aceptar menos rendimiento por menor costo.

<!-- example -->

| Pilar | Pregunta típica |
|---|---|
| Excelencia operativa | ¿Cómo despliegas y aprendes de los incidentes? |
| Seguridad | ¿Cómo gestionas identidades y proteges los datos? |
| Confiabilidad | ¿Cómo se recupera la carga de un fallo? |
| Eficiencia del rendimiento | ¿Cómo eliges los recursos correctos? |
| Optimización de costos | ¿Cómo sabes qué gastas y por qué? |
| Sostenibilidad | ¿Cómo reduces el uso de recursos? |

#### ¿Qué es el AWS Well-Architected Framework?

Un conjunto de buenas prácticas y preguntas para diseñar y revisar cargas de trabajo en AWS, organizado en seis pilares. La herramienta Well-Architected Tool de la consola hace una revisión estructurada de una carga de trabajo.

#### ¿Cuáles son los seis pilares del Well-Architected Framework?

Excelencia operativa, Seguridad, Fiabilidad, Eficiencia del rendimiento, Optimización de costos y Sostenibilidad.

#### ¿En qué se centra el pilar de Excelencia operativa?

En ejecutar y supervisar sistemas y mejorar continuamente los procesos: operaciones como código, cambios pequeños y reversibles, aprender de los fallos y anticiparlos.

#### ¿En qué se centra el pilar de Seguridad?

En proteger datos, sistemas y activos: una base sólida de identidades, trazabilidad, seguridad en todas las capas, controles automatizados, cifrado en tránsito y en reposo, y preparación ante incidentes de seguridad.

#### ¿En qué se centra el pilar de Fiabilidad?

En que una carga de trabajo cumpla su función correctamente y de forma constante: recuperación automática ante fallos, pruebas de los procedimientos de recuperación, escalado horizontal y gestión de cambios mediante automatización.

#### ¿En qué se centra el pilar de Eficiencia del rendimiento?

En usar los recursos de forma eficiente a medida que cambian la demanda y la tecnología: elegir los tipos de recursos adecuados, usar servicios gestionados y serverless, desplegar globalmente en minutos y experimentar a menudo.

#### ¿En qué se centra el pilar de Optimización de costos?

En aportar valor al menor precio: pagar solo por lo que se usa, medir la eficiencia, no gastar en trabajo sin valor diferencial, y analizar y atribuir el gasto.

#### ¿En qué se centra el pilar de Sostenibilidad?

En minimizar el impacto ambiental de las cargas de trabajo: conocer tu impacto, maximizar la utilización, usar servicios gestionados y hardware más eficiente, y reducir los recursos que necesitan los usuarios finales.

<!-- challenge -->

Un equipo corre su base de producción en una sola instancia sin backups para ahorrar. ¿Qué pilares descuida y cuál es el arreglo más barato?

<!-- solution -->

Sobre todo Confiabilidad (punto único de fallo, sin recuperación) a favor de Optimización de costos. El arreglo más barato son backups automáticos con recuperación a un punto en el tiempo; Multi-AZ agrega disponibilidad a mayor costo.

<!-- takeaways -->

- Seis pilares: operación, seguridad, confiabilidad, rendimiento, costo y sostenibilidad.
- Los pilares a menudo compiten entre sí.
- Las revisiones hacen explícitos esos equilibrios.

<!-- unit: Principios de diseño -->

<!-- goals -->

- Aplicar "diseñar para fallar", el bajo acoplamiento y las aplicaciones sin estado.
- Explicar por qué se recomienda la infraestructura como código.

<!-- concept -->

Algunos principios se repiten en todos los pilares. Espera que cualquier componente falle, así que construye redundancia y recuperación automática. Conecta los componentes con colas y eventos para que una parte lenta no frene al resto. Mantén sin estado los servidores de aplicación para que cualquiera pueda reemplazarse.

La infraestructura como código hace todo esto repetible: los entornos se vuelven plantillas revisadas y versionadas, y reconstruir tras un fallo es volver a ejecutar la plantilla.

<!-- example -->

```text
Tightly coupled:  web ─► order service ─► payment API (down → orders fail)
Loosely coupled:  web ─► SQS queue ─► order workers ─► payment API (down → orders wait)
```

#### ¿Qué significa "diseñar para el fallo"?

Asumir que cualquier componente puede fallar y construir el sistema para que siga funcionando cuando ocurra: varias AZ, comprobaciones de estado, sustitución automática, reintentos y componentes desacoplados.

#### ¿Qué es el acoplamiento débil y qué servicios ayudan a lograrlo?

Diseñar los componentes para que un fallo o una lentitud en uno no se propague a los demás. Las colas (Amazon SQS), las notificaciones (Amazon SNS), los buses de eventos (Amazon EventBridge) y los balanceadores de carga permiten que los componentes se comuniquen sin depender directamente unos de otros.

#### ¿Qué diferencia hay entre una aplicación sin estado y una con estado?

Un componente sin estado no guarda datos de sesión entre solicitudes, así que cualquier instancia puede atender cualquier solicitud y se pueden añadir o quitar instancias libremente. El estado se guarda en otro sitio (DynamoDB, ElastiCache, S3). Los componentes con estado son más difíciles de escalar horizontalmente.

#### ¿Qué es la infraestructura como código y por qué la recomienda el Well-Architected Framework?

Definir la infraestructura en plantillas o código versionados (CloudFormation, AWS CDK) en lugar de clics manuales en la consola. Los entornos se vuelven reproducibles, revisables y rápidos de reconstruir, lo que favorece la excelencia operativa y la fiabilidad.

<!-- challenge -->

Los usuarios pierden la sesión cada vez que Auto Scaling quita una instancia. ¿Cuál es la causa y el arreglo?

<!-- solution -->

Las sesiones se guardan en las instancias, así que la aplicación tiene estado. Mueve los datos de sesión a un almacén compartido (ElastiCache o DynamoDB) para que cualquier instancia atienda a cualquier usuario.

<!-- takeaways -->

- Diseña para fallar: redundancia y recuperación automática.
- Colas y eventos desacoplan los componentes.
- Servidores sin estado e IaC facilitan los reemplazos.

<!-- stage: Seguridad -->

### Seguridad, modelo de responsabilidad compartida e IAM

<!-- unit: Responsabilidad compartida -->

<!-- goals -->

- Explicar qué asegura AWS y qué asegura el cliente.
- Mostrar cómo cambian las responsabilidades entre EC2, RDS y S3.

<!-- concept -->

La seguridad en AWS se divide por una línea. AWS asegura la nube en sí: edificios, hardware, la capa de virtualización y las entrañas de los servicios gestionados. Tú aseguras lo que pones en ella: datos, identidades, configuración y todo lo que instales.

Dónde cae la línea depende del servicio. Cuanto más gestiona AWS, menos haces tú, pero datos, accesos y configuración siempre siguen siendo tuyos.

<!-- example -->

| Tarea | EC2 | RDS | S3 |
|---|---|---|---|
| Seguridad física | AWS | AWS | AWS |
| Parches del sistema operativo | Cliente | AWS | AWS |
| Parches del motor de base de datos | Cliente | AWS | n/a |
| Datos, políticas de acceso, configuración de cifrado | Cliente | Cliente | Cliente |

#### ¿Qué es el modelo de responsabilidad compartida de AWS?

La seguridad se reparte entre AWS y el cliente. AWS es responsable de la seguridad **de** la nube (hardware, infraestructura global, instalaciones, capa de virtualización, software de los servicios gestionados). El cliente es responsable de la seguridad **en** la nube (datos, identidades y permisos, sistemas operativos y aplicaciones que ejecuta, configuración de red y cortafuegos, opciones de cifrado).

#### ¿Cómo cambia el modelo de responsabilidad compartida entre EC2, RDS y S3?

Cuanto más gestionado es el servicio, menos hace el cliente. En EC2 aplicas los parches del sistema operativo invitado y del software. En RDS, AWS parchea el sistema operativo y el motor de base de datos, y tú gestionas usuarios, acceso de red y datos. En S3 gestionas los datos, las políticas de acceso y el cifrado.

#### ¿Quién es responsable de parchear el sistema operativo de una instancia EC2?

El cliente. AWS parchea el hipervisor y los servidores físicos. Herramientas como AWS Systems Manager Patch Manager ayudan a automatizar los parches del sistema invitado.

#### ¿Quién es responsable de la seguridad física de los centros de datos?

AWS. Los clientes nunca tienen acceso físico a los centros de datos de AWS.

#### ¿Qué responsabilidades son compartidas por ambos?

La gestión de parches (AWS parchea la infraestructura, el cliente sus sistemas invitados y aplicaciones), la gestión de la configuración, y la concienciación y formación (cada uno forma a su personal).

<!-- challenge -->

Un bucket S3 de una empresa quedó público por error y se filtraron datos. Según el modelo de responsabilidad compartida, ¿de quién fue el fallo y qué control lo habría evitado?

<!-- solution -->

Del cliente: la configuración de acceso del bucket es su responsabilidad. S3 Block Public Access a nivel de cuenta (más SCPs en Organizations y reglas de Config) habría impedido que los buckets se volvieran públicos.

<!-- takeaways -->

- AWS asegura "la" nube; tú aseguras lo que hay "en" la nube.
- Los servicios más gestionados trasladan más trabajo a AWS.
- Datos, identidades y configuración siempre son tuyos.

<!-- unit: Usuario root e identidades de IAM -->

<!-- goals -->

- Proteger el usuario root y conocer sus tareas exclusivas.
- Elegir entre usuarios, grupos y roles de IAM.

<!-- concept -->

Toda cuenta empieza con un usuario root que puede hacer cualquier cosa, incluso cerrar la cuenta. Como no se puede limitar, debe guardarse bajo llave con MFA y usarse solo para las pocas tareas que lo exigen.

El acceso diario pasa por IAM. Los usuarios representan personas o aplicaciones con credenciales de larga vida; los grupos hacen manejables los permisos; los roles dan credenciales temporales a quien tenga confianza para asumirlos. Los roles son la opción más segura, sobre todo para aplicaciones.

<!-- example -->

```text
root user        ─► MFA, no access keys, used only for root-only tasks
group: analysts  ─► policy AnalystsReadOnly ◄─ users ana, luis
role: ec2-app    ─► policy AppS3Access      ◄─ assumed by EC2 instances
```

#### ¿Qué es AWS Identity and Access Management (IAM)?

El servicio global que controla quién puede iniciar sesión en una cuenta de AWS (autenticación) y qué puede hacer (autorización). Gestiona usuarios, grupos, roles y políticas sin costo adicional.

#### ¿Qué es el usuario raíz y cómo debe protegerse?

La identidad creada con la cuenta, con acceso ilimitado a todo, incluida la facturación y el cierre de la cuenta. Protégelo con una contraseña robusta y MFA, elimina sus claves de acceso y úsalo solo para las pocas tareas que lo requieren.

#### ¿Qué tareas solo puede hacer el usuario raíz?

Por ejemplo: cambiar el correo o el nombre de la cuenta, cerrar la cuenta, cambiar el plan de AWS Support, restaurar los permisos de IAM cuando el único administrador se ha bloqueado a sí mismo, y algunos ajustes de facturación.

#### ¿Qué es un usuario de IAM?

Una identidad que representa a una persona o aplicación, con credenciales de larga duración: una contraseña para la consola y/o claves de acceso para la API. AWS recomienda, para las personas, credenciales federadas o temporales en lugar de usuarios de IAM siempre que sea posible.

#### ¿Qué es un grupo de IAM?

Un conjunto de usuarios de IAM. Las políticas asociadas al grupo se aplican a todos sus miembros, lo que simplifica la gestión de permisos. Los grupos no se pueden anidar y no son identidades.

#### ¿Qué es un rol de IAM?

Una identidad con permisos pero sin credenciales de larga duración. Una entidad de confianza (un servicio de AWS como EC2 o Lambda, un usuario, otra cuenta o una identidad federada) asume el rol y recibe credenciales temporales de AWS STS.

#### ¿Por qué una instancia EC2 debe usar un rol en lugar de claves de acceso?

Las claves guardadas en la instancia pueden filtrarse y hay que rotarlas a mano. Un rol proporciona credenciales temporales que se renuevan automáticamente a través de los metadatos de la instancia, sin guardar nada secreto en disco.

<!-- challenge -->

Un desarrollador guarda claves de acceso en un archivo de configuración de una instancia EC2 para que la app lea S3. ¿Qué recomiendas?

<!-- solution -->

Crear un rol IAM con lectura sobre el bucket necesario, asociarlo a la instancia mediante un instance profile, quitar las claves del archivo y desactivarlas. La app recibe automáticamente credenciales temporales rotadas.

<!-- takeaways -->

- Protege el root con MFA; no lo uses a diario.
- Los grupos manejan permisos de usuarios; los roles dan credenciales temporales.
- Las aplicaciones en AWS deben usar roles, no claves.

<!-- unit: Políticas y evaluación de permisos -->

<!-- goals -->

- Leer una sentencia de política IAM y sus partes.
- Predecir el resultado cuando las políticas permiten y deniegan.

<!-- concept -->

Los permisos en AWS se escriben como políticas JSON que permiten o deniegan acciones sobre recursos, opcionalmente bajo condiciones. Los recursos se nombran con ARNs, así una política puede apuntar a un solo bucket o a una sola tabla.

La evaluación sigue una regla simple: todo empieza denegado, un allow abre el acceso y un deny explícito siempre gana. El mínimo privilegio significa escribir los allow tan estrechos como lo exija la tarea y ampliarlos solo cuando haga falta.

<!-- example -->

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::sales-reports/*",
    "Condition": {"Bool": {"aws:SecureTransport": "true"}}
  }]
}
```

#### ¿Qué es una política de IAM?

Un documento JSON que permite o deniega acciones sobre recursos, con condiciones opcionales. Las políticas basadas en identidades se asocian a usuarios, grupos o roles. Las políticas basadas en recursos (como las políticas de bucket de S3) se asocian a recursos.

#### ¿Qué contiene una instrucción de política de IAM?

`Effect` (Allow o Deny), `Action` (por ejemplo `s3:GetObject`), `Resource` (un ARN) y, opcionalmente, `Condition` (por ejemplo una IP de origen o MFA obligatoria). Las políticas basadas en recursos tienen además un `Principal`.

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-bucket/reports/*"
  }]
}
```

#### ¿Cómo evalúa IAM los permisos cuando las políticas entran en conflicto?

Todo está denegado por defecto. Un Allow explícito concede el acceso, pero un Deny explícito en cualquier sitio gana siempre a cualquier Allow.

#### ¿Qué es el principio de mínimo privilegio?

Conceder solo los permisos necesarios para una tarea, y nada más. Empieza con poco y añade permisos según haga falta. IAM Access Analyzer puede generar políticas a partir de la actividad real.

#### ¿Qué es un ARN?

Un Amazon Resource Name identifica un recurso de forma única: `arn:partition:service:region:account-id:resource`, por ejemplo `arn:aws:s3:::my-bucket`.

<!-- challenge -->

Un usuario tiene una política de grupo que permite `s3:*` en todos los buckets y una política propia que deniega `s3:DeleteObject` en `finance-*`. ¿Puede borrar objetos en `finance-2026`?

<!-- solution -->

No. El deny explícito se impone a cualquier allow, así que se rechazan los borrados en buckets que coinciden con `finance-*`, mientras siguen permitidas las demás acciones de S3 ahí.

<!-- takeaways -->

- Las políticas permiten o deniegan acciones sobre recursos, con condiciones.
- Denegado por defecto; allow concede; deny explícito siempre gana.
- Mínimo privilegio: empieza estrecho y amplía cuando haga falta.

<!-- unit: Credenciales e higiene de la cuenta -->

<!-- goals -->

- Asegurar el inicio de sesión con MFA y políticas de contraseñas.
- Auditar credenciales y permisos sin usar.

<!-- concept -->

La mayoría de los compromisos de cuentas empiezan con una credencial robada. El MFA hace insuficiente una contraseña robada, las políticas de contraseñas reducen las débiles, y las claves de acceso, que nunca expiran solas, deben ser pocas y rotarse.

La higiene también es mirar atrás: quién sigue teniendo claves viejas, quién tiene permisos que nunca usa. El credential report y Access Advisor responden esas preguntas para que puedas quitar lo que sobra.

<!-- example -->

```bash
aws iam generate-credential-report
aws iam get-credential-report --query Content --output text | base64 -d \
  | cut -d, -f1,4,9,11 | column -t -s,      # user, password, key 1 active, key 1 last rotated
```

#### ¿Qué es la autenticación multifactor (MFA) y qué dispositivos admite AWS?

Un segundo factor además de la contraseña. AWS admite llaves de acceso (passkeys) y llaves de seguridad FIDO2, aplicaciones de autenticación virtuales y tokens TOTP físicos.

#### ¿Qué son las claves de acceso?

Un par formado por un ID de clave de acceso y una clave de acceso secreta, usado para firmar solicitudes programáticas (CLI, SDK). Son credenciales de larga duración: no las incluyas nunca en el código, rótalas y, siempre que puedas, usa roles o IAM Identity Center.

#### ¿Qué es una política de contraseñas en IAM?

Reglas de la cuenta para las contraseñas de los usuarios de IAM: longitud mínima, tipos de caracteres obligatorios, caducidad e impedir su reutilización.

#### ¿Qué es el informe de credenciales de IAM?

Un CSV a nivel de cuenta que lista todos los usuarios y el estado de sus credenciales: contraseñas, claves de acceso, MFA y fechas de último uso. Útil para auditorías.

#### ¿Qué es IAM Access Advisor?

Una vista que muestra para qué servicios tiene permisos un usuario, grupo o rol y cuándo los usó por última vez. Ayuda a eliminar permisos no utilizados.

<!-- challenge -->

Una auditoría encuentra un usuario con permisos de administrador que no inicia sesión hace un año pero tiene una clave de acceso activa. ¿Qué haces?

<!-- solution -->

Revisar el último uso de la clave; desactivarla y luego borrar la clave y el usuario si ya no se necesita. Usar Access Advisor en las identidades que queden para quitar permisos sin uso.

<!-- takeaways -->

- El MFA bloquea la mayoría de compromisos por contraseña.
- Las claves de acceso no expiran; minimízalas y rótalas.
- Credential reports y Access Advisor muestran qué quitar.

<!-- unit: Federación y credenciales temporales -->

<!-- goals -->

- Dar acceso al personal mediante IAM Identity Center y federación.
- Explicar cómo emite STS credenciales temporales.

<!-- concept -->

En empresas con muchas cuentas y mucha gente, crear usuarios IAM en todas partes no escala y deja credenciales olvidadas cuando alguien se va. La federación permite iniciar sesión con la identidad corporativa, e IAM Identity Center la asigna a permission sets en varias cuentas.

Por debajo, STS emite credenciales de corta vida cada vez que se asume un rol. Las credenciales temporales expiran solas, por eso son más seguras que las claves de larga vida.

<!-- example -->

```bash
aws sso login --profile data-dev                  # corporate sign-in via Identity Center
aws sts get-caller-identity --profile data-dev    # temporary role credentials
```

#### ¿Qué es AWS IAM Identity Center?

El sucesor de AWS Single Sign-On. Gestiona de forma centralizada el acceso de los empleados a varias cuentas de AWS y aplicaciones de negocio, con su propio directorio o un proveedor de identidades externo (Microsoft Entra ID, Okta, Active Directory).

#### ¿Qué es la federación de identidades?

Permitir que los usuarios inicien sesión con una identidad existente (directorio corporativo, proveedor SAML 2.0 u OIDC) y reciban credenciales temporales de AWS, sin crear usuarios de IAM para ellos.

#### ¿Qué es AWS STS?

AWS Security Token Service emite credenciales temporales con privilegios limitados, por ejemplo cuando se asume un rol o cuando un usuario federado inicia sesión.

<!-- challenge -->

Una empresa con 20 cuentas de AWS crea usuarios IAM en cada una para 150 empleados. ¿Qué propones?

<!-- solution -->

Conectar el proveedor de identidad corporativo a IAM Identity Center, definir permission sets por rol de trabajo y asignar grupos a las cuentas. Luego eliminar los usuarios IAM por cuenta y sus claves.

<!-- takeaways -->

- Identity Center centraliza el acceso del personal entre cuentas.
- La federación reutiliza las identidades corporativas.
- Las credenciales de STS expiran solas.

### Servicios de seguridad y cumplimiento

<!-- unit: Gobierno multicuenta -->

<!-- goals -->

- Organizar cuentas con AWS Organizations y OUs.
- Poner barandas con SCPs y Control Tower.

<!-- concept -->

Las empresas usan muchas cuentas para separar equipos, entornos y riesgos. Administrarlas una por una no escala, así que Organizations las agrupa en unidades organizativas y aplica reglas desde arriba.

Las Service Control Policies fijan lo máximo que cualquiera puede hacer en una cuenta, incluso los administradores: por ejemplo, nadie puede salir de las regiones aprobadas ni desactivar los logs. Control Tower empaqueta esto en una landing zone lista con barandas.

<!-- example -->

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {"StringNotEquals": {"aws:RequestedRegion": ["eu-west-1", "eu-west-3"]}}
}
```

#### ¿Qué es AWS Organizations?

Un servicio para gestionar de forma centralizada varias cuentas de AWS: agruparlas en unidades organizativas (OU), aplicarles políticas y consolidar la facturación. Una cuenta de administración es la propietaria de la organización.

#### ¿Qué son las Service Control Policies (SCP)?

Políticas de AWS Organizations que fijan los permisos máximos de cuentas u OU. No conceden permisos: limitan lo que las políticas de IAM de esas cuentas pueden permitir, incluso para el usuario raíz de una cuenta miembro.

#### ¿Qué es AWS Control Tower?

Un servicio que configura y gobierna un entorno multicuenta seguro (una landing zone) según las buenas prácticas, con barreras de protección preventivas y de detección y un panel de control.

<!-- challenge -->

Una SCP deniega todas las acciones fuera de dos regiones de la UE. Un administrador de la cuenta tiene permisos IAM completos. ¿Puede lanzar una instancia en us-east-1?

<!-- solution -->

No. Las SCPs fijan los permisos máximos de la cuenta, así que ni un administrador puede actuar fuera de las regiones permitidas. (Los servicios globales pueden necesitar excepciones en la SCP).

<!-- takeaways -->

- Organizations agrupa las cuentas en OUs.
- Las SCPs limitan lo que cualquier identidad puede hacer en una cuenta.
- Control Tower monta una landing zone gobernada.

<!-- unit: Cifrado y secretos -->

<!-- goals -->

- Cifrar datos en reposo y en tránsito con KMS y ACM.
- Guardar y rotar secretos con Secrets Manager o Parameter Store.

<!-- concept -->

El cifrado protege los datos en dos estados. En reposo, las claves gestionadas en KMS cifran volúmenes, objetos y bases, y el acceso a la clave se vuelve un segundo chequeo de permisos. En tránsito, los certificados TLS de ACM protegen el tráfico hacia balanceadores y CloudFront.

Los secretos como las contraseñas de bases de datos necesitan su propio lugar. Guardarlos en un servicio gestionado con rotación significa que nunca están en el código y cambian sin redesplegar.

<!-- example -->

| Necesidad | Servicio |
|---|---|
| Cifrar S3, EBS, RDS con claves que controlas | KMS |
| HSM de un solo inquilino para cumplimiento estricto | CloudHSM |
| Certificado HTTPS para un balanceador | ACM |
| Contraseña de base de datos con rotación | Secrets Manager |
| Valores de configuración de la app | Parameter Store |

#### ¿Qué es AWS Key Management Service (KMS)?

Un servicio gestionado para crear y controlar claves de cifrado y usarlas para cifrar datos. Está integrado con la mayoría de los servicios de AWS y registra el uso de las claves en CloudTrail.

#### ¿Qué diferencia hay entre AWS KMS y AWS CloudHSM?

KMS es un servicio gestionado multiinquilino en el que AWS opera los módulos de seguridad de hardware. CloudHSM te da HSM dedicados de un solo inquilino que controlas tú, para requisitos de cumplimiento estrictos.

#### ¿Qué diferencia hay entre el cifrado en reposo y en tránsito?

En reposo protege los datos almacenados (objetos S3, volúmenes EBS, archivos de base de datos), normalmente con claves de KMS. En tránsito protege los datos que circulan por la red, normalmente con TLS.

#### ¿Qué es AWS Certificate Manager (ACM)?

Un servicio que emite, gestiona y renueva certificados SSL/TLS para usarlos con servicios de AWS como Elastic Load Balancing, CloudFront y API Gateway. Los certificados públicos son gratuitos.

#### ¿Qué es AWS Secrets Manager?

Un servicio para guardar, recuperar y rotar automáticamente secretos como contraseñas de bases de datos y claves de API, para que no estén escritos en el código de las aplicaciones.

#### ¿Qué diferencia hay entre Secrets Manager y Systems Manager Parameter Store?

Ambos guardan configuración y secretos. Secrets Manager añade la rotación automática integrada y el uso compartido entre cuentas, con un costo por secreto. El nivel estándar de Parameter Store es gratuito y sirve para valores de configuración y secretos sencillos sin rotación.

<!-- challenge -->

La contraseña de una base está en el código fuente de la aplicación y se subió a un repositorio público. ¿Qué haces ahora y para la próxima vez?

<!-- solution -->

Rotar la contraseña de inmediato y revisar los logs buscando abusos. Pasarla a Secrets Manager con rotación automática, que la app la lea al ejecutar mediante su rol IAM y agregar escaneo de secretos al repositorio.

<!-- takeaways -->

- KMS gestiona las claves de cifrado; CloudHSM da HSMs dedicados.
- ACM emite y renueva certificados TLS.
- Secrets Manager guarda y rota secretos.

<!-- unit: Proteger y detectar -->

<!-- goals -->

- Asociar los servicios de seguridad de AWS a las amenazas que cubren.
- Combinar servicios de protección, detección e investigación.

<!-- concept -->

Los servicios de seguridad hacen tres trabajos. Algunos protegen en el borde: Shield absorbe ataques DDoS y WAF filtra peticiones web maliciosas. Otros detectan: GuardDuty encuentra amenazas en los logs, Inspector vulnerabilidades y Macie datos sensibles donde no deberían estar. Otros ayudan a responder: Security Hub reúne los hallazgos en un lugar y Detective ayuda a rastrear qué pasó.

Saber qué trabajo hace un servicio suele bastar para elegir el correcto.

<!-- example -->

| Problema | Servicio |
|---|---|
| Intentos de inyección SQL en una app web | WAF |
| DDoS grande contra un sitio web | Shield (Advanced para protección extra) |
| Instancia que habla con una IP maliciosa conocida | GuardDuty |
| CVE sin parchear en una imagen de contenedor | Inspector |
| Números de tarjeta en un bucket S3 | Macie |
| Una vista de todos los hallazgos entre cuentas | Security Hub |

#### ¿Qué es AWS Shield?

Protección gestionada contra ataques DDoS. Shield Standard es automático y gratuito para todos los clientes frente a los ataques habituales de las capas de red y transporte. Shield Advanced es de pago y añade protección frente a ataques mayores, acceso 24/7 al Shield Response Team y protección de costos.

#### ¿Qué es AWS WAF?

Un cortafuegos de aplicaciones web que filtra las solicitudes HTTP(S) dirigidas a CloudFront, Application Load Balancer, API Gateway y AppSync mediante reglas (conjuntos de IP, límites de frecuencia, patrones de inyección SQL y cross-site scripting, grupos de reglas gestionadas).

#### ¿Qué es Amazon GuardDuty?

Un servicio inteligente de detección de amenazas que analiza continuamente los eventos de CloudTrail, los VPC Flow Logs y los registros DNS (y opcionalmente otras fuentes) con aprendizaje automático e inteligencia de amenazas para detectar actividad sospechosa, como credenciales comprometidas o minería de criptomonedas.

#### ¿Qué es Amazon Inspector?

Un servicio automatizado de gestión de vulnerabilidades que analiza instancias EC2, imágenes de contenedores en ECR y funciones Lambda en busca de vulnerabilidades de software y exposición de red no deseada.

#### ¿Qué es Amazon Macie?

Un servicio que usa aprendizaje automático y detección de patrones para descubrir y proteger datos sensibles, como datos personales, en Amazon S3.

#### ¿Qué es AWS Security Hub?

Una vista central de las alertas de seguridad y del estado de cumplimiento de varias cuentas. Agrega hallazgos de GuardDuty, Inspector, Macie y herramientas de socios, y ejecuta comprobaciones automáticas frente a estándares como los benchmarks CIS.

#### ¿Qué es Amazon Detective?

Un servicio que analiza y visualiza datos de seguridad para investigar la causa raíz de un hallazgo o de una actividad sospechosa.

<!-- challenge -->

GuardDuty informa que una instancia EC2 está minando criptomonedas. ¿Qué servicio te ayuda a entender cómo pasó y qué haces primero?

<!-- solution -->

Aislar la instancia (security group restrictivo, snapshot para forense) y revocar sus credenciales. Usar Detective para rastrear la actividad y el punto de entrada, e Inspector para revisar la vulnerabilidad explotada.

<!-- takeaways -->

- Shield y WAF protegen en el borde.
- GuardDuty, Inspector y Macie detectan amenazas, vulnerabilidades y datos sensibles.
- Security Hub centraliza; Detective investiga.

<!-- unit: Cumplimiento y reportes -->

<!-- goals -->

- Encontrar los reportes y acuerdos de cumplimiento de AWS.
- Conocer las reglas para pruebas de penetración y reportes de abuso.

<!-- concept -->

Los clientes heredan parte de su cumplimiento de AWS. Los auditores quieren pruebas de que la parte de AWS está certificada, y Artifact entrega esos reportes y acuerdos a demanda. Tu parte sigue necesitando tus propios controles y evidencias.

Probar tu propia seguridad está permitido en muchos servicios sin pedir permiso, dentro de reglas publicadas. Cuando recursos de AWS se usan contra ti, o los tuyos son abusados, el contacto es el equipo de abuso.

<!-- example -->

| Necesidad | Dónde |
|---|---|
| Reporte SOC 2 para un auditor | AWS Artifact |
| Firmar un business associate addendum (HIPAA) | AWS Artifact |
| Pen test de tu app web en EC2 | Permitido por la política, sin aprobación |
| Reportar spam que sale de una IP de AWS | AWS Trust & Safety (abuso) |

#### ¿Qué es AWS Artifact?

Un portal de autoservicio con los informes de cumplimiento de AWS (SOC, ISO, PCI DSS) y acuerdos (como el Business Associate Addendum para HIPAA).

#### ¿Qué es el programa de cumplimiento de AWS?

AWS mantiene certificaciones y acreditaciones (ISO 27001, SOC 1/2/3, PCI DSS, elegibilidad HIPAA, apoyo al RGPD) para su infraestructura. Los clientes heredan los controles de la infraestructura, pero deben hacer que sus propias cargas de trabajo cumplan.

#### ¿Hace falta permiso de AWS para hacer una prueba de penetración?

No para una lista de servicios permitidos (EC2, RDS, Lambda, CloudFront y otros). Algunas actividades siguen prohibidas, como los ataques DoS, que requieren un proceso de aprobación aparte para los eventos simulados.

#### ¿Qué es AWS Abuse y cuándo se contacta?

El equipo de AWS al que se notifica que recursos de AWS se están usando de forma abusiva, por ejemplo para spam, escaneo de puertos, ataques DoS o alojar malware.

<!-- challenge -->

Un auditor pide pruebas de que el centro de datos donde corre tu carga tiene certificación ISO 27001. ¿Qué entregas y basta para tu auditoría?

<!-- solution -->

Descargar el certificado ISO 27001 de AWS desde AWS Artifact. Cubre solo las responsabilidades de AWS; también debes mostrar tus propios controles (accesos, cifrado, logs) sobre tus cargas.

<!-- takeaways -->

- Artifact entrega los reportes y acuerdos de cumplimiento de AWS.
- El cumplimiento de AWS cubre solo la parte de AWS.
- Hacer pen testing en muchos servicios no requiere aprobación.

<!-- stage: Servicios principales -->

### Cómputo: EC2, contenedores y serverless

<!-- unit: Fundamentos de EC2 -->

<!-- goals -->

- Describir instancias EC2, AMIs y familias de instancias.
- Entender el almacenamiento de instancia y el ciclo de vida.

<!-- concept -->

EC2 alquila servidores virtuales. Eliges una plantilla (una AMI con el sistema operativo y el software), un tamaño de una familia afinada para CPU, memoria, almacenamiento o aceleradores, y un script para el primer arranque. Las instancias se comportan entonces como servidores que controlas.

El ciclo de vida importa para costos y datos. Las instancias detenidas conservan sus volúmenes EBS y dejan de pagar cómputo; las terminadas desaparecen. Los discos de instance store son rápidos pero pierden los datos cuando la instancia se detiene.

<!-- example -->

```bash
aws ec2 run-instances --image-id ami-0abcd1234 --instance-type m7i.large \
  --iam-instance-profile Name=web-app \
  --user-data file://install_web.sh
```

#### ¿Qué es Amazon EC2 y cuáles son sus características principales?

Elastic Compute Cloud proporciona servidores virtuales redimensionables (instancias). Características principales: muchos tipos de instancia, elección del sistema operativo mediante AMI, varios modelos de precios, almacenamiento EBS y de instancia, grupos de seguridad, Auto Scaling, direcciones IP elásticas y ubicación en cualquier AZ.

#### ¿Qué es una AMI?

Una Amazon Machine Image es una plantilla con el sistema operativo, el software y la configuración que se usa para lanzar instancias. Puedes usar AMI de AWS, del Marketplace, de la comunidad o propias.

#### ¿Cuáles son las familias de instancias EC2?

- **Uso general** (M, T): CPU, memoria y red equilibradas.
- **Optimizadas para cómputo** (C): procesadores de alto rendimiento, para procesamiento por lotes, videojuegos, modelización científica.
- **Optimizadas para memoria** (R, X): grandes conjuntos de datos en memoria.
- **Computación acelerada** (P, G, Inf, Trn): GPU o chips propios para aprendizaje automático y gráficos.
- **Optimizadas para almacenamiento** (I, D): lectura y escritura secuencial intensiva en almacenamiento local, para almacenes de datos y OLTP.

#### ¿Qué son las instancias T y el rendimiento ampliable?

Las instancias T ofrecen un nivel base de CPU y acumulan créditos de CPU cuando están ociosas, que gastan para superar ese nivel. Encajan con cargas de CPU media baja y picos ocasionales.

#### ¿Qué son los datos de usuario (user data) de EC2?

Un script que se pasa al lanzar la instancia y se ejecuta en el primer arranque, para instalar software o configurar la instancia.

#### ¿Qué es el almacén de instancia de EC2 (instance store)?

Almacenamiento de bloques temporal conectado físicamente al servidor. Es muy rápido, pero sus datos se pierden cuando la instancia se detiene o se termina, así que sirve para búferes, cachés y datos temporales.

#### ¿Qué diferencia hay entre detener y terminar una instancia?

Detenerla la apaga: se conservan los volúmenes EBS raíz y solo pagas el almacenamiento, y puedes volver a arrancarla. Terminarla la elimina y, por defecto, también su volumen EBS raíz.

<!-- challenge -->

Una app de analítica en memoria que consume mucha RAM corre en una instancia de propósito general y no deja de hacer swap. ¿Qué familia sugieres?

<!-- solution -->

Una familia optimizada para memoria (R o X), que ofrece mucha más RAM por vCPU. Mide antes el uso de memoria para elegir el tamaño.

<!-- takeaways -->

- Una AMI es la plantilla; la familia define el balance de recursos.
- Detener conserva EBS; terminar borra la instancia.
- Los datos del instance store no sobreviven a una detención.

<!-- unit: Pagar por EC2 -->

<!-- goals -->

- Comparar On-Demand, Savings Plans, Reserved, Spot y Dedicated.
- Asociar una opción de precio a un patrón de carga.

<!-- concept -->

La misma instancia puede costar cantidades muy distintas según cómo te comprometas. On-Demand es el precio de la flexibilidad. Comprometerse con uso estable por uno o tres años con Savings Plans o Reserved Instances lo baja mucho. Spot vende capacidad sobrante con el mayor descuento, pero AWS puede retirarla con dos minutos de aviso.

Así que la elección de precio sigue a la carga: base estable con compromisos, picos con On-Demand y batch interrumpible con Spot.

<!-- example -->

| Carga | Precio |
|---|---|
| Servidores web 24/7 durante años | Savings Plan |
| Picos de tráfico en temporada | On-Demand |
| Renderizado nocturno de imágenes, reiniciable | Spot |
| Licencia ligada a núcleos físicos | Dedicated Host |

#### ¿Cuáles son las opciones de precios de EC2?

- **Bajo demanda:** pago por segundo u hora, sin compromiso.
- **Savings Plans:** compromiso de gasto por hora durante 1 o 3 años, hasta un 72 % de descuento aproximadamente.
- **Instancias reservadas:** compromiso con una configuración de instancia durante 1 o 3 años.
- **Instancias de spot:** capacidad sobrante con hasta un 90 % de descuento, que puede interrumpirse con dos minutos de aviso.
- **Hosts dedicados:** un servidor físico para ti, por licencias y cumplimiento.
- **Instancias dedicadas:** instancias en hardware no compartido con otras cuentas.
- **Reservas de capacidad:** reservar capacidad en una AZ, a precio bajo demanda.

#### ¿Cuándo conviene usar instancias de spot?

Para cargas flexibles, tolerantes a fallos e interrumpibles: trabajos por lotes, procesamiento de datos, compilaciones de CI, servidores web sin estado. Nunca para una base de datos que no puede pararse.

#### ¿Qué diferencia hay entre los Compute Savings Plans y los EC2 Instance Savings Plans?

Los Compute Savings Plans se aplican a cualquier familia, tamaño, región y sistema operativo, y también a Fargate y Lambda. Los EC2 Instance Savings Plans están ligados a una familia de instancias en una región, pero dan un descuento mayor.

#### ¿Cuándo hace falta un host dedicado?

Cuando las licencias de software van ligadas a núcleos o zócalos físicos (traer tu propia licencia), o cuando el cumplimiento exige visibilidad y control del servidor físico.

<!-- challenge -->

Una empresa corre 20 instancias todo el año y suma 30 más durante dos meses cada invierno. ¿Cómo lo pagas?

<!-- solution -->

Cubrir las 20 instancias estables con un Savings Plan (los Compute Savings Plans mantienen flexibilidad) y correr las 30 estacionales en On-Demand, o en Spot si la carga tolera interrupciones.

<!-- takeaways -->

- Compromete el uso estable; deja los picos en On-Demand.
- Spot es lo más barato pero interrumpible.
- Los Dedicated Hosts atienden licencias por núcleo y aislamiento.

<!-- unit: Red y escalado de EC2 -->

<!-- goals -->

- Controlar el tráfico de las instancias con security groups y acceder a ellas con seguridad.
- Escalar y balancear carga con Auto Scaling y ELB.

<!-- concept -->

Una instancia sola no es ni alcanzable con seguridad ni resiliente. Los security groups deciden qué tráfico le llega, y son stateful, así las respuestas se permiten automáticamente. Session Manager e Instance Connect dan acceso a los administradores sin claves SSH de larga vida.

La resiliencia y la escala vienen de grupos de instancias: un balanceador reparte el tráfico entre zonas y deja de enviar a destinos no sanos, mientras Auto Scaling reemplaza instancias fallidas y ajusta la capacidad a la demanda.

<!-- example -->

```text
users ─► Application Load Balancer (AZ a, b)
           └─► Auto Scaling group: min 2, desired 4, max 10 (target CPU 50%)
                 security group: allow 443 from the load balancer only
```

#### ¿Qué es un grupo de seguridad?

Un cortafuegos virtual con estado para instancias (asociado a interfaces de red). Solo tiene reglas de permiso. El tráfico de respuesta se permite automáticamente, y por defecto se deniega todo el tráfico entrante y se permite todo el saliente.

#### ¿Qué es una dirección IP elástica?

Una dirección IPv4 pública estática que asignas a tu cuenta y puedes asociar a una instancia. Las direcciones IPv4 públicas se facturan por hora, estén asociadas o no.

#### ¿Qué es EC2 Auto Scaling?

Un servicio que añade o retira instancias EC2 de un grupo de Auto Scaling según políticas (seguimiento de objetivo, por pasos, programadas, predictivas) y sustituye las instancias en mal estado. Defines la capacidad mínima, deseada y máxima.

#### ¿Qué es Elastic Load Balancing y qué tipos tiene?

Un servicio que reparte el tráfico entre destinos de varias AZ y comprueba su estado.
- **Application Load Balancer:** HTTP/HTTPS, capa 7, enrutamiento por ruta y por host.
- **Network Load Balancer:** TCP/UDP/TLS, capa 4, rendimiento muy alto e IP estáticas.
- **Gateway Load Balancer:** capa 3, para dispositivos de red de terceros como cortafuegos.

#### ¿Qué aportan EC2 Instance Connect o Session Manager?

Formas de acceder a las instancias sin gestionar claves SSH. Session Manager (parte de Systems Manager) funciona incluso sin abrir puertos de entrada, y registra las sesiones.

<!-- challenge -->

Una app web corre en una sola instancia con una Elastic IP. Se cayó cuando falló la instancia. ¿Cómo la rediseñas?

<!-- solution -->

Poner dos o más instancias en un grupo de Auto Scaling en dos zonas detrás de un Application Load Balancer, apuntar el DNS al balanceador y prescindir de la Elastic IP. Las instancias fallidas se reemplazan solas.

<!-- takeaways -->

- Los security groups son firewalls stateful por instancia.
- Los balanceadores reparten tráfico y revisan la salud.
- Auto Scaling reemplaza y ajusta instancias.

<!-- unit: Contenedores y funciones -->

<!-- goals -->

- Elegir entre Lambda, ECS, EKS y Fargate.
- Saber dónde se guardan las imágenes de contenedores.

<!-- concept -->

Contenedores y funciones alejan aún más el trabajo de los servidores. Lambda corre una función por evento y cobra solo mientras corre, ideal para trabajo corto y con picos. Los contenedores empaquetan una aplicación con sus dependencias; ECS y EKS los planifican y Fargate los corre sin administrar instancias.

La elección depende de cuánto dura el trabajo, cuánto control necesitas y si el equipo ya conoce Kubernetes.

<!-- example -->

| Carga | Buena opción |
|---|---|
| Redimensionar una imagen al subirla | Lambda |
| API web en contenedores, equipo pequeño | ECS sobre Fargate |
| El estándar de la empresa es Kubernetes | EKS |
| Guardar y escanear imágenes | ECR |

#### ¿Qué es AWS Lambda?

Un servicio de cómputo serverless que ejecuta tu función en respuesta a eventos (una llamada a una API, un archivo en S3, un mensaje, una programación). Pagas por solicitud y por duración en milisegundos. Una invocación puede durar como máximo 15 minutos.

#### ¿Cuándo elegirías Lambda en lugar de EC2?

Para cargas basadas en eventos, de corta duración, variables o imprevisibles en las que no quieres gestionar servidores. EC2 encaja con procesos de larga duración, requisitos especiales de sistema operativo o carga alta y constante.

#### ¿Qué diferencia hay entre Amazon ECS y Amazon EKS?

Los dos orquestan contenedores. ECS es el orquestador propio de AWS, más sencillo. EKS es Kubernetes gestionado, para equipos que usan las herramientas de Kubernetes o necesitan portabilidad.

#### ¿Qué es AWS Fargate?

Un motor de cómputo serverless para contenedores que funciona con ECS y EKS. Defines la CPU y la memoria de cada tarea o pod, y AWS lo ejecuta sin servidores que gestionar.

#### ¿Qué es Amazon ECR?

Elastic Container Registry, un registro gestionado para guardar, analizar y compartir imágenes de contenedores Docker y OCI.

<!-- challenge -->

Una tarea de procesamiento de datos corre 40 minutos cada noche. Un colega propone Lambda. ¿Encaja?

<!-- solution -->

No: las funciones Lambda están limitadas a 15 minutos. Córrela como tarea de contenedor en ECS con Fargate (o AWS Batch), que no tiene ese límite y tampoco necesita servidores.

<!-- takeaways -->

- Lambda para trabajo corto dirigido por eventos (máximo 15 minutos).
- ECS es más simple; EKS es Kubernetes.
- Fargate corre contenedores sin administrar instancias.

<!-- unit: Plataformas gestionadas -->

<!-- goals -->

- Reconocer los casos de uso de Elastic Beanstalk, Lightsail, Batch y App Runner.
- Elegir la plataforma más simple que encaje.

<!-- concept -->

Algunos servicios existen sobre todo para ocultar decisiones de infraestructura. Elastic Beanstalk despliega código sobre EC2 con balanceo y escalado ya configurados. App Runner hace lo mismo para contenedores y código fuente con aún menos que configurar. Lightsail ofrece servidores simples a precio fijo para proyectos pequeños. Batch planifica grandes cantidades de jobs sobre capacidad gestionada.

Cambian control por velocidad, a menudo el cambio correcto para equipos pequeños.

<!-- example -->

| Necesidad | Servicio |
|---|---|
| Desplegar una app Django sin aprender los detalles de EC2 | Elastic Beanstalk |
| Correr una API web en contenedor desde un repo | App Runner |
| Blog pequeño con precio mensual predecible | Lightsail |
| 10.000 jobs de simulación | AWS Batch |

#### ¿Qué es AWS Elastic Beanstalk?

Una plataforma como servicio: subes el código de la aplicación (Java, .NET, Node.js, Python, PHP, Go, Ruby, Docker) y Beanstalk aprovisiona y gestiona EC2, el balanceo de carga, Auto Scaling y la monitorización. Los recursos subyacentes siguen visibles y configurables.

#### ¿Qué es Amazon Lightsail?

Un servicio simplificado de servidores privados virtuales, bases de datos y contenedores a un precio mensual previsible, pensado para webs sencillas y usuarios que empiezan en AWS.

#### ¿Qué es AWS Batch?

Un servicio que ejecuta trabajos de cómputo por lotes a cualquier escala, aprovisionando capacidad EC2 o Fargate (incluida spot) según los trabajos en cola.

#### ¿Qué es AWS App Runner?

Un servicio totalmente gestionado que construye y ejecuta aplicaciones web y API a partir de código fuente o de una imagen de contenedor, con escalado automático y HTTPS.

<!-- challenge -->

Una startup de dos personas quiere desplegar esta semana una API en contenedor con HTTPS y autoescalado, sin experiencia en operación. ¿Qué sugieres?

<!-- solution -->

AWS App Runner: apúntalo a la imagen o al repositorio y se encarga de build, despliegue, HTTPS, balanceo y escalado. Revisar ECS más adelante si necesitan más control.

<!-- takeaways -->

- Los servicios de plataforma cambian control por velocidad.
- Beanstalk y App Runner despliegan apps sin trabajo de infraestructura.
- Batch corre grandes colas de jobs sobre capacidad gestionada.

### Almacenamiento

<!-- unit: Fundamentos de S3 -->

<!-- goals -->

- Describir buckets, objetos, durabilidad y clases de almacenamiento.
- Bajar costos de almacenamiento con clases y reglas de ciclo de vida.

<!-- concept -->

S3 guarda objetos (archivos con metadatos) en buckets, con una durabilidad altísima porque cada objeto se copia en varias instalaciones. Lo que varía es qué tan rápido y qué tan seguido necesitas los datos, y las clases de almacenamiento lo ponen precio: el acceso frecuente cuesta más por gigabyte guardado, los archivos cuestan poco de guardar pero más y más lento de recuperar.

Las reglas de ciclo de vida mueven objetos entre clases a medida que envejecen, así los datos se abaratan solos.

<!-- example -->

```json
{"Rules": [{"ID": "logs", "Status": "Enabled", "Filter": {"Prefix": "logs/"},
  "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"},
                  {"Days": 180, "StorageClass": "GLACIER"}],
  "Expiration": {"Days": 730}}]}
```

#### ¿Qué es Amazon S3 y qué clases de almacenamiento ofrece?

Simple Storage Service es un almacenamiento de objetos con una durabilidad de 11 nueves (99,999999999 %), donde los datos se guardan como objetos en buckets. Clases de almacenamiento:
- **S3 Standard:** datos de acceso frecuente.
- **S3 Intelligent-Tiering:** mueve los objetos entre niveles automáticamente cuando los patrones de acceso son desconocidos o cambian.
- **S3 Standard-IA:** acceso poco frecuente, recuperación en milisegundos, con cargo por recuperación.
- **S3 One Zone-IA:** acceso poco frecuente guardado en una sola AZ, más barato y menos resiliente.
- **S3 Express One Zone:** latencia de milisegundos de un dígito para los datos más sensibles al rendimiento.
- **S3 Glacier Instant Retrieval:** archivo consultado más o menos una vez por trimestre, recuperación en milisegundos.
- **S3 Glacier Flexible Retrieval:** archivo, recuperación en minutos u horas.
- **S3 Glacier Deep Archive:** la más barata, recuperación en 12 a 48 horas.

#### ¿Qué son un bucket y un objeto de S3?

Un bucket es un contenedor de objetos con un nombre único a nivel mundial, creado en una región. Un objeto es un archivo con sus metadatos, identificado por una clave, de hasta 5 TB.

#### ¿Qué durabilidad y disponibilidad tiene S3 Standard?

Está diseñado para una durabilidad del 99,999999999 % y una disponibilidad del 99,99 %, con los datos guardados en al menos tres AZ.

#### ¿Cuándo usarías S3 One Zone-IA?

Para datos de acceso poco frecuente que se pueden volver a generar, como copias de seguridad secundarias o datos derivados, cuando perder una AZ es aceptable a cambio de un precio menor.

#### ¿Qué son las políticas de ciclo de vida de S3?

Reglas que pasan automáticamente los objetos a clases de almacenamiento más baratas a partir de cierta antigüedad, o los eliminan (caducidad).

<!-- challenge -->

Los logs de una aplicación se leen seguido durante una semana, rara vez durante un año, y deben guardarse 7 años para auditoría. Diseña un ciclo de vida.

<!-- solution -->

Mantenerlos en S3 Standard 30 días, pasarlos a Standard-IA, luego a Glacier Flexible Retrieval o Deep Archive tras un año, y expirarlos a los 7 años.

<!-- takeaways -->

- S3 guarda objetos en buckets con 11 nueves de durabilidad.
- Las clases cambian velocidad de acceso por precio.
- Las reglas de ciclo de vida mueven y expiran datos automáticamente.

<!-- unit: Proteger y servir datos en S3 -->

<!-- goals -->

- Proteger objetos con versionado, controles de acceso, cifrado y replicación.
- Servir sitios web y acelerar subidas desde S3.

<!-- concept -->

Los valores por defecto de S3 son seguros (los buckets nuevos son privados y cifrados), y la mayoría de incidentes vienen de cambiarlos. El versionado protege contra sobrescrituras y borrados, Block Public Access evita exposiciones accidentales, las políticas limitan quién lee qué y la replicación guarda una copia en otra región.

S3 también puede servir contenido directamente, para sitios estáticos, normalmente detrás de CloudFront, y acelerar subidas de larga distancia mediante edge locations.

<!-- example -->

```bash
aws s3api put-bucket-versioning --bucket finance-docs --versioning-configuration Status=Enabled
aws s3api put-public-access-block --bucket finance-docs \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

#### ¿Qué es el control de versiones de S3?

Una opción del bucket que conserva todas las versiones de un objeto, para poder recuperar objetos sobrescritos o eliminados.

#### ¿Cómo se controla el acceso a S3?

Con políticas de IAM, políticas de bucket, puntos de acceso, ACL (desactivadas por defecto hoy) y Block Public Access, que impide el acceso público a nivel de bucket o de cuenta. Las URL prefirmadas dan acceso temporal a un objeto.

#### ¿Cómo se cifran los datos de S3?

Todos los objetos nuevos se cifran en reposo por defecto con claves gestionadas por S3 (SSE-S3). Puedes elegir claves de KMS (SSE-KMS), claves proporcionadas por el cliente (SSE-C) o cifrar en el cliente antes de subir.

#### ¿Qué es la replicación de S3?

La copia automática y asíncrona de objetos a otro bucket de otra región (Cross-Region Replication) o de la misma región (Same-Region Replication). Requiere el control de versiones.

#### ¿Qué es el alojamiento de sitios web estáticos en S3?

Servir un sitio web hecho de archivos estáticos (HTML, CSS, JS, imágenes) directamente desde un bucket, normalmente detrás de CloudFront para tener HTTPS y caché.

#### ¿Qué es S3 Transfer Acceleration?

Subidas más rápidas a larga distancia, enrutándolas por las ubicaciones de borde de CloudFront y la red troncal de AWS.

<!-- challenge -->

Un usuario borró una carpeta importante de un bucket. El versionado estaba activo. ¿Puedes recuperarla y cómo?

<!-- solution -->

Sí. Con versionado, el borrado solo agregó delete markers. Quita los delete markers (o copia de vuelta las versiones anteriores) y considera MFA delete u Object Lock para buckets críticos.

<!-- takeaways -->

- El versionado protege contra sobrescrituras y borrados.
- Block Public Access evita exposiciones accidentales.
- La replicación copia objetos a otra región o cuenta.

<!-- unit: Almacenamiento en bloque y de archivos -->

<!-- goals -->

- Comparar S3, EBS, EFS y FSx.
- Respaldar volúmenes EBS con snapshots.

<!-- concept -->

No todas las aplicaciones pueden usar almacenamiento de objetos. Las bases de datos y los sistemas operativos necesitan almacenamiento en bloque, un disco conectado a una instancia: eso es EBS, respaldado con snapshots incrementales. Las aplicaciones que comparten archivos entre muchos servidores necesitan un sistema de archivos: EFS para Linux y FSx para Windows y sistemas especializados.

La elección sigue al patrón de acceso: objetos por API, disco de una instancia o archivos compartidos.

<!-- example -->

| Necesidad | Servicio |
|---|---|
| Disco de arranque y de base de datos para una instancia | EBS |
| Carpeta compartida para 20 servidores web Linux | EFS |
| Recursos compartidos de Windows con Active Directory | FSx for Windows File Server |
| Imágenes y backups accedidos por HTTP | S3 |

#### ¿Qué es Amazon EBS?

Elastic Block Store ofrece volúmenes de bloques en red para instancias EC2, que persisten con independencia de la vida de la instancia. Un volumen vive en una AZ y se replica dentro de ella. Tipos: gp3 (SSD de uso general), io2 (SSD de IOPS provisionadas), st1 (HDD optimizado para rendimiento) y sc1 (HDD de acceso poco frecuente).

#### ¿Qué son las instantáneas de EBS?

Copias de seguridad incrementales de volúmenes EBS en un momento dado, guardadas en S3 (gestionado por AWS). Se pueden copiar a otras regiones y usar para crear volúmenes nuevos.

#### ¿Qué es Amazon EFS?

Elastic File System es un sistema de archivos NFS gestionado para Linux que crece y se reduce automáticamente y que pueden montar a la vez muchas instancias de varias AZ.

#### ¿Qué diferencia hay entre S3, EBS y EFS?

S3 es almacenamiento de objetos al que se accede por API, prácticamente ilimitado, para cualquier número de clientes. EBS es almacenamiento de bloques conectado (normalmente) a una instancia en una AZ, como un disco. EFS es un sistema de archivos compartido para muchas instancias Linux de varias AZ.

#### ¿Qué es Amazon FSx?

Sistemas de archivos de terceros totalmente gestionados: FSx for Windows File Server (SMB), FSx for Lustre (computación de alto rendimiento), FSx for NetApp ONTAP y FSx for OpenZFS.

<!-- challenge -->

Diez servidores Linux detrás de un balanceador deben leer y escribir los mismos archivos subidos. ¿Qué almacenamiento eliges?

<!-- solution -->

Amazon EFS, montado por todos los servidores por NFS, o S3 si la aplicación puede usar una API. Los volúmenes EBS se conectan a una sola instancia, así que no sirven para acceso compartido.

<!-- takeaways -->

- EBS es almacenamiento en bloque para una instancia.
- EFS y FSx son sistemas de archivos compartidos.
- S3 es almacenamiento de objetos accedido por API.

<!-- unit: Híbrido, transferencia y backup -->

<!-- goals -->

- Mover datos a AWS en línea y fuera de línea.
- Centralizar los backups entre servicios.

<!-- concept -->

Llevar datos a AWS depende del volumen y del ancho de banda. Las transferencias en línea con DataSync sirven para cantidades continuas o moderadas; cuando por red tardaría semanas, los dispositivos Snow envían los datos físicamente. Algunas aplicaciones on-premises siguen corriendo y usan almacenamiento en la nube mediante Storage Gateway.

Cuando las cargas ya corren en AWS, los backups deben centralizarse, con políticas y auditoría entre servicios, que es el trabajo de AWS Backup.

<!-- example -->

| Situación | Servicio |
|---|---|
| Archivo de 500 TB, enlace de oficina lento | Snowball |
| Sincronización diaria de un servidor NFS a S3 | DataSync |
| App de backup on-premises que escribe en cinta en la nube | Storage Gateway (Tape Gateway) |
| Política de backup para RDS, EBS y DynamoDB | AWS Backup |

#### ¿Qué es AWS Storage Gateway?

Un servicio de almacenamiento híbrido que da a las aplicaciones locales acceso al almacenamiento en la nube. Tipos: S3 File Gateway, FSx File Gateway, Volume Gateway y Tape Gateway (biblioteca de cintas virtual para copias de seguridad).

#### ¿Qué es la familia AWS Snow?

Dispositivos físicos para mover grandes volúmenes de datos hacia o desde AWS sin conexión, o para procesar datos en el borde donde hay poca o ninguna conectividad (dispositivos AWS Snowball Edge).

#### ¿Qué es AWS DataSync?

Un servicio de transferencia de datos en línea que mueve datos entre almacenamiento local (NFS, SMB, HDFS, almacenes de objetos) y los servicios de almacenamiento de AWS, de forma rápida y con verificación.

#### ¿Qué es AWS Backup?

Un servicio centralizado para automatizar y auditar las copias de seguridad de varios servicios: EBS, EC2, RDS, DynamoDB, EFS, FSx, S3 y más, con planes de copia y copias entre regiones o entre cuentas.

<!-- challenge -->

Una empresa debe mover 200 TB a AWS por un enlace de 100 Mbps. Estima el tiempo de transferencia en línea y sugiere una opción.

<!-- solution -->

A 100 Mbps, 200 TB tardan unos 185 días a velocidad máxima. Usar dispositivos Snowball Edge para enviar los datos y luego DataSync para los cambios hechos durante el envío.

<!-- takeaways -->

- DataSync mueve datos en línea; los dispositivos Snow los envían.
- Storage Gateway conecta apps on-premises con almacenamiento en la nube.
- AWS Backup centraliza las políticas de backup.

### Bases de datos y analítica

<!-- unit: Bases de datos relacionales -->

<!-- goals -->

- Comparar RDS, Aurora y DynamoDB.
- Distinguir Multi-AZ de réplicas de lectura y usar DMS para migraciones.

<!-- concept -->

Las bases relacionales en AWS vienen gestionadas: RDS corre motores conocidos y se encarga de backups, parches y failover; Aurora es el motor nativo de AWS con almacenamiento replicado entre zonas. DynamoDB es otro modelo, un almacén clave-valor que escala sin servidores.

Dos funciones de RDS se confunden a menudo. Multi-AZ es para disponibilidad: un standby toma el control si falla el primario. Las réplicas de lectura son para escala: sirven lecturas. DMS trae bases existentes con poco tiempo de inactividad.

<!-- example -->

| Necesidad | Opción |
|---|---|
| Sobrevivir a la caída de una zona | RDS Multi-AZ |
| Descargar las lecturas de reportes | Réplica de lectura |
| Carrito de compras con millones de usuarios, acceso por clave | DynamoDB |
| Mover Oracle on-premises a PostgreSQL | DMS (+ Schema Conversion) |

#### ¿En qué se diferencia Amazon RDS de Amazon DynamoDB?

RDS es un servicio de bases de datos relacionales gestionado (SQL, esquemas, joins, transacciones) que ejecuta MySQL, PostgreSQL, MariaDB, Oracle, SQL Server o Db2 en instancias cuyo tamaño eliges. DynamoDB es una base de datos NoSQL serverless de clave-valor y documentos, con rendimiento de milisegundos de un dígito a cualquier escala, sin esquema fijo más allá de las claves y con escalado automático.

#### ¿Qué gestiona Amazon RDS por ti?

El aprovisionamiento, los parches del sistema operativo y de la base de datos, las copias de seguridad automáticas y la recuperación a un momento dado, la conmutación Multi-AZ, las réplicas de lectura, la monitorización y el crecimiento del almacenamiento. Tú gestionas el esquema, las consultas, los usuarios y el acceso de red.

#### ¿Qué diferencia hay entre RDS Multi-AZ y las réplicas de lectura?

Multi-AZ mantiene una o varias réplicas en espera síncronas en otra AZ para la alta disponibilidad y la conmutación automática. En su configuración clásica no sirve lecturas. Las réplicas de lectura son copias asíncronas para repartir el tráfico de lectura, posiblemente en otras regiones, y se pueden promocionar.

#### ¿Qué es Amazon Aurora?

Una base de datos relacional nativa de la nube compatible con MySQL y PostgreSQL. Guarda seis copias de los datos en tres AZ, escala el almacenamiento automáticamente y ofrece Aurora Serverless para cargas variables.

#### ¿Qué es AWS Database Migration Service (DMS)?

Un servicio que migra bases de datos a AWS con un tiempo de inactividad mínimo, entre motores iguales (homogénea) o distintos (heterogénea, con la Schema Conversion Tool), y que puede replicar los cambios en curso.

<!-- challenge -->

Los reportes ralentizan una base RDS en horario laboral. El equipo propone activar Multi-AZ. ¿Es el arreglo correcto?

<!-- solution -->

No. Los standbys Multi-AZ no sirven lecturas; son para failover. Agrega una réplica de lectura y apunta los reportes a ella (o lleva los reportes a un warehouse).

<!-- takeaways -->

- RDS gestiona motores; Aurora es nativo de la nube; DynamoDB es clave-valor.
- Multi-AZ es disponibilidad; las réplicas de lectura, escala de lecturas.
- DMS migra bases con mínima inactividad.

<!-- unit: Bases de datos de propósito específico -->

<!-- goals -->

- Asociar necesidades de caché, documentos, grafos, columnas anchas y series de tiempo a servicios.
- Saber cuándo ayuda un almacén en memoria.

<!-- concept -->

El enfoque de AWS es "la base correcta para cada trabajo". En vez de forzar toda forma de datos en tablas, ofrece motores construidos para patrones de acceso específicos: cachés en memoria para lecturas de microsegundos, almacenes de documentos para JSON, grafos para relaciones, almacenes de columnas anchas para escrituras masivas y series de tiempo para métricas.

La pregunta es cómo lee y escribe datos la aplicación; el motor sigue de ahí.

<!-- example -->

| Patrón de acceso | Servicio |
|---|---|
| Cachear páginas de producto | ElastiCache |
| Almacén primario duradero compatible con Redis | MemoryDB |
| Documentos estilo MongoDB | DocumentDB |
| Anillos de fraude, grafos sociales | Neptune |
| Cargas de Cassandra | Keyspaces |
| Lecturas de sensores IoT | Timestream |

#### ¿Qué es Amazon ElastiCache?

Caché en memoria gestionada con Valkey, Redis OSS o Memcached, que se usa para reducir la carga de la base de datos y servir lecturas frecuentes con latencia de microsegundos.

#### ¿Qué es Amazon MemoryDB?

Una base de datos en memoria duradera, compatible con Valkey y Redis OSS, que puede usarse como base de datos principal gracias a su registro de transacciones Multi-AZ.

#### ¿Qué es Amazon DocumentDB?

Una base de datos documental gestionada compatible con cargas de trabajo de MongoDB.

#### ¿Qué es Amazon Neptune?

Una base de datos de grafos gestionada para datos muy conectados, como redes sociales, detección de fraude y grafos de conocimiento.

#### ¿Qué es Amazon Keyspaces?

Una base de datos gestionada y serverless compatible con Apache Cassandra.

#### ¿Qué es Amazon Timestream?

Una base de datos de series temporales gestionada para IoT y métricas operativas.

<!-- challenge -->

Las páginas de producto de un e-commerce consultan la base en cada vista y la sobrecargan. ¿Qué agregas?

<!-- solution -->

Una caché de ElastiCache delante de la base: cachear los datos de producto con una expiración sensata, para que la mayoría de vistas nunca lleguen a la base.

<!-- takeaways -->

- Elige la base según el patrón de acceso.
- Las cachés bajan la carga y la latencia de la base.
- Grafos, documentos y series de tiempo encajan con formas concretas.

<!-- unit: Servicios de analítica -->

<!-- goals -->

- Distinguir OLTP de OLAP y los servicios de cada uno.
- Ubicar Redshift, Athena, Glue, EMR y Lake Formation en una plataforma de datos.

<!-- concept -->

Los sistemas transaccionales responden muchas preguntas pequeñas rápido; los analíticos responden preguntas grandes sobre mucha historia. Mezclarlos ralentiza ambos, así que la analítica suele ir a una plataforma aparte.

En AWS esa plataforma tiene piezas intercambiables: S3 como lake, Glue para catalogar y transformar, Lake Formation para gobernar, Athena para SQL serverless sobre archivos, Redshift como warehouse para BI pesado y EMR para frameworks de big data.

<!-- example -->

```text
RDS (OLTP) ─► DMS / Glue ─► S3 data lake ─► Athena (ad hoc SQL)
                               │  Glue Data Catalog + Lake Formation
                               └─► Redshift (dashboards)   EMR (Spark)
```

#### ¿Qué es Amazon Redshift?

Un almacén de datos en la nube gestionado, a escala de petabytes, para consultas analíticas SQL (OLAP), con almacenamiento en columnas, una opción serverless y la posibilidad de consultar datos en S3.

#### ¿Qué diferencia hay entre OLTP y OLAP y qué servicios de AWS encajan con cada uno?

OLTP gestiona muchas lecturas y escrituras transaccionales pequeñas (pedidos, pagos): RDS, Aurora, DynamoDB. OLAP ejecuta grandes consultas analíticas sobre datos históricos: Redshift, Athena.

#### ¿Qué es Amazon Athena?

Un servicio de consultas interactivas serverless para analizar datos en S3 con SQL estándar. Pagas por cantidad de datos escaneados, así que los formatos en columnas y el particionado reducen el costo.

#### ¿Qué es AWS Glue?

Un servicio serverless de integración de datos: rastreadores para descubrir esquemas, el Glue Data Catalog como almacén central de metadatos y trabajos ETL basados en Spark.

#### ¿Qué es Amazon EMR?

Una plataforma de big data gestionada para ejecutar Apache Spark, Hive, Presto/Trino, HBase y otros frameworks sobre EC2, EKS o en modo serverless.

#### ¿Qué es AWS Lake Formation?

Un servicio para construir, proteger y gestionar un data lake en S3, con permisos detallados y centralizados sobre las tablas del Glue Data Catalog.

<!-- challenge -->

Los analistas quieren correr SQL ocasional sobre tres años de logs en S3 sin cargarlos en ningún lado. ¿Qué servicio encaja?

<!-- solution -->

Amazon Athena con tablas en el Glue Data Catalog: las consultas corren directamente sobre S3 y pagas por datos escaneados. Convertir los logs a Parquet mantiene bajos los costos.

<!-- takeaways -->

- OLTP para transacciones; OLAP para análisis.
- Athena consulta S3; Redshift sirve BI pesado.
- Glue y Lake Formation catalogan y gobiernan el lake.

<!-- unit: Streaming, búsqueda y BI -->

<!-- goals -->

- Reconocer los casos de uso de Kinesis, OpenSearch y QuickSight.
- Construir un flujo simple de tiempo real a dashboard.

<!-- concept -->

Algunos datos valen solo mientras están frescos: clics, lecturas de sensores, logs. Kinesis captura y entrega esos streams, para procesamiento propio o directo al almacenamiento. OpenSearch indexa texto y logs para buscarlos y explorarlos de forma interactiva.

Al final de la mayoría de pipelines hay una herramienta de BI; QuickSight ofrece dashboards serverless que los usuarios de negocio pueden explorar y compartir.

<!-- example -->

```text
app clicks ─► Kinesis Data Streams ─► consumers (real-time alerts)
           └► Firehose ─► S3 ─► Athena ─► QuickSight dashboard
app logs   ─► OpenSearch Service (search, log analytics)
```

#### ¿Qué es Amazon Kinesis?

Servicios para datos en streaming en tiempo real. Kinesis Data Streams captura y guarda flujos para procesarlos a medida. Amazon Data Firehose carga flujos en destinos como S3, Redshift u OpenSearch.

#### ¿Qué es Amazon OpenSearch Service?

Un servicio gestionado para clústeres de OpenSearch (y del antiguo Elasticsearch), usado para analizar registros, búsqueda de texto completo y observabilidad.

#### ¿Qué es Amazon QuickSight?

Un servicio de inteligencia de negocio serverless para crear cuadros de mando e informes interactivos, con análisis basados en aprendizaje automático y preguntas en lenguaje natural.

<!-- challenge -->

Los ingenieros de soporte quieren buscar por palabra clave en los logs de errores de la aplicación segundos después de cada error. ¿Qué servicio sugieres?

<!-- solution -->

Amazon OpenSearch Service, alimentado con los logs (por ejemplo mediante Firehose o suscripciones de CloudWatch), con OpenSearch Dashboards para búsquedas y visualizaciones.

<!-- takeaways -->

- Kinesis captura y entrega datos de streaming.
- OpenSearch potencia la búsqueda y la analítica de logs.
- QuickSight ofrece dashboards de BI serverless.

### Redes y entrega de contenidos

<!-- unit: Componentes de una VPC -->

<!-- goals -->

- Describir VPCs, bloques CIDR y subredes.
- Enrutar tráfico con internet gateways, NAT gateways y bastiones.

<!-- concept -->

Una VPC es tu red privada en una región, con un rango de direcciones que eliges. Las subredes la dividen por zona y por exposición. Lo que hace pública a una subred no es una casilla sino una ruta a un internet gateway; las privadas no la tienen, así sus recursos no son alcanzables desde internet.

Los recursos privados igual necesitan descargar actualizaciones, lo que los NAT gateways permiten en una sola dirección. El acceso administrativo pasa por un bastión endurecido o, mejor, Session Manager.

<!-- example -->

```text
VPC 10.0.0.0/16
 ├─ public subnet  10.0.1.0/24  (AZ a)  route 0.0.0.0/0 → internet gateway   [load balancer, NAT]
 └─ private subnet 10.0.11.0/24 (AZ a)  route 0.0.0.0/0 → NAT gateway        [app servers, DB]
```

#### ¿Qué es Amazon VPC?

Virtual Private Cloud es una red virtual aislada lógicamente, dentro de una región, en la que lanzas recursos. Eliges su rango de IP y creas subredes, tablas de rutas y puertas de enlace.

#### ¿Qué es un bloque CIDR?

Una notación para un rango de direcciones IP, como 10.0.0.0/16, que se usa para definir el espacio de direcciones de una VPC y sus subredes.

#### ¿Qué diferencia hay entre una subred pública y una privada?

Una subred pública tiene una ruta hacia una puerta de enlace de internet, así que los recursos con IP pública son accesibles desde internet. Una subred privada no tiene esa ruta: sus recursos solo salen a internet, si acaso, a través de una puerta de enlace NAT.

#### ¿Qué es una puerta de enlace de internet?

Un componente de la VPC que permite la comunicación entre los recursos de la VPC e internet.

#### ¿Qué es una puerta de enlace NAT?

Un servicio gestionado que permite que las instancias de subredes privadas inicien conexiones salientes a internet (para actualizaciones, por ejemplo) mientras bloquea las conexiones entrantes no solicitadas.

#### ¿Qué es un host bastión?

Una instancia en una subred pública que sirve de punto de entrada protegido para acceder por SSH o RDP a instancias de subredes privadas. Systems Manager Session Manager suele sustituirlo.

<!-- challenge -->

Los servidores de base de datos no deben ser alcanzables desde internet pero necesitan descargar parches del sistema operativo. ¿Dónde los pones y cómo obtienen los parches?

<!-- solution -->

En subredes privadas sin ruta al internet gateway, con una ruta a un NAT gateway en una subred pública solo para tráfico saliente. Mejor aún, usar VPC endpoints y Systems Manager Patch Manager.

<!-- takeaways -->

- Una ruta a un internet gateway hace pública una subred.
- Los NAT gateways permiten salida a internet solo de ida.
- Pon bases de datos y servidores de app en subredes privadas.

<!-- unit: Seguridad de red y acceso privado -->

<!-- goals -->

- Comparar security groups y network ACLs.
- Llegar a servicios de AWS de forma privada y registrar el tráfico de red.

<!-- concept -->

La defensa de red tiene dos capas. Los security groups protegen cada recurso y recuerdan las conexiones, así las respuestas vuelven solas. Las network ACLs protegen subredes enteras, evalúan reglas en orden y necesitan reglas explícitas en ambos sentidos. La mayoría de diseños se apoya en los security groups y mantiene simples las ACLs.

El tráfico hacia los servicios de AWS tampoco necesita internet: endpoints y PrivateLink lo mantienen en la red de AWS. Los Flow Logs registran lo que realmente pasó.

<!-- example -->

| | Security group | Network ACL |
|---|---|---|
| Se aplica a | Interfaz de red | Subred |
| Estado | Stateful | Stateless |
| Reglas | Solo permitir | Permitir y denegar, numeradas |

#### ¿Qué diferencia hay entre un grupo de seguridad y una ACL de red?

Un grupo de seguridad actúa a nivel de instancia (interfaz de red), tiene estado y solo admite reglas de permiso. Una ACL de red actúa a nivel de subred, no tiene estado (el tráfico de respuesta debe permitirse explícitamente), admite reglas de permiso y de denegación, y evalúa las reglas por orden de número.

#### ¿Qué son los VPC Flow Logs?

Registros del tráfico IP que entra y sale de las interfaces de red de una VPC, enviados a CloudWatch Logs o S3 para diagnosticar problemas y analizar la seguridad.

#### ¿Qué es un punto de enlace de VPC (VPC endpoint)?

Una conexión privada desde una VPC a servicios de AWS sin pasar por internet. Los puntos de enlace de puerta de enlace sirven S3 y DynamoDB. Los puntos de enlace de interfaz (AWS PrivateLink) sirven muchos otros servicios.

#### ¿Qué es AWS PrivateLink?

Una tecnología que expone servicios de forma privada entre VPC y cuentas mediante puntos de enlace de interfaz, manteniendo el tráfico dentro de la red de AWS.

<!-- challenge -->

Debes bloquear un rango de IPs maliciosas para que no llegue a ninguna instancia de una subred. ¿Security group o NACL?

<!-- solution -->

Una network ACL con una regla de deny para ese rango, numerada antes de las reglas de allow: los security groups no pueden denegar, solo permitir.

<!-- takeaways -->

- Security groups: stateful, por recurso, solo permitir.
- NACLs: stateless, por subred, permitir y denegar.
- Los endpoints mantienen privado el tráfico hacia AWS.

<!-- unit: Conectar redes -->

<!-- goals -->

- Conectar VPCs con peering y Transit Gateway.
- Conectar oficinas y usuarios con VPN y Direct Connect.

<!-- concept -->

A medida que las empresas crecen, las redes se multiplican: muchas VPCs, oficinas, centros de datos y trabajadores remotos. El peering conecta dos VPCs directamente, pero no se encadena, así que muchas VPCs terminan en una malla. Transit Gateway reemplaza la malla por un hub.

Para enlaces on-premises, la VPN es rápida y cifrada sobre internet; Direct Connect es una línea privada con rendimiento estable que tarda semanas en montarse. Client VPN atiende a usuarios individuales.

<!-- example -->

| Necesidad | Servicio |
|---|---|
| Dos VPCs comparten una base de datos | VPC peering |
| 40 VPCs y dos centros de datos | Transit Gateway |
| Enlace de oficina esta semana | Site-to-Site VPN |
| 10 Gbps estables hacia AWS | Direct Connect |
| Empleados remotos | Client VPN |

#### ¿Qué es el emparejamiento de VPC (VPC peering)?

Una conexión de red privada entre dos VPC (de la misma o distinta cuenta o región). No es transitiva.

#### ¿Qué es AWS Transit Gateway?

Un concentrador que conecta muchas VPC y redes locales a través de una sola puerta de enlace, en lugar de mallas complejas de emparejamientos.

#### ¿Qué es AWS Site-to-Site VPN?

Una conexión IPsec cifrada entre una red local y una VPC a través de internet. Es rápida de configurar, pero su rendimiento depende de internet.

#### ¿Qué es AWS Direct Connect?

Una conexión de red privada y dedicada entre tus instalaciones y AWS. Ofrece ancho de banda y latencia constantes y puede reducir los costos de transferencia, pero tarda semanas en instalarse. No está cifrada por defecto.

#### ¿Qué es AWS Client VPN?

Un servicio de VPN gestionado que permite a usuarios individuales conectarse de forma segura a AWS y a redes locales desde sus dispositivos.

<!-- challenge -->

Una empresa necesita un enlace confiable y de gran ancho de banda con AWS pero no puede esperar meses, y debe quedar cubierta si el enlace falla. ¿Qué montas?

<!-- solution -->

Pedir Direct Connect para el ancho de banda estable y montar de inmediato una Site-to-Site VPN; mantener la VPN como camino de respaldo cuando Direct Connect esté activo.

<!-- takeaways -->

- El peering une dos VPCs; Transit Gateway une muchas.
- La VPN es rápida y cifrada; Direct Connect, privada y estable.
- Client VPN conecta a usuarios individuales.

<!-- unit: DNS y entrega de contenido -->

<!-- goals -->

- Enrutar usuarios con Route 53 y sus políticas de enrutamiento.
- Acelerar aplicaciones con CloudFront, Global Accelerator y API Gateway.

<!-- concept -->

Los usuarios llegan a las aplicaciones mediante nombres y redes que puedes moldear. Route 53 responde consultas DNS y puede enviar a los usuarios al endpoint más cercano, más sano o con un peso dado. CloudFront cachea contenido cerca de los usuarios para que la mayoría de peticiones nunca lleguen a tus servidores. Global Accelerator pone el tráfico pronto en la red troncal de AWS para lo que no se cachea.

API Gateway pone delante de las APIs autenticación, throttling y monitoreo, a menudo frente a Lambda.

<!-- example -->

| Objetivo | Política de Route 53 |
|---|---|
| Enviar el 10 % de los usuarios a una versión nueva | Weighted |
| Conmutar a una región de respaldo | Failover |
| Servir desde la región más rápida | Latency |
| Servir contenido francés en Francia | Geolocation |

#### ¿Qué es Amazon Route 53?

Un servicio DNS de alta disponibilidad y registrador de dominios, con comprobaciones de estado y políticas de enrutamiento.

#### ¿Cuáles son las políticas de enrutamiento de Route 53?

Simple, ponderada, basada en latencia, conmutación por error, geolocalización, geoproximidad, basada en IP y respuesta de varios valores.

#### ¿Qué es Amazon CloudFront?

Una red de entrega de contenidos que guarda contenido en caché en ubicaciones de borde cercanas a los usuarios, reduciendo la latencia. Funciona con orígenes como S3, balanceadores de carga o cualquier servidor HTTP, admite HTTPS y se integra con WAF y Shield.

#### ¿Qué es AWS Global Accelerator?

Un servicio que enruta el tráfico de los usuarios por la red global de AWS a través de dos direcciones IP anycast estáticas, mejorando el rendimiento y la disponibilidad de aplicaciones TCP/UDP en varias regiones. A diferencia de CloudFront, no guarda en caché.

#### ¿Qué es Amazon API Gateway?

Un servicio gestionado para crear, publicar, proteger y supervisar API REST, HTTP y WebSocket, a menudo delante de funciones Lambda.

<!-- challenge -->

Un sitio alojado en eu-west-1 va lento para usuarios en Asia, sobre todo por imágenes grandes. ¿Qué agregas primero?

<!-- solution -->

Amazon CloudFront delante del sitio (o del bucket S3 con las imágenes), para que el contenido se cachee en edge locations cerca de los usuarios asiáticos.

<!-- takeaways -->

- Route 53 enruta por peso, latencia, salud o ubicación.
- CloudFront cachea contenido en el borde.
- API Gateway pone delante de las APIs protección y control.

<!-- stage: Operar y pagar -->

### Gestión, gobernanza y herramientas para desarrolladores

<!-- unit: Monitoreo y auditoría -->

<!-- goals -->

- Distinguir CloudWatch, CloudTrail y Config.
- Rastrear peticiones y seguir la salud de los servicios de AWS.

<!-- concept -->

Tres preguntas necesitan tres servicios. ¿Está sano? CloudWatch recoge métricas y logs y lanza alarmas. ¿Quién hizo qué? CloudTrail registra cada llamada a la API. ¿Está configurado como debe? Config registra la configuración de los recursos en el tiempo y la compara con reglas.

Para aplicaciones distribuidas, X-Ray sigue una petición a través de los servicios, y el Health Dashboard te avisa cuando AWS mismo tiene un problema que te afecta.

<!-- example -->

| Pregunta | Servicio |
|---|---|
| ¿CPU por encima del 80 % durante 10 minutos? | Alarma de CloudWatch |
| ¿Quién borró el security group? | CloudTrail |
| ¿Están cifrados todos los buckets? | Regla de Config |
| ¿Qué servicio ralentiza el checkout? | X-Ray |
| ¿Una caída de AWS afecta mi región? | Health Dashboard |

#### ¿Qué es Amazon CloudWatch?

Un servicio de monitorización y observabilidad: métricas, alarmas, registros (CloudWatch Logs), paneles y eventos, para recursos de AWS y aplicaciones.

#### ¿Qué es AWS CloudTrail?

Un servicio que registra las llamadas a la API y la actividad de la cuenta (quién hizo qué, cuándo y desde dónde) para la gobernanza, el cumplimiento y la auditoría. Los registros pueden enviarse a S3 y analizarse con CloudTrail Lake.

#### ¿Qué diferencia hay entre CloudWatch y CloudTrail?

CloudWatch supervisa el rendimiento y el estado (métricas, registros, alarmas). CloudTrail audita las acciones (llamadas a la API hechas en la cuenta).

#### ¿Qué es AWS Config?

Un servicio que registra la configuración de los recursos y sus cambios a lo largo del tiempo y la evalúa frente a reglas, para auditar el cumplimiento y diagnosticar problemas.

#### ¿Qué es AWS X-Ray?

Un servicio que traza las solicitudes a través de aplicaciones distribuidas para encontrar cuellos de botella y errores.

#### ¿Qué es el AWS Health Dashboard?

Una vista del estado de los servicios de AWS y de los eventos que afectan a tus propios recursos, como mantenimientos programados o incidencias en tus regiones.

<!-- challenge -->

Un security group de producción se abrió anoche a todo internet. ¿Cómo encuentras quién fue y recibes una alerta la próxima vez?

<!-- solution -->

Buscar en CloudTrail la llamada `AuthorizeSecurityGroupIngress` para hallar la identidad y la hora. Agregar una regla de Config (o de EventBridge) que marque security groups abiertos y avise al equipo, con remediación automática si se quiere.

<!-- takeaways -->

- CloudWatch: salud. CloudTrail: actividad. Config: configuración.
- X-Ray rastrea peticiones distribuidas.
- El Health Dashboard reporta problemas de AWS que te afectan.

<!-- unit: Administrar y automatizar -->

<!-- goals -->

- Interactuar con AWS mediante la consola, la CLI, los SDKs e IaC.
- Automatizar infraestructura, operación y despliegues.

<!-- concept -->

Todo en AWS es una API, y la consola, la CLI y los SDKs son solo formas distintas de llamarla. El trabajo repetible debe pasar por código: CloudFormation y CDK describen la infraestructura, Systems Manager ejecuta tareas operativas sobre flotas y los servicios Code* compilan y despliegan software.

Trusted Advisor cierra el círculo revisando la cuenta y señalando ahorros, riesgos y límites.

<!-- example -->

```yaml
# CloudFormation: a versioned, private S3 bucket
Resources:
  ReportsBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration: {Status: Enabled}
      PublicAccessBlockConfiguration: {BlockPublicAcls: true, BlockPublicPolicy: true,
                                       IgnorePublicAcls: true, RestrictPublicBuckets: true}
```

#### ¿De qué formas se puede interactuar con AWS?

La AWS Management Console (web), la AWS CLI, los SDK para lenguajes de programación, la infraestructura como código (CloudFormation, CDK) y AWS CloudShell (un shell en el navegador ya autenticado).

#### ¿Qué es AWS CloudFormation?

Infraestructura como código: describes los recursos en plantillas JSON o YAML, y CloudFormation los crea, actualiza y elimina como una pila, en el orden correcto.

#### ¿Qué es el AWS Cloud Development Kit (CDK)?

Un framework para definir infraestructura en la nube con lenguajes de programación (TypeScript, Python, Java, C#, Go). Genera plantillas de CloudFormation.

#### ¿Qué es AWS Systems Manager?

Un conjunto de herramientas operativas para gestionar servidores EC2 y locales a escala: Session Manager, Patch Manager, Run Command, Parameter Store, Automation e inventario.

#### ¿Qué son AWS CodeCommit, CodeBuild, CodeDeploy y CodePipeline?

Herramientas de CI/CD: CodeBuild compila y prueba el código, CodeDeploy automatiza los despliegues en EC2, Lambda, ECS y servidores locales, CodePipeline orquesta las canalizaciones de publicación. CodeCommit es un servicio de alojamiento Git cerrado a nuevos clientes.

#### ¿Qué es AWS Trusted Advisor?

Un servicio que inspecciona tu cuenta y recomienda mejoras en cinco categorías: optimización de costos, rendimiento, seguridad, tolerancia a fallos y cuotas de servicio. Los planes de soporte Basic y Developer solo tienen las comprobaciones principales. Business y superiores tienen el conjunto completo.

<!-- challenge -->

Un equipo crea entornos de prueba haciendo clics en la consola, y cada uno termina un poco distinto. ¿Qué propones?

<!-- solution -->

Definir el entorno en CloudFormation o CDK, guardarlo en Git y crear cada entorno desde la misma plantilla con parámetros. Desplegar los cambios mediante un pipeline en vez de la consola.

<!-- takeaways -->

- Consola, CLI y SDKs llaman todos a las mismas APIs.
- CloudFormation y CDK hacen repetible la infraestructura.
- Trusted Advisor revisa costos, seguridad, límites y más.

<!-- unit: Desacoplar aplicaciones -->

<!-- goals -->

- Elegir entre SQS, SNS y EventBridge.
- Desacoplar productores de consumidores.

<!-- concept -->

Cuando un componente llama directamente a otro, la lentitud de uno contagia a ambos. Los servicios de mensajería rompen ese vínculo. Una cola guarda el trabajo hasta que un consumidor esté listo; un tópico entrega cada mensaje a muchos suscriptores a la vez; un bus de eventos enruta eventos por contenido a los destinos correctos, incluidos servicios de AWS y SaaS.

La diferencia está en la entrega: un consumidor por mensaje, todos los suscriptores o enrutamiento por reglas.

<!-- example -->

| Patrón | Servicio |
|---|---|
| Pedidos procesados por un grupo de workers | SQS |
| Enviar una alerta a email, SMS y una Lambda | SNS |
| Enrutar eventos "pedido realizado" a facturación y analítica por reglas | EventBridge |

#### ¿Qué es Amazon SQS?

Simple Queue Service es una cola de mensajes totalmente gestionada que desacopla componentes. Las colas estándar ofrecen un alto rendimiento con entrega al menos una vez. Las colas FIFO garantizan el orden y el procesamiento exactamente una vez.

#### ¿Qué diferencia hay entre SQS y SNS?

SQS es una cola: los consumidores sondean los mensajes y cada mensaje lo procesa un consumidor. SNS es publicación/suscripción: un mensaje publicado en un tema se envía a todos los suscriptores (SQS, Lambda, HTTP, correo, SMS). A menudo se combinan en un patrón de distribución (fan-out).

#### ¿Qué es Amazon EventBridge?

Un bus de eventos serverless que enruta eventos de servicios de AWS, aplicaciones SaaS y tu propio código hacia destinos según reglas, y programa tareas (EventBridge Scheduler).

<!-- challenge -->

Un servicio de pedidos llama directamente al servicio de correo; cuando el correo va lento, el checkout supera el timeout. ¿Cómo lo arreglas?

<!-- solution -->

Publicar los eventos de pedido en una cola SQS (o un tópico SNS con suscripción SQS) y dejar que el servicio de correo los consuma a su ritmo. El checkout termina en cuanto el mensaje queda guardado.

<!-- takeaways -->

- Las colas SQS dan un consumidor por mensaje.
- SNS reparte a muchos suscriptores.
- EventBridge enruta eventos por reglas.

### Facturación, precios y soporte

<!-- unit: Qué mueve el costo -->

<!-- goals -->

- Nombrar los principales factores de costo en AWS.
- Estimar costos y usar con criterio la capa gratuita.

<!-- concept -->

AWS factura sobre todo tres cosas: tiempo de cómputo, datos guardados y datos que salen de AWS. La mayoría de sorpresas vienen de olvidar una de ellas, como instancias ociosas o grandes transferencias de salida. La capa gratuita ayuda a aprender, con límites fáciles de superar.

El trabajo de costos empieza antes de construir, con una estimación, y sigue después, quitando desperdicio y comprometiendo el uso estable.

<!-- example -->

| Factor de costo | Ejemplo | Palanca |
|---|---|---|
| Cómputo | 10 instancias 24/7 | Ajustar tamaño, Savings Plans, apagar si está ociosa |
| Almacenamiento | 50 TB en S3 Standard | Ciclo de vida a clases más baratas |
| Transferencia de salida | Video servido desde EC2 | CloudFront, compresión |

#### ¿Cuáles son los tres factores fundamentales del costo en AWS?

El cómputo, el almacenamiento y la transferencia de datos salientes. La transferencia de datos entrantes suele ser gratuita.

#### ¿Qué es la capa gratuita de AWS (Free Tier)?

Ofertas para probar AWS sin costo dentro de ciertos límites. Incluye ofertas siempre gratuitas (por ejemplo solicitudes de Lambda y almacenamiento de DynamoDB hasta un límite), créditos u ofertas de 12 meses para cuentas nuevas según el plan de la cuenta, y pruebas gratuitas cortas de servicios concretos. El uso que supera los límites se factura.

#### ¿Qué es la AWS Pricing Calculator?

Una herramienta gratuita para estimar el costo de una arquitectura antes de construirla.

#### ¿Cómo se pueden reducir los costos en AWS?

Ajustar el tamaño de las instancias, apagar los recursos que no se usan, usar Savings Plans o instancias reservadas para cargas estables y spot para las interrumpibles, elegir clases de almacenamiento más baratas con reglas de ciclo de vida, usar serverless para cargas variables, reducir la transferencia de datos (por ejemplo con CloudFront y puntos de enlace de VPC) y controlar el gasto con etiquetas, Budgets y Cost Explorer.

<!-- challenge -->

La cuenta Free Tier de un estudiante generó una factura de 90 USD. Nombra dos causas probables y cómo evitarlas.

<!-- solution -->

Recursos fuera de los límites gratuitos (una instancia más grande, un NAT gateway, una instancia RDS encendida) o uso después de terminar las ofertas de 12 meses. Configurar una alerta de presupuesto con un monto bajo y borrar los recursos tras los experimentos.

<!-- takeaways -->

- Cómputo, almacenamiento y transferencia de salida mueven el costo.
- Estima con el Pricing Calculator antes de construir.
- La capa gratuita tiene límites; configura alertas de presupuesto.

<!-- unit: Seguir y controlar el gasto -->

<!-- goals -->

- Analizar y proyectar el gasto con Cost Explorer y exportaciones detalladas.
- Controlar y atribuir costos con presupuestos, tags y facturación consolidada.

<!-- concept -->

No puedes controlar lo que no ves. Cost Explorer muestra tendencias y proyecciones; las exportaciones detalladas dan datos línea por línea para tu propio análisis; los tags atribuyen costos a proyectos y equipos. Los presupuestos agregan alertas, y Compute Optimizer sugiere mejores tamaños según el uso real.

En las organizaciones, la facturación consolidada combina el uso de todas las cuentas, lo que alcanza antes los descuentos por volumen y deja que los compromisos beneficien a toda la empresa.

<!-- example -->

```bash
aws budgets create-budget --account-id 123456789012 --budget '{
  "BudgetName": "data-team-monthly", "BudgetLimit": {"Amount": "5000", "Unit": "USD"},
  "TimeUnit": "MONTHLY", "BudgetType": "COST",
  "CostFilters": {"TagKeyValue": ["user:team$data"]}}'
```

#### ¿Qué es AWS Cost Explorer?

Una herramienta para visualizar, analizar y prever los costos y el uso a lo largo del tiempo, con filtros por servicio, cuenta o etiqueta, y recomendaciones de Savings Plans y de ajuste de tamaño.

#### ¿Qué es AWS Budgets?

Un servicio para fijar presupuestos de costo, uso o reservas y recibir alertas (o lanzar acciones) cuando el gasto real o previsto supera un umbral.

#### ¿Qué es el AWS Cost and Usage Report, ahora Data Exports?

Los datos de facturación más detallados, entregados en S3 con granularidad horaria o diaria, para analizarlos con Athena, QuickSight u otras herramientas.

#### ¿Qué son las etiquetas de asignación de costos?

Etiquetas (pares clave-valor como `project=lakehouse`) activadas en la consola de facturación para poder agrupar y filtrar los costos por ellas en Cost Explorer y los informes.

#### ¿Qué es la facturación unificada de AWS Organizations?

Una sola factura para todas las cuentas de una organización, que paga la cuenta de administración. El uso se suma para los descuentos por volumen, y los descuentos de instancias reservadas y Savings Plans pueden compartirse entre cuentas.

#### ¿Qué es AWS Compute Optimizer?

Un servicio que aplica aprendizaje automático a las métricas de uso para recomendar tipos de instancia EC2, grupos de Auto Scaling, volúmenes EBS, funciones Lambda y configuraciones de ECS en Fargate óptimos.

<!-- challenge -->

Finanzas quiere el costo mensual de AWS de cada equipo, pero todos comparten cuentas. ¿Qué configuras?

<!-- solution -->

Definir un tag `team`, exigirlo en los recursos (tag policies, SCPs o IaC), activarlo como cost allocation tag y reportar por tag en Cost Explorer con un presupuesto por equipo. Separar cuentas por equipo es la solución a más largo plazo.

<!-- takeaways -->

- Cost Explorer muestra y proyecta el gasto.
- Tags y cuentas atribuyen costos a sus dueños.
- La facturación consolidada comparte descuentos entre cuentas.

<!-- unit: Soporte y socios -->

<!-- goals -->

- Comparar los planes de AWS Support y lo que incluye cada uno.
- Saber dónde conseguir ayuda: re:Post, TAMs, Marketplace y socios.

<!-- concept -->

La ayuda en AWS viene por niveles. Todos reciben documentación, la comunidad re:Post y chequeos básicos. Los planes pagos agregan casos técnicos con tiempos de respuesta más rápidos a medida que sube el plan, y los niveles más altos suman un Technical Account Manager que conoce tu entorno.

Más allá de AWS, los socios y Professional Services ofrecen consultoría, y el Marketplace vende software listo que corre en AWS, facturado en tu cuenta de AWS.

<!-- example -->

| Necesidad | Plan o recurso |
|---|---|
| Aprender, sin producción | Basic + re:Post |
| Carga de producción, problemas en horario laboral | Developer o Business |
| Crítica para el negocio, respuesta rápida 24/7 | Business o Enterprise On-Ramp |
| TAM dedicado, sistemas críticos | Enterprise |

#### ¿Cuáles son los planes de AWS Support?

- **Basic:** gratuito. Documentación, foros, AWS re:Post, Health Dashboard y las comprobaciones principales de Trusted Advisor.
- **Developer:** acceso por correo a ingenieros de soporte en horario laboral, para pruebas y desarrollo.
- **Business:** soporte 24/7 por teléfono, chat y correo, Trusted Advisor completo y respuesta rápida si un sistema de producción cae.
- **Enterprise On-Ramp:** añade un grupo de Technical Account Managers y una respuesta más rápida para sistemas críticos.
- **Enterprise:** un Technical Account Manager asignado, la respuesta más rápida si un sistema crítico cae y un servicio de conserjería para la facturación.

Consulta la página de AWS Support para ver los nombres y los tiempos de respuesta actuales, porque AWS los revisa.

#### ¿Qué es un Technical Account Manager (TAM)?

Un interlocutor técnico de AWS dedicado a los clientes Enterprise, que ofrece orientación proactiva sobre arquitectura, operaciones y buenas prácticas.

#### ¿Qué es AWS re:Post?

Un sitio comunitario de preguntas y respuestas, moderado con expertos de AWS, que sustituyó a los foros de AWS.

#### ¿Qué es AWS Marketplace?

Un catálogo digital seleccionado de software, datos y servicios de terceros que funcionan en AWS, que se compran y facturan a través de tu cuenta de AWS.

#### ¿Qué son AWS Professional Services y la AWS Partner Network?

AWS Professional Services es el equipo de consultoría propio de AWS. La AWS Partner Network (APN) es la comunidad mundial de socios consultores y tecnológicos que ayudan a los clientes a construir en AWS.

<!-- challenge -->

El sitio de producción de una empresa se cae a las 2 a. m. y tiene el plan Developer. ¿Qué soporte puede recibir y qué plan encajaría mejor?

<!-- solution -->

Developer da soporte por correo en horario laboral para orientación general, no casos urgentes de producción. Business (o superior) agrega teléfono y chat 24/7 con respuesta rápida ante caídas de producción.

<!-- takeaways -->

- Los planes difieren en tiempos de respuesta y acceso.
- Los planes Enterprise incluyen un TAM.
- Marketplace y socios amplían lo que ofrece AWS.
