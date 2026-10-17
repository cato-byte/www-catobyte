## Guía de estudio AWS Certified Cloud Practitioner

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio AWS Certified Cloud Practitioner: unas 200 preguntas](../../images/aws_practicioner_guide_title_img.png)

Unas 200 preguntas con respuestas breves que usé para preparar el examen AWS Certified Cloud Practitioner (CLF-C02), que aprobé en octubre de 2026. Siguen los cuatro dominios del examen: conceptos de la nube, seguridad y cumplimiento, tecnología y servicios de la nube, y facturación, precios y soporte. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía. Los servicios y los precios cambian, así que consulta la documentación de AWS antes de fiarte de una cifra.

<!-- QA -->

### Conceptos de la nube

#### ¿Qué es la computación en la nube?

La entrega bajo demanda de recursos de TI (cómputo, almacenamiento, bases de datos, red, software) a través de internet, con pago por uso. En lugar de comprar y gestionar centros de datos, alquilas capacidad a un proveedor y la liberas cuando ya no la necesitas.

#### ¿Cuáles son las seis ventajas de la computación en la nube según AWS?

1. Cambiar gasto fijo (inversión de capital) por gasto variable.
2. Beneficiarse de enormes economías de escala.
3. Dejar de adivinar la capacidad.
4. Aumentar la velocidad y la agilidad.
5. Dejar de gastar dinero en operar y mantener centros de datos.
6. Llegar a todo el mundo en minutos.

#### ¿Qué modelos de implementación de la nube admite AWS?

- **Nube (nativo de la nube):** todo se ejecuta en la nube pública.
- **Local (nube privada):** recursos en tu propio centro de datos, a menudo con virtualización y herramientas de gestión. AWS Outposts lleva la infraestructura de AWS a tus instalaciones.
- **Híbrido:** recursos en la nube conectados a infraestructura local, por ejemplo durante una migración o para datos que deben quedarse en casa.

#### ¿Qué significan IaaS, PaaS y SaaS? Da ejemplos de AWS.

- **IaaS (infraestructura como servicio):** obtienes máquinas virtuales, almacenamiento y redes, y gestionas el sistema operativo y todo lo que está por encima. Ejemplo: Amazon EC2.
- **PaaS (plataforma como servicio):** el proveedor gestiona la infraestructura y la plataforma, tú despliegas código. Ejemplo: AWS Elastic Beanstalk.
- **SaaS (software como servicio):** una aplicación completa que se usa por internet. Ejemplos: Amazon WorkMail, Amazon Chime, Amazon QuickSight.

#### ¿Qué es la elasticidad?

La capacidad de obtener recursos cuando los necesitas y liberarlos cuando no, siguiendo la demanda de forma automática. Ejemplo: un grupo de Auto Scaling que añade instancias EC2 durante un pico de tráfico y las retira después.

#### ¿Qué es la escalabilidad?

La capacidad de un sistema de soportar una carga creciente añadiendo recursos. Escalar verticalmente significa recursos más grandes, escalar horizontalmente significa más recursos. La elasticidad es escalabilidad que además reduce los recursos automáticamente.

#### ¿Qué diferencia hay entre escalar vertical y horizontalmente?

Escalar verticalmente sustituye un recurso por otro más grande (un tipo de instancia mayor). Es sencillo, pero tiene un límite y suele requerir un reinicio. Escalar horizontalmente añade más recursos del mismo tamaño detrás de un balanceador de carga. No tiene límite práctico y mejora la disponibilidad.

#### ¿Qué ventajas tiene usar AWS en lugar de una infraestructura local?

Sin compra inicial de hardware, pago solo por lo que usas, capacidad en minutos en lugar de meses, alcance global, servicios gestionados que eliminan trabajo sin valor diferencial (parches, copias de seguridad), seguridad y certificaciones de cumplimiento integradas, y la posibilidad de experimentar barato y cerrar lo que no funciona.

