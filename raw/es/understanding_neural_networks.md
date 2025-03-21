## Entendiendo las redes neuronales

##### Publicado el {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Imagen creada por ChatGPT, OpenAI. 7 de octubre de 2024](../../images/understanding_neural_networks_title_img.webp)

¡Hola a todos! Hoy quiero repasar y dar una introducción básica a las redes neuronales para que podamos entender en términos muy generales la tecnología que hace que los modelos de IA funcionen. Tengo otra publicación sobre [PLN](../post/nlp_introduction.html) si quieres profundizar, creo que puede ser útil, al igual que otro conjunto de técnicas que permiten que herramientas como Gemini y ChatGPT comprendan lo que estás tratando de decir.

Puedes encontrar una buena introducción en este artículo del MIT [https://news.mit.edu/2017/explained-neural-networks-deep-learning-0414], del que saqué algunas ideas para escribir este artículo. También te recomiendo que leas mi otro artículo [a simple introduction to machine learning](../a_simple_introduction_to_machine_learning.html) para que puedas tener una base básica sobre el aprendizaje automático.


### 1. ¿Qué son las redes neuronales?

Una red neuronal es un modelo computacional inspirado en la estructura del cerebro humano, que consta de capas de neuronas artificiales conectadas por "pesos" que determinan la fuerza de las conexiones entre ellas. Estas redes pueden aprender de los datos y mejorar con el tiempo a través de un proceso llamado entrenamiento. En su forma más básica, una red neuronal tiene tres tipos de capas: la capa de entrada, que recibe datos sin procesar (como los valores de píxeles de una imagen o las palabras de una oración); las capas ocultas, que realizan el cálculo real y cuyo número y complejidad determinan la capacidad de la red para aprender características profundas y abstractas; y la capa de salida, que produce el resultado, como predecir una etiqueta (por ejemplo, "gato" o "perro" para un clasificador de imágenes o la siguiente palabra en una oración para un modelo de lenguaje).

### 2. Componentes básicos de una red neuronal

Para entender cómo funciona una red neuronal, debemos desglosar sus componentes fundamentales. En el corazón de la red se encuentran las neuronas (también llamadas nodos), que son las unidades computacionales básicas. Cada neurona recibe entradas, las procesa mediante la aplicación de pesos y produce una salida. La fuerza de las conexiones entre neuronas está determinada por los pesos, que controlan cuánta influencia tiene la salida de una neurona en la entrada de la siguiente neurona. A través del proceso de entrenamiento, los pesos aprenden la importancia de diferentes características. Otro elemento importante es el sesgo, que es una constante añadida a la suma ponderada de las entradas, lo que da a la red flexibilidad para modelar relaciones complejas. Finalmente, después de que se suman y ponderan las entradas, la neurona aplica una función de activación (como ReLU o Sigmoid) para decidir si debe "activarse" (emitir un valor significativo) o permanecer inactiva. Las funciones de activación introducen no linealidad en la red, lo que le permite resolver problemas complejos que los modelos lineales simples no pueden.


### 3. Entrenamiento, validación y reentrenamiento

El entrenamiento de una red neuronal implica introducir datos y ajustar sus pesos mediante un proceso denominado retropropagación. Durante el entrenamiento, se presenta a la red un gran conjunto de datos de pares de entrada y salida, como imágenes y sus etiquetas correspondientes. Para cada punto de datos, la red realiza una predicción y se calcula la diferencia entre el resultado previsto y el real (denominada pérdida). Para minimizar esta pérdida, la red utiliza retropropagación y descenso de gradiente. La retropropagación implica propagar la pérdida a través de la red para actualizar los pesos, mientras que el descenso de gradiente es un algoritmo de optimización que ajusta los pesos para minimizar la pérdida en la siguiente iteración. La validación es crucial durante el entrenamiento para supervisar el rendimiento de la red en un conjunto de datos independiente, lo que garantiza que no se sobreajuste y que pueda generalizarse bien a nuevos datos. Si el rendimiento de la red es deficiente, puede ser necesario volver a entrenarla. Esto puede implicar cambiar la estructura de la red, agregar más capas o aplicar técnicas de regularización para mejorar la generalización y evitar el sobreajuste.

### 4. Un ejemplo del mundo real

Ahora veamos un ejemplo simple del mundo real para fundamentar estos conceptos. Tratemos de predecir si un correo electrónico es spam o no. En este ejemplo, queremos que nuestra red neuronal clasifique los correos electrónicos como spam o no. Cada correo electrónico se representa como un vector de características, donde cada característica podría indicar: la presencia de palabras específicas, la frecuencia de ciertos signos de puntuación, la presencia de ciertas palabras clave asociadas con el spam (como "gratis", "comprar ahora", etc.). El proceso de transformar características como palabras, signos de puntuación u otros datos no numéricos en valores numéricos para el aprendizaje automático se denomina comúnmente extracción de características o ingeniería de características. Específicamente, cuando se trabaja con datos de texto, este proceso a menudo se conoce como vectorización o vectorización de texto.

Revisemos este proceso más en detalle:

Primero, el preprocesamiento del texto implica limpiar los datos sin procesar. Este paso incluye la eliminación de elementos innecesarios como palabras vacías (como "el", "es", "en"), caracteres especiales o números (a menos que sean esenciales). Después de limpiar el texto, a menudo se convierte a minúsculas para garantizar la uniformidad, de modo que palabras como "Spam" y "spam" se traten de la misma manera. Por ejemplo, la oración "¡¡¡Dinero gratis!!! ¡Haga clic ahora para reclamar su recompensa!!!" se convierte en "dinero gratis, haga clic ahora para reclamar su recompensa".

El proceso de transformar características como palabras, signos de puntuación u otros datos no numéricos en valores numéricos para el aprendizaje automático se denomina extracción de características o ingeniería de características. Específicamente, cuando se trabaja con datos de texto, esta transformación a menudo se conoce como vectorización o vectorización de texto. Esto es esencial para los modelos de aprendizaje automático, ya que requieren entradas numéricas para hacer predicciones o clasificaciones.

Repasemos los pasos de la extracción de características y la vectorización en el contexto de una tarea de clasificación de spam, donde el objetivo es clasificar si un correo electrónico es spam o no en función de la presencia de ciertas palabras, signos de puntuación y otras características relevantes.

Primero, el preprocesamiento del texto implica limpiar los datos sin procesar. Este paso incluye la eliminación de elementos innecesarios, como palabras vacías (como "the", "is", "in"), caracteres especiales o números (a menos que sean esenciales). Después de limpiar el texto, a menudo se convierte a minúsculas para garantizar la uniformidad, por lo que palabras como "Spam" y "spam" se tratan de la misma manera. Por ejemplo, la oración "¡¡¡Dinero gratis!!! ¡Haga clic ahora para reclamar su recompensa!!!" se convierte en "dinero gratis, haga clic ahora para reclamar su recompensa".

A continuación, extraemos características del texto limpiado. Las características comunes incluyen frecuencias de palabras, frecuencias de puntuación, la presencia de palabras específicas (como "gratis" o "ganar" que están asociadas con el spam) y la longitud del mensaje. Estas características pueden proporcionar información útil para distinguir entre correos electrónicos spam y no spam.

Una vez que se identifican las características, el siguiente paso es la vectorización, donde los datos textuales se convierten a un formato numérico que un modelo de aprendizaje automático puede procesar. Un método común es Bag of Words (BoW), donde se crea un vocabulario de todas las palabras únicas en el conjunto de datos de entrenamiento. Para cada documento (correo electrónico), se crea un vector basado en la frecuencia de cada palabra de este vocabulario. Por ejemplo, si el vocabulario consta de palabras como "gratis", "dinero", "reclamar" y "recompensa", cada correo electrónico estará representado por un vector que cuenta cuántas veces aparece cada palabra en ese correo electrónico.

Ejemplo:
Para las oraciones:

Correo electrónico 1: "Dinero gratis, ¡reclama tu recompensa ahora!"
Correo electrónico 2: "¡Compra ahora, oferta especial en productos!"
Vocabulario: ["gratis", "dinero", "reclamar", "tuyo", "recompensa", "ahora", "comprar", "especial", "oferta", "en", "productos"]

Vector de correo electrónico 1: [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
Vector de correo electrónico 2: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

Cada valor del vector representa la frecuencia de la palabra correspondiente en el correo electrónico.

Otra técnica de vectorización es la frecuencia de término-frecuencia de documento inversa (TF-IDF), que ajusta las frecuencias de las palabras teniendo en cuenta la frecuencia o rareza de una palabra en todos los documentos. Este método ayuda a enfatizar las palabras que aparecen con frecuencia en un documento en particular pero que son raras en todo el conjunto de datos, lo que las hace más útiles para las tareas de clasificación.

En algunos casos, se utiliza la codificación One-Hot, especialmente para las características categóricas. Por ejemplo, si está comprobando la presencia de determinadas palabras o signos de puntuación, puede asignar un valor binario (1 para presencia, 0 para ausencia). Por ejemplo, si está comprobando las palabras "dinero" y "gratis", un correo electrónico que contenga ambas palabras podría estar representado por el vector \[1, 1\], mientras que un correo electrónico que no contenga ninguna de ellas se representaría como \[0, 0\].

Finalmente, después de aplicar la vectorización, todas las características se combinan en un vector de características final. Este vector, que incluye frecuencias de palabras, recuentos de puntuación y otras características, sirve como entrada para un algoritmo de aprendizaje automático. Por ejemplo, el vector de características de un correo electrónico podría verse así: \[3 (gratis), 1 (dinero), 0 (oferta), 2 (signos de exclamación), 5 (longitud)\

En resumen, la transformación de datos no numéricos, como palabras y signos de puntuación, en valores numéricos se denomina vectorización o extracción de características. Al aplicar métodos como Bag of Words, TF-IDF y One-Hot Encoding, podemos convertir datos de texto en un formato adecuado para los modelos de aprendizaje automático. Estos métodos ayudan a capturar los patrones y características esenciales de los datos que son importantes para tareas como la clasificación de correo no deseado.

A continuación, definimos la arquitectura de nuestra red neuronal. En este ejemplo, la capa de entrada contendrá una neurona por cada característica extraída del correo electrónico (por ejemplo, frecuencias de palabras o recuentos de caracteres). Las neuronas de entrada se conectan a una capa oculta, donde especificamos la cantidad de neuronas en función de la complejidad del problema (por ejemplo, 64 neuronas en una capa oculta). Estas neuronas aplican una función de activación como ReLU para agregar no linealidad, lo que permite que la red aprenda relaciones complejas entre las características. La capa de salida final tiene dos neuronas, una para cada clase: "spam" y "no spam", que generan probabilidades para cada clase. El uso de la función de activación softmax garantiza que los resultados sean probabilidades que sumen 1, lo que indica la probabilidad de que un correo electrónico pertenezca a cada clase.

Durante el entrenamiento, cada correo electrónico pasa por la red en un proceso llamado propagación hacia adelante. La red calcula una suma ponderada de las entradas en cada neurona, aplica funciones de activación y genera una predicción (probabilidad de ser spam o no). Luego, utilizamos una función de pérdida, como la entropía cruzada categórica, para medir la diferencia entre la predicción de la red y la etiqueta verdadera del correo electrónico.

Para mejorar la precisión, aplicamos la retropropagación para ajustar los pesos en función de la pérdida. En la retropropagación, la pérdida se propaga hacia atrás a través de la red, calculando cuánto contribuyó cada peso al error. Mediante un algoritmo de optimización como el descenso de gradiente, los pesos se ajustan para minimizar el error. Este proceso se repite en varias épocas, donde cada época representa un paso a través de todo el conjunto de datos de entrenamiento.

Durante el entrenamiento, validamos periódicamente el rendimiento del modelo en un conjunto de datos de validación para detectar el sobreajuste. Si el modelo funciona bien con los datos de entrenamiento pero mal con los datos de validación, es posible que debamos ajustar los hiperparámetros (por ejemplo, la tasa de aprendizaje, la cantidad de capas) o introducir técnicas de regularización para ayudar a generalizar a nuevos correos electrónicos.

Por último, una vez que se completa el entrenamiento y el modelo funciona bien con el conjunto de datos de validación, lo probamos con el conjunto de datos de prueba para confirmar que puede clasificar con precisión los correos electrónicos no vistos. Al seguir este flujo de trabajo, la red neuronal aprende de los ejemplos etiquetados, perfecciona su comprensión de lo que distingue al correo no deseado de los correos electrónicos legítimos y se convierte en un clasificador confiable para detectar el correo no deseado en aplicaciones del mundo real.


### 5. ¿Cuántos datos necesita una red neuronal?

La cantidad de datos depende de la complejidad del problema. Las tareas sencillas, como reconocer números escritos a mano, pueden requerir menos datos, mientras que las tareas más complejas, como la clasificación de imágenes o el procesamiento del lenguaje natural, necesitan grandes cantidades de datos para generalizar bien y evitar el sobreajuste.

### 6. ¿Qué son los pesos y cómo se determinan?

Los pesos representan la fuerza de las conexiones entre neuronas, inicialmente se establecen de forma aleatoria pero se afinan durante el entrenamiento. A medida que la red aprende, los pesos se ajustan para reducir el valor de la función de pérdida. A través de este proceso de optimización, la red se vuelve más precisa, mejorando sus capacidades predictivas.

### 7. Cómo las redes neuronales procesan imágenes y texto

Si bien los conceptos básicos de las redes neuronales (pesos, neuronas, funciones de activación) son los mismos, la estructura y el diseño de las redes para imágenes y texto pueden diferir significativamente:

Redes neuronales para procesamiento de imágenes: estas redes suelen ser redes neuronales convolucionales (CNN), que están diseñadas para procesar datos en forma de cuadrícula, como píxeles en una imagen. Las CNN utilizan capas especializadas llamadas capas convolucionales que aplican filtros a la imagen y capturan características como bordes, texturas y patrones en diferentes niveles. Este enfoque jerárquico ayuda a las CNN a aprender a reconocer objetos complejos a partir de patrones simples.

Redes neuronales para procesamiento de texto: las redes neuronales basadas en texto suelen utilizar redes neuronales recurrentes (RNN) o transformadores. Las RNN están diseñadas para manejar datos secuenciales (como palabras en una oración) y mantener un estado interno que las ayuda a "recordar" entradas anteriores. Esto es crucial para comprender el contexto del lenguaje. Los modelos modernos como Transformers (utilizados en modelos como GPT-4) se basan en mecanismos de atención para comprender las relaciones entre las palabras sin necesidad de procesarlas secuencialmente, lo que permite una comprensión del lenguaje más eficiente y escalable.


### 8. Similitudes entre las redes de imágenes y texto

A pesar de estas diferencias, las redes neuronales para imágenes y texto comparten varias similitudes:

Arquitectura en capas: tanto las redes de imágenes como las de texto utilizan múltiples capas (de entrada, ocultas y de salida) para extraer características y hacer predicciones.

Pesos y retropropagación: el proceso de ajuste de pesos mediante retropropagación y descenso de gradiente se aplica a ambos tipos de redes.

Funciones de activación: las funciones de activación no lineales (como ReLU) se utilizan en ambos tipos de redes para introducir no linealidad, lo que permite que el modelo capture relaciones complejas.

### 9. Diferencias clave

Estructura de datos: las imágenes son 2D (o 3D con canales de color), por lo que se utilizan capas convolucionales y agrupamiento para procesar relaciones espaciales. El texto, por otro lado, es secuencial, por lo que las redes necesitan mecanismos para capturar el orden de las palabras y sus dependencias.

Preprocesamiento: los datos de imagen a menudo necesitan ser redimensionados, normalizados o ampliados (por ejemplo, rotados o volteados) para ayudar a la red a generalizar. Los datos de texto requieren tokenización (dividir oraciones en palabras o caracteres) y pueden implicar la incrustación de las palabras en vectores continuos.

### Conclusión

Las redes neuronales son herramientas poderosas que permiten a la IA abordar problemas complejos en campos como la visión artificial y el procesamiento del lenguaje natural. En el núcleo de estas redes hay componentes simples (neuronas, pesos y funciones de activación), pero su verdadera fortaleza radica en su capacidad de aprender y adaptarse a través de procesos como el entrenamiento, la retropropagación y la validación. Ya sea que procesen imágenes o texto, las redes neuronales comparten los mismos principios fundamentales, pero adaptan sus arquitecturas a la naturaleza específica de los datos que manejan, lo que las hace versátiles y efectivas en una amplia gama de aplicaciones.