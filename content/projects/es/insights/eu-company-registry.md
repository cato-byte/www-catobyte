---
title: Lo que dicen 52 millones de filas de registros mercantiles sobre las empresas europeas
summary: Resultados en vivo del lakehouse de registros mercantiles. Dónde están las empresas, cuántas operan de verdad, dónde pesa la pesca, cuánto sobreviven las empresas nuevas y lo limpios que están los datos, a partir de seis registros nacionales.
data_url: /en/projects/eu-company-registry/data/
---

<div data-viz="kpis"></div>

Cada gráfico de esta página lee los pequeños ficheros JSON que publica la última tarea del pipeline tras cada ejecución mensual. Las cifras del texto se rellenan a partir de esos mismos ficheros, así que nada está escrito a mano. Del lakehouse solo salen agregados: ni datos de empresas fila a fila, ni nombres.

## Dónde están las empresas

El mapa sitúa <span data-stat="on_map">50,9 M</span> de empresas y establecimientos, el <span data-stat="on_map_share">97 %</span> de los vigentes. Cambia a la capa de pesca, filtra por sector o por registro y haz clic en un municipio para ver su desglose. Para que los ficheros sigan siendo ligeros, el pipeline publica los 5.000 municipios más grandes y todos los que tienen al menos una empresa pesquera.

<div data-viz="map"></div>

<div data-viz="industry_mix"></div>

Los registros no describen lo mismo. Francia y Navarra publican *establecimientos* (cada tienda, oficina o centro), los otros cuatro publican personas jurídicas. Francia además conserva sus establecimientos cerrados, por eso su tabla bronze es mucho mayor que su registro vivo. El fichero de datos básicos de Estonia no tiene ningún código de actividad, por eso no aparece en la estructura sectorial.

## Una empresa registrada no es una empresa en actividad

El hallazgo más útil es también el menos visible. Un registro mercantil indica dónde están *registradas* las empresas, y muchas lo están en una gestoría, un despacho de constitución de sociedades o una oficina virtual.

<div data-viz="activity"></div>

En el Reino Unido solo el <span data-stat="gb_operating">59 %</span> de las empresas activas parece operar donde está registrado: el <span data-stat="gb_mass">27 %</span> está en una dirección compartida por 50 empresas o más, el <span data-stat="gb_dormant">12 %</span> presenta cuentas de empresa inactiva y el <span data-stat="gb_strike_off">8 %</span> ya está en proceso de baja. Sin esta corrección, un mapa muestra sobre todo dónde están los despachos que constituyen sociedades.

<div data-viz="hotspots"></div>

La dirección con más sedes, <span data-stat="top_hotspot_address">71-75 Shelton Street, London</span>, alberga <span data-stat="top_hotspot_companies">76.065</span> empresas activas. La opción *Empresas en actividad* del mapa las descarta.

## Polos pesqueros

Las cifras brutas ponen primero a las grandes ciudades, porque tienen muchas empresas de todo tipo. El cociente de localización hace una pregunta mejor: ¿cuánto más frecuente es la pesca entre las empresas de un municipio que en el conjunto del país? Así aparecen los puertos: Shetland y Orcadas, las Hébridas, la costa noreste de Escocia (Fraserburgh, Buckie, Macduff) y, en Francia, la costa ostrícola y mejillonera de Charente-Maritime, la bahía del Mont-Saint-Michel y la laguna de Thau.

<div data-viz="fishing_hubs"></div>

<div data-viz="fishing_jobs"></div>

Navarra no tiene costa, así que sus únicas unidades pesqueras son unas pocas piscifactorías de trucha. Estonia no puede participar porque su fichero no tiene códigos de actividad.

## Altas, cierres y supervivencia

<div data-viz="demography"></div>

Los ficheros masivos del Reino Unido, Noruega y Estonia solo listan empresas vivas. Una empresa creada en 2005 y cerrada en 2010 simplemente ha desaparecido, así que los años antiguos parecen más pequeños de lo que fueron. El pipeline marca estas series con sesgo de supervivencia en lugar de esconder el problema.

Francia e Irlanda conservan las unidades cerradas con su fecha de cierre, así que la supervivencia se puede medir correctamente: para las empresas nacidas cada año, la proporción que sigue viva uno, tres, cinco y diez años después.

<div data-viz="survival"></div>

De los establecimientos franceses creados en <span data-stat="fr_survival_10y_cohort">2016</span>, el <span data-stat="fr_survival_10y">38 %</span> seguía abierto diez años después. En Irlanda la supervivencia a un año ronda el 100 % en todas las cohortes. Lo más probable es que eso hable más del registro que de las empresas: una empresa solo sale del registro al final de un procedimiento de baja o de liquidación, que dura meses.

<div data-viz="survival_sections"></div>

## Dificultades por sector

Cuatro registros publican si una empresa está en liquidación, en insolvencia o en proceso de baja. No usan el mismo vocabulario, así que silver primero los traduce a un conjunto común de estados.

<div data-viz="distress"></div>

## Empleos, no solo empresas

Un recuento de empresas trata igual a un autónomo y a una fábrica. Noruega publica plantillas exactas. Francia y Navarra publican tramos (*de 20 a 49 empleados*), así que el pipeline conserva los dos límites y los gráficos muestran el intervalo en lugar de inventarse un punto medio.

<div data-viz="employment"></div>

## ¿Qué tan limpios están los datos?

<div data-viz="funnel"></div>

<div data-viz="precision"></div>

El <span data-stat="fr_address_share">65 %</span> de los establecimientos franceses está situado en su dirección exacta, porque el INSEE publica coordenadas Lambert-93 y el pipeline las convierte a latitud y longitud con expresiones nativas de Spark. El resto se sitúa a nivel de código postal o de municipio con cruces sin conexión contra GeoNames, y un proceso en segundo plano mejora los más útiles a precisión de dirección, unos cientos cada vez, con geocodificadores públicos gratuitos.

<div data-viz="dq"></div>

Dos reglas destacan. La mayoría de las empresas irlandesas no tiene un código postal válido en el fichero de la CRO, así que Irlanda se sitúa a nivel de distrito (clave de encaminamiento del Eircode) o de municipio. En el Reino Unido, unos pocos miles de números de empresa no encajan en ninguno de los formatos conocidos del registro (ocho cifras, o dos letras y seis cifras). El pipeline no adivina: esas filas van a cuarentena con el registro completo y la regla incumplida, listas para revisarse y volver a procesarse.

<div data-viz="coverage"></div>

## Fuentes y licencias

INSEE SIRENE (Licence Ouverte 2.0), Companies House Basic Company Data (OGL v3), CRO Irlanda (CC BY 4.0), Brønnøysund Enhetsregisteret (NLOD 2.0), RIK Estonia (CC BY 4.0), Gobierno de Navarra (CC BY 4.0). Centroides de códigos postales y municipios: GeoNames (CC BY 4.0). Teselas del mapa: © colaboradores de OpenStreetMap.