#### ¿Qué diferencia hay entre CapEx y OpEx?

El gasto de capital (CapEx) es una inversión inicial en activos físicos, como servidores, que se amortiza durante años. El gasto operativo (OpEx) es el gasto continuo en servicios. La nube convierte la mayor parte del CapEx de TI en OpEx.

#### ¿Qué significa "economías de escala" en la nube?

AWS compra hardware, energía y red a una escala que ningún cliente alcanza por separado, así que su costo por unidad es menor. Parte del ahorro se traslada a los clientes con bajadas de precio, que AWS ha aplicado muchas veces.

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

#### ¿Qué es la agilidad en el contexto de la nube?

La velocidad a la que puedes disponer de recursos y probar ideas nuevas. Recursos que tardaban semanas en llegar están disponibles en minutos, así que el costo y el tiempo de experimentar bajan mucho.

#### ¿Qué significa "llegar a todo el mundo en minutos"?

Que puedes desplegar una aplicación en regiones de AWS de todo el mundo con unos pocos clics o llamadas a la API, y dar menor latencia a los usuarios sin construir centros de datos en otros países.

#### ¿Qué es un servicio gestionado?

Un servicio en el que AWS opera la infraestructura y el software subyacentes (aprovisionamiento, parches, copias de seguridad, escalado) y tú solo lo usas. Amazon RDS es una base de datos gestionada. Ejecutar una base de datos en EC2 no lo es: todo eso lo haces tú.

#### ¿Qué significa "serverless" (sin servidor)?

Ejecutas código o usas un servicio sin aprovisionar ni gestionar servidores. La capacidad escala automáticamente y pagas por el uso real. Ejemplos: AWS Lambda, Amazon S3, Amazon DynamoDB, AWS Fargate, Amazon Athena.

#### ¿Qué es el AWS Cloud Adoption Framework (AWS CAF)?

Una guía que ayuda a las organizaciones a planificar su transformación a la nube. Agrupa las capacidades en seis perspectivas: Negocio, Personas, Gobernanza (orientadas al negocio) y Plataforma, Seguridad, Operaciones (técnicas).

#### ¿Qué son las 7 R de la migración?

Retirar (Retire), Conservar (Retain), Realojar (Rehost, "lift and shift"), Reubicar (Relocate, por ejemplo VMware Cloud on AWS), Recomprar (Repurchase, pasar a SaaS), Redefinir la plataforma (Replatform, "lift, tinker and shift", como pasar a RDS) y Refactorizar o rediseñar (Refactor, reconstruir de forma nativa para la nube).

### Infraestructura global y Well-Architected Framework

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

#### ¿Qué es una ubicación de borde (edge location)?

Un emplazamiento que ejecuta las cachés de CloudFront y el DNS de Route 53 (y servicios como Lambda@Edge) cerca de los usuarios finales. Hay muchas más ubicaciones de borde que regiones.

#### ¿Qué es una Local Zone?

Una extensión de una región situada cerca de una gran ciudad, que ejecuta algunos servicios (como EC2 y EBS) para dar una latencia de milisegundos de un dígito a los usuarios de esa zona.

#### ¿Qué es AWS Wavelength?

Infraestructura integrada en las redes 5G de los operadores de telecomunicaciones, para que las aplicaciones lleguen a los dispositivos móviles con una latencia muy baja.

#### ¿Qué es AWS Outposts?

Racks de hardware gestionado por AWS instalados en tu propio centro de datos, que ejecutan servicios de AWS con las mismas API y herramientas. Se usan para baja latencia con sistemas locales, procesamiento local de datos o residencia de datos.

#### ¿Los servicios son globales o regionales?

La mayoría son regionales: los recursos viven en una región. Algunos son globales: IAM, Route 53, CloudFront, AWS Organizations y WAF para CloudFront. Otros, como las subredes de EC2 y los volúmenes EBS, están limitados a una zona de disponibilidad.

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

#### ¿Qué significa "diseñar para el fallo"?

