## Sueños de Big Data

##### Publicado el {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Imagen creada por ChatGPT, OpenAI. 13 de Noviembre de 2024 ](../../images/big_data_dreams_little_data_realities_title_img.webp)

## Expectativa vs. Realidad

Este es un análisis subjetivo basado en mi experiencia personal. En mi vida profesional, he trabajado en varios departamentos de los llamados "Big Data" en varias empresas. Estas empresas a menudo tenían arquitecturas de datos elaboradas configuradas para manejar datos a gran escala. Cuando me gradué, el mensaje oficial era que los datos estaban creciendo exponencialmente. Se suponía que el Internet de las cosas (IdC) se estaba apoderando de la sociedad, inundándonos con datos que necesitaríamos administrar, analizar y transformar en información. Escuchamos que la mayoría de los datos producidos en todo el mundo aún estaban inexplorados, esperando ser analizados. Hablábamos de terabytes, tal vez incluso petabytes, de información. También se habló de la necesidad de procesamiento de datos en tiempo real, donde las empresas necesitaban paneles de control dinámicos y aplicaciones para reaccionar rápidamente a los problemas.

Para lidiar con estos supuestos diluvios de datos, las empresas invertían mucho en infraestructura de datos. En ese momento, la mayor parte del procesamiento de datos se realizaba en las instalaciones, por lo que Hadoop era el rey. Se utilizaban ampliamente herramientas como Apache Hive, Zeppelin y Zookeeper, y plataformas como Oracle R3. También estaban surgiendo contenedores y microservicios, y los lagos de datos estaban en todas partes. Pero a pesar de todo esto, la realidad en estas empresas era muy diferente de la imagen que vendían las conferencias tecnológicas y los libros blancos. Los datos con los que trabajábamos a menudo eran solo unos pocos gigabytes, a veces solo un puñado. Estos "big data" eran más bien "small data", muy lejos de los torrentes que habíamos imaginado.

Sospecho que esta era marcó una especie de experimentación impulsada por la curiosidad por parte de las empresas. Parecía que estaba de moda tener una infraestructura de big data, pero a menudo no se hacía una evaluación crítica de las necesidades reales de datos. Por eso, con frecuencia me encontré con empresas con arquitecturas robustas cuyos volúmenes de datos no justificaban la inversión. En muchos casos, las bases de datos relacionales clásicas y los scripts de procesamiento de datos sencillos habrían sido suficientes.


## Por qué la inundación de datos nunca llegó

Hay varias razones por las que la inundación de datos nunca llegó. Una es la política corporativa: los diferentes departamentos de la misma empresa suelen dudar (o directamente se niegan) a compartir los datos necesarios para los proyectos de big data. Otro factor es la regulación. Los datos confidenciales, como la información médica, deben protegerse, lo que dificulta su acceso o uso en muchos casos. Luego están los datos externos. Las empresas suelen confiar en proveedores externos para obtener algunos datos, pero estos datos no son gratuitos. Cada registro tiene un costo, por lo que las empresas pueden limitar la cantidad de datos que compran, y los proveedores a veces tienen dificultades técnicas o problemas con la calidad de los datos. Cuando hay contratos y relaciones profesionales involucrados, las cosas pueden complicarse.

Sin embargo, la razón más común es la elección de los casos de uso. Gran parte de mi trabajo se ha centrado en procesar datos de clientes para análisis de marketing. La cantidad de clientes, transacciones o productos puede ser sorprendentemente pequeña para ciertas empresas, especialmente cuando sus productos son caros. Piense en la frecuencia con la que compra electrodomésticos o abre una nueva cuenta bancaria. En casos como el monitoreo de infraestructura, donde el equipo genera señales cada pocos segundos, el volumen de datos es alto, pero para el análisis de pérdida de clientes, campañas de fidelización o detección de fraudes, los conjuntos de datos son en muchos casos relativamente pequeños: solo unos pocos gigabytes.
## Trabajar con "datos diminutos"

Dado este contexto, a menudo me encontré usando herramientas e infraestructura de big data para conjuntos de datos mucho más pequeños de lo previsto. Seguí las prácticas de big data, como crear canales de procesamiento para limpiar, formatear y consolidar datos, configurar herramientas de monitoreo y alertas, y usar programadores para ejecutar trabajos en momentos específicos. Ocasionalmente, necesitaba ingerir datos más antiguos en un nuevo conjunto de datos o incluso reconstruir conjuntos de datos para corregir errores históricos.

Una parte importante de mi trabajo implicaba leer registros para comprender por qué fallaban ciertos procesos. Los problemas de desbordamiento de memoria eran comunes, especialmente cuando la infraestructura era limitada, lo que causaba que los trabajos se bloquearan o se colgaran indefinidamente. La implementación en diferentes entornos (desarrollo, prueba y producción) también fue un desafío. A veces, los trabajos funcionaban en un entorno pero no en otro, y en los peores casos incluso se trataba de cambios de emergencia realizados directamente en la producción (no es lo ideal, pero sucede).

¿Lo más gracioso? Como la mayoría de los conjuntos de datos eran minúsculos, la optimización no solía ser una prioridad y las herramientas de big data a menudo parecían demasiado potentes para la tarea. Pero las complejidades del trabajo (corrección de datos, fallas en la cadena de producción, discrepancias en el entorno) seguían siendo similares a las de los conjuntos de datos verdaderamente grandes.

## FOMO y aspiraciones de Big Data

Algunas empresas realmente necesitan procesar datos masivos. Pensemos en Google, que desarrolló herramientas como MapReduce (predecesor de Apache Spark) y muchas más para manejar los datos colosales que maneja. Uber procesa datos de miles de viajes en tiempo real, mientras que Netflix ofrece transmisión sin interrupciones a millones de personas. Este es el sueño al que aspiran muchas empresas, que se imaginan que administran infraestructuras de big data como estos gigantes.

Pero la mayoría de las empresas están bien con actualizar los paneles de control una vez a la semana o al mes. Su negocio principal a menudo opera en el mundo físico, con clientes que no exigen respuestas inmediatas. Los datos en tiempo real no siempre son necesarios.

Entonces, sí, algunas situaciones realmente necesitan los mejores y más grandes cruceros para navegar los mares de datos. Pero en muchos casos, una pequeña balsa es todo lo que necesita para los estanques de datos en los que se encuentra. Y eso está bien, la clave es conocer su negocio y comprender la escala de los datos con los que está trabajando.