Asumir que cualquier componente puede fallar y construir el sistema para que siga funcionando cuando ocurra: varias AZ, comprobaciones de estado, sustitución automática, reintentos y componentes desacoplados.

#### ¿Qué es el acoplamiento débil y qué servicios ayudan a lograrlo?

Diseñar los componentes para que un fallo o una lentitud en uno no se propague a los demás. Las colas (Amazon SQS), las notificaciones (Amazon SNS), los buses de eventos (Amazon EventBridge) y los balanceadores de carga permiten que los componentes se comuniquen sin depender directamente unos de otros.

#### ¿Qué diferencia hay entre una aplicación sin estado y una con estado?

Un componente sin estado no guarda datos de sesión entre solicitudes, así que cualquier instancia puede atender cualquier solicitud y se pueden añadir o quitar instancias libremente. El estado se guarda en otro sitio (DynamoDB, ElastiCache, S3). Los componentes con estado son más difíciles de escalar horizontalmente.

#### ¿Qué es la infraestructura como código y por qué la recomienda el Well-Architected Framework?

Definir la infraestructura en plantillas o código versionados (CloudFormation, AWS CDK) en lugar de clics manuales en la consola. Los entornos se vuelven reproducibles, revisables y rápidos de reconstruir, lo que favorece la excelencia operativa y la fiabilidad.

### Seguridad, modelo de responsabilidad compartida e IAM

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

#### ¿Qué es la autenticación multifactor (MFA) y qué dispositivos admite AWS?

Un segundo factor además de la contraseña. AWS admite llaves de acceso (passkeys) y llaves de seguridad FIDO2, aplicaciones de autenticación virtuales y tokens TOTP físicos.

#### ¿Qué son las claves de acceso?

Un par formado por un ID de clave de acceso y una clave de acceso secreta, usado para firmar solicitudes programáticas (CLI, SDK). Son credenciales de larga duración: no las incluyas nunca en el código, rótalas y, siempre que puedas, usa roles o IAM Identity Center.

#### ¿Qué es AWS IAM Identity Center?

El sucesor de AWS Single Sign-On. Gestiona de forma centralizada el acceso de los empleados a varias cuentas de AWS y aplicaciones de negocio, con su propio directorio o un proveedor de identidades externo (Microsoft Entra ID, Okta, Active Directory).

#### ¿Qué es la federación de identidades?

Permitir que los usuarios inicien sesión con una identidad existente (directorio corporativo, proveedor SAML 2.0 u OIDC) y reciban credenciales temporales de AWS, sin crear usuarios de IAM para ellos.

#### ¿Qué es AWS STS?

AWS Security Token Service emite credenciales temporales con privilegios limitados, por ejemplo cuando se asume un rol o cuando un usuario federado inicia sesión.

#### ¿Qué es el informe de credenciales de IAM?

Un CSV a nivel de cuenta que lista todos los usuarios y el estado de sus credenciales: contraseñas, claves de acceso, MFA y fechas de último uso. Útil para auditorías.

#### ¿Qué es IAM Access Advisor?

Una vista que muestra para qué servicios tiene permisos un usuario, grupo o rol y cuándo los usó por última vez. Ayuda a eliminar permisos no utilizados.

#### ¿Qué es un ARN?

Un Amazon Resource Name identifica un recurso de forma única: `arn:partition:service:region:account-id:resource`, por ejemplo `arn:aws:s3:::my-bucket`.

#### ¿Qué es una política de contraseñas en IAM?

Reglas de la cuenta para las contraseñas de los usuarios de IAM: longitud mínima, tipos de caracteres obligatorios, caducidad e impedir su reutilización.

### Servicios de seguridad y cumplimiento

#### ¿Qué es AWS Organizations?

Un servicio para gestionar de forma centralizada varias cuentas de AWS: agruparlas en unidades organizativas (OU), aplicarles políticas y consolidar la facturación. Una cuenta de administración es la propietaria de la organización.

#### ¿Qué son las Service Control Policies (SCP)?

Políticas de AWS Organizations que fijan los permisos máximos de cuentas u OU. No conceden permisos: limitan lo que las políticas de IAM de esas cuentas pueden permitir, incluso para el usuario raíz de una cuenta miembro.

#### ¿Qué es AWS Control Tower?

Un servicio que configura y gobierna un entorno multicuenta seguro (una landing zone) según las buenas prácticas, con barreras de protección preventivas y de detección y un panel de control.

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

#### ¿Qué es AWS Artifact?

Un portal de autoservicio con los informes de cumplimiento de AWS (SOC, ISO, PCI DSS) y acuerdos (como el Business Associate Addendum para HIPAA).

#### ¿Qué es el programa de cumplimiento de AWS?

AWS mantiene certificaciones y acreditaciones (ISO 27001, SOC 1/2/3, PCI DSS, elegibilidad HIPAA, apoyo al RGPD) para su infraestructura. Los clientes heredan los controles de la infraestructura, pero deben hacer que sus propias cargas de trabajo cumplan.

#### ¿Hace falta permiso de AWS para hacer una prueba de penetración?

No para una lista de servicios permitidos (EC2, RDS, Lambda, CloudFront y otros). Algunas actividades siguen prohibidas, como los ataques DoS, que requieren un proceso de aprobación aparte para los eventos simulados.

#### ¿Qué es AWS Abuse y cuándo se contacta?

El equipo de AWS al que se notifica que recursos de AWS se están usando de forma abusiva, por ejemplo para spam, escaneo de puertos, ataques DoS o alojar malware.

### Cómputo: EC2, contenedores y serverless

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

#### ¿Qué es un grupo de seguridad?

Un cortafuegos virtual con estado para instancias (asociado a interfaces de red). Solo tiene reglas de permiso. El tráfico de respuesta se permite automáticamente, y por defecto se deniega todo el tráfico entrante y se permite todo el saliente.

#### ¿Qué es EC2 Auto Scaling?

Un servicio que añade o retira instancias EC2 de un grupo de Auto Scaling según políticas (seguimiento de objetivo, por pasos, programadas, predictivas) y sustituye las instancias en mal estado. Defines la capacidad mínima, deseada y máxima.

#### ¿Qué es Elastic Load Balancing y qué tipos tiene?

Un servicio que reparte el tráfico entre destinos de varias AZ y comprueba su estado.
- **Application Load Balancer:** HTTP/HTTPS, capa 7, enrutamiento por ruta y por host.
- **Network Load Balancer:** TCP/UDP/TLS, capa 4, rendimiento muy alto e IP estáticas.
- **Gateway Load Balancer:** capa 3, para dispositivos de red de terceros como cortafuegos.

#### ¿Qué es una dirección IP elástica?

Una dirección IPv4 pública estática que asignas a tu cuenta y puedes asociar a una instancia. Las direcciones IPv4 públicas se facturan por hora, estén asociadas o no.

#### ¿Qué son los datos de usuario (user data) de EC2?

Un script que se pasa al lanzar la instancia y se ejecuta en el primer arranque, para instalar software o configurar la instancia.

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

#### ¿Qué es AWS Elastic Beanstalk?

Una plataforma como servicio: subes el código de la aplicación (Java, .NET, Node.js, Python, PHP, Go, Ruby, Docker) y Beanstalk aprovisiona y gestiona EC2, el balanceo de carga, Auto Scaling y la monitorización. Los recursos subyacentes siguen visibles y configurables.

#### ¿Qué es Amazon Lightsail?

Un servicio simplificado de servidores privados virtuales, bases de datos y contenedores a un precio mensual previsible, pensado para webs sencillas y usuarios que empiezan en AWS.

#### ¿Qué es AWS Batch?

Un servicio que ejecuta trabajos de cómputo por lotes a cualquier escala, aprovisionando capacidad EC2 o Fargate (incluida spot) según los trabajos en cola.

#### ¿Qué es AWS App Runner?

Un servicio totalmente gestionado que construye y ejecuta aplicaciones web y API a partir de código fuente o de una imagen de contenedor, con escalado automático y HTTPS.

#### ¿Qué es el almacén de instancia de EC2 (instance store)?

Almacenamiento de bloques temporal conectado físicamente al servidor. Es muy rápido, pero sus datos se pierden cuando la instancia se detiene o se termina, así que sirve para búferes, cachés y datos temporales.

#### ¿Qué aportan EC2 Instance Connect o Session Manager?

Formas de acceder a las instancias sin gestionar claves SSH. Session Manager (parte de Systems Manager) funciona incluso sin abrir puertos de entrada, y registra las sesiones.

#### ¿Qué diferencia hay entre detener y terminar una instancia?

Detenerla la apaga: se conservan los volúmenes EBS raíz y solo pagas el almacenamiento, y puedes volver a arrancarla. Terminarla la elimina y, por defecto, también su volumen EBS raíz.

### Almacenamiento

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

#### ¿Qué son las políticas de ciclo de vida de S3?

Reglas que pasan automáticamente los objetos a clases de almacenamiento más baratas a partir de cierta antigüedad, o los eliminan (caducidad).

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

#### ¿Qué es AWS Storage Gateway?

Un servicio de almacenamiento híbrido que da a las aplicaciones locales acceso al almacenamiento en la nube. Tipos: S3 File Gateway, FSx File Gateway, Volume Gateway y Tape Gateway (biblioteca de cintas virtual para copias de seguridad).

#### ¿Qué es la familia AWS Snow?

Dispositivos físicos para mover grandes volúmenes de datos hacia o desde AWS sin conexión, o para procesar datos en el borde donde hay poca o ninguna conectividad (dispositivos AWS Snowball Edge).

#### ¿Qué es AWS Backup?

Un servicio centralizado para automatizar y auditar las copias de seguridad de varios servicios: EBS, EC2, RDS, DynamoDB, EFS, FSx, S3 y más, con planes de copia y copias entre regiones o entre cuentas.

#### ¿Qué es AWS DataSync?

Un servicio de transferencia de datos en línea que mueve datos entre almacenamiento local (NFS, SMB, HDFS, almacenes de objetos) y los servicios de almacenamiento de AWS, de forma rápida y con verificación.

#### ¿Qué durabilidad y disponibilidad tiene S3 Standard?

Está diseñado para una durabilidad del 99,999999999 % y una disponibilidad del 99,99 %, con los datos guardados en al menos tres AZ.

#### ¿Cuándo usarías S3 One Zone-IA?

Para datos de acceso poco frecuente que se pueden volver a generar, como copias de seguridad secundarias o datos derivados, cuando perder una AZ es aceptable a cambio de un precio menor.

### Bases de datos y analítica

#### ¿En qué se diferencia Amazon RDS de Amazon DynamoDB?

RDS es un servicio de bases de datos relacionales gestionado (SQL, esquemas, joins, transacciones) que ejecuta MySQL, PostgreSQL, MariaDB, Oracle, SQL Server o Db2 en instancias cuyo tamaño eliges. DynamoDB es una base de datos NoSQL serverless de clave-valor y documentos, con rendimiento de milisegundos de un dígito a cualquier escala, sin esquema fijo más allá de las claves y con escalado automático.

#### ¿Qué gestiona Amazon RDS por ti?

El aprovisionamiento, los parches del sistema operativo y de la base de datos, las copias de seguridad automáticas y la recuperación a un momento dado, la conmutación Multi-AZ, las réplicas de lectura, la monitorización y el crecimiento del almacenamiento. Tú gestionas el esquema, las consultas, los usuarios y el acceso de red.

#### ¿Qué diferencia hay entre RDS Multi-AZ y las réplicas de lectura?

Multi-AZ mantiene una o varias réplicas en espera síncronas en otra AZ para la alta disponibilidad y la conmutación automática. En su configuración clásica no sirve lecturas. Las réplicas de lectura son copias asíncronas para repartir el tráfico de lectura, posiblemente en otras regiones, y se pueden promocionar.

#### ¿Qué es Amazon Aurora?

Una base de datos relacional nativa de la nube compatible con MySQL y PostgreSQL. Guarda seis copias de los datos en tres AZ, escala el almacenamiento automáticamente y ofrece Aurora Serverless para cargas variables.

#### ¿Qué es Amazon ElastiCache?

Caché en memoria gestionada con Valkey, Redis OSS o Memcached, que se usa para reducir la carga de la base de datos y servir lecturas frecuentes con latencia de microsegundos.

#### ¿Qué es Amazon MemoryDB?

Una base de datos en memoria duradera, compatible con Valkey y Redis OSS, que puede usarse como base de datos principal gracias a su registro de transacciones Multi-AZ.

#### ¿Qué es Amazon Redshift?

Un almacén de datos en la nube gestionado, a escala de petabytes, para consultas analíticas SQL (OLAP), con almacenamiento en columnas, una opción serverless y la posibilidad de consultar datos en S3.

#### ¿Qué diferencia hay entre OLTP y OLAP y qué servicios de AWS encajan con cada uno?

OLTP gestiona muchas lecturas y escrituras transaccionales pequeñas (pedidos, pagos): RDS, Aurora, DynamoDB. OLAP ejecuta grandes consultas analíticas sobre datos históricos: Redshift, Athena.

#### ¿Qué es Amazon DocumentDB?

Una base de datos documental gestionada compatible con cargas de trabajo de MongoDB.

#### ¿Qué es Amazon Neptune?

Una base de datos de grafos gestionada para datos muy conectados, como redes sociales, detección de fraude y grafos de conocimiento.

#### ¿Qué es Amazon Keyspaces?

Una base de datos gestionada y serverless compatible con Apache Cassandra.

#### ¿Qué es Amazon Timestream?

Una base de datos de series temporales gestionada para IoT y métricas operativas.

#### ¿Qué es AWS Database Migration Service (DMS)?

Un servicio que migra bases de datos a AWS con un tiempo de inactividad mínimo, entre motores iguales (homogénea) o distintos (heterogénea, con la Schema Conversion Tool), y que puede replicar los cambios en curso.

#### ¿Qué es Amazon Athena?

Un servicio de consultas interactivas serverless para analizar datos en S3 con SQL estándar. Pagas por cantidad de datos escaneados, así que los formatos en columnas y el particionado reducen el costo.

#### ¿Qué es AWS Glue?

Un servicio serverless de integración de datos: rastreadores para descubrir esquemas, el Glue Data Catalog como almacén central de metadatos y trabajos ETL basados en Spark.

#### ¿Qué es Amazon EMR?

Una plataforma de big data gestionada para ejecutar Apache Spark, Hive, Presto/Trino, HBase y otros frameworks sobre EC2, EKS o en modo serverless.

#### ¿Qué es Amazon Kinesis?

Servicios para datos en streaming en tiempo real. Kinesis Data Streams captura y guarda flujos para procesarlos a medida. Amazon Data Firehose carga flujos en destinos como S3, Redshift u OpenSearch.

#### ¿Qué es Amazon QuickSight?

Un servicio de inteligencia de negocio serverless para crear cuadros de mando e informes interactivos, con análisis basados en aprendizaje automático y preguntas en lenguaje natural.

#### ¿Qué es Amazon OpenSearch Service?

Un servicio gestionado para clústeres de OpenSearch (y del antiguo Elasticsearch), usado para analizar registros, búsqueda de texto completo y observabilidad.

#### ¿Qué es AWS Lake Formation?

Un servicio para construir, proteger y gestionar un data lake en S3, con permisos detallados y centralizados sobre las tablas del Glue Data Catalog.

### Redes y entrega de contenidos

#### ¿Qué es Amazon VPC?

Virtual Private Cloud es una red virtual aislada lógicamente, dentro de una región, en la que lanzas recursos. Eliges su rango de IP y creas subredes, tablas de rutas y puertas de enlace.

#### ¿Qué diferencia hay entre una subred pública y una privada?

Una subred pública tiene una ruta hacia una puerta de enlace de internet, así que los recursos con IP pública son accesibles desde internet. Una subred privada no tiene esa ruta: sus recursos solo salen a internet, si acaso, a través de una puerta de enlace NAT.

#### ¿Qué es una puerta de enlace de internet?

Un componente de la VPC que permite la comunicación entre los recursos de la VPC e internet.

#### ¿Qué es una puerta de enlace NAT?

Un servicio gestionado que permite que las instancias de subredes privadas inicien conexiones salientes a internet (para actualizaciones, por ejemplo) mientras bloquea las conexiones entrantes no solicitadas.

#### ¿Qué diferencia hay entre un grupo de seguridad y una ACL de red?

Un grupo de seguridad actúa a nivel de instancia (interfaz de red), tiene estado y solo admite reglas de permiso. Una ACL de red actúa a nivel de subred, no tiene estado (el tráfico de respuesta debe permitirse explícitamente), admite reglas de permiso y de denegación, y evalúa las reglas por orden de número.

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

#### ¿Qué es un punto de enlace de VPC (VPC endpoint)?

Una conexión privada desde una VPC a servicios de AWS sin pasar por internet. Los puntos de enlace de puerta de enlace sirven S3 y DynamoDB. Los puntos de enlace de interfaz (AWS PrivateLink) sirven muchos otros servicios.

#### ¿Qué es AWS PrivateLink?

Una tecnología que expone servicios de forma privada entre VPC y cuentas mediante puntos de enlace de interfaz, manteniendo el tráfico dentro de la red de AWS.

#### ¿Qué son los VPC Flow Logs?

Registros del tráfico IP que entra y sale de las interfaces de red de una VPC, enviados a CloudWatch Logs o S3 para diagnosticar problemas y analizar la seguridad.

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

#### ¿Qué es un bloque CIDR?

Una notación para un rango de direcciones IP, como 10.0.0.0/16, que se usa para definir el espacio de direcciones de una VPC y sus subredes.

#### ¿Qué es un host bastión?

Una instancia en una subred pública que sirve de punto de entrada protegido para acceder por SSH o RDP a instancias de subredes privadas. Systems Manager Session Manager suele sustituirlo.

### Gestión, gobernanza y herramientas para desarrolladores

#### ¿Qué es Amazon CloudWatch?

Un servicio de monitorización y observabilidad: métricas, alarmas, registros (CloudWatch Logs), paneles y eventos, para recursos de AWS y aplicaciones.

#### ¿Qué es AWS CloudTrail?

Un servicio que registra las llamadas a la API y la actividad de la cuenta (quién hizo qué, cuándo y desde dónde) para la gobernanza, el cumplimiento y la auditoría. Los registros pueden enviarse a S3 y analizarse con CloudTrail Lake.

#### ¿Qué diferencia hay entre CloudWatch y CloudTrail?

CloudWatch supervisa el rendimiento y el estado (métricas, registros, alarmas). CloudTrail audita las acciones (llamadas a la API hechas en la cuenta).

#### ¿Qué es AWS Config?

Un servicio que registra la configuración de los recursos y sus cambios a lo largo del tiempo y la evalúa frente a reglas, para auditar el cumplimiento y diagnosticar problemas.

#### ¿Qué es AWS Systems Manager?

Un conjunto de herramientas operativas para gestionar servidores EC2 y locales a escala: Session Manager, Patch Manager, Run Command, Parameter Store, Automation e inventario.

#### ¿Qué es AWS CloudFormation?

Infraestructura como código: describes los recursos en plantillas JSON o YAML, y CloudFormation los crea, actualiza y elimina como una pila, en el orden correcto.

#### ¿Qué es el AWS Cloud Development Kit (CDK)?

Un framework para definir infraestructura en la nube con lenguajes de programación (TypeScript, Python, Java, C#, Go). Genera plantillas de CloudFormation.

#### ¿Qué es AWS Trusted Advisor?

Un servicio que inspecciona tu cuenta y recomienda mejoras en cinco categorías: optimización de costos, rendimiento, seguridad, tolerancia a fallos y cuotas de servicio. Los planes de soporte Basic y Developer solo tienen las comprobaciones principales. Business y superiores tienen el conjunto completo.

#### ¿Qué es el AWS Health Dashboard?

Una vista del estado de los servicios de AWS y de los eventos que afectan a tus propios recursos, como mantenimientos programados o incidencias en tus regiones.

#### ¿De qué formas se puede interactuar con AWS?

La AWS Management Console (web), la AWS CLI, los SDK para lenguajes de programación, la infraestructura como código (CloudFormation, CDK) y AWS CloudShell (un shell en el navegador ya autenticado).

#### ¿Qué son AWS CodeCommit, CodeBuild, CodeDeploy y CodePipeline?

Herramientas de CI/CD: CodeBuild compila y prueba el código, CodeDeploy automatiza los despliegues en EC2, Lambda, ECS y servidores locales, CodePipeline orquesta las canalizaciones de publicación. CodeCommit es un servicio de alojamiento Git cerrado a nuevos clientes.

#### ¿Qué es AWS X-Ray?

Un servicio que traza las solicitudes a través de aplicaciones distribuidas para encontrar cuellos de botella y errores.

#### ¿Qué es Amazon SQS?

Simple Queue Service es una cola de mensajes totalmente gestionada que desacopla componentes. Las colas estándar ofrecen un alto rendimiento con entrega al menos una vez. Las colas FIFO garantizan el orden y el procesamiento exactamente una vez.

#### ¿Qué diferencia hay entre SQS y SNS?

SQS es una cola: los consumidores sondean los mensajes y cada mensaje lo procesa un consumidor. SNS es publicación/suscripción: un mensaje publicado en un tema se envía a todos los suscriptores (SQS, Lambda, HTTP, correo, SMS). A menudo se combinan en un patrón de distribución (fan-out).

#### ¿Qué es Amazon EventBridge?

Un bus de eventos serverless que enruta eventos de servicios de AWS, aplicaciones SaaS y tu propio código hacia destinos según reglas, y programa tareas (EventBridge Scheduler).

### Facturación, precios y soporte

#### ¿Cuáles son los tres factores fundamentales del costo en AWS?

El cómputo, el almacenamiento y la transferencia de datos salientes. La transferencia de datos entrantes suele ser gratuita.

#### ¿Qué es la capa gratuita de AWS (Free Tier)?

Ofertas para probar AWS sin costo dentro de ciertos límites. Incluye ofertas siempre gratuitas (por ejemplo solicitudes de Lambda y almacenamiento de DynamoDB hasta un límite), créditos u ofertas de 12 meses para cuentas nuevas según el plan de la cuenta, y pruebas gratuitas cortas de servicios concretos. El uso que supera los límites se factura.

#### ¿Qué es la AWS Pricing Calculator?

Una herramienta gratuita para estimar el costo de una arquitectura antes de construirla.

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

#### ¿Cómo se pueden reducir los costos en AWS?

Ajustar el tamaño de las instancias, apagar los recursos que no se usan, usar Savings Plans o instancias reservadas para cargas estables y spot para las interrumpibles, elegir clases de almacenamiento más baratas con reglas de ciclo de vida, usar serverless para cargas variables, reducir la transferencia de datos (por ejemplo con CloudFront y puntos de enlace de VPC) y controlar el gasto con etiquetas, Budgets y Cost Explorer.
