## Preparación e Integración de Datos para Análisis Espacio-Temporal

### 1. Descripción de los Datos Originales

Se trabajó con cuatro fuentes principales de datos:

* **Temperatura Superficial del Mar (TSM):** Datos mensuales por estación de monitoreo para el periodo 1981–2018.
* **Clorofila a (Chl a):** Datos mensuales por estación para el periodo 1997–2018.
* **Coordenadas de estaciones:** Posiciones geográficas (latitud y longitud) de las 17 estaciones distribuidas en la zona costera occidental del Golfo de California.
* **Índice ONI (Oceanic Niño Index):** Serie temporal trimestral estandarizada que identifica episodios cálidos (El Niño), fríos (La Niña) y neutros, proporcionada por NOAA.

---

### 2. Transformación y Enriquecimiento de los Datos

#### 2.1 Estructura Longitudinal de TSM y Chl a

Para facilitar análisis multivariados y temporales, los datasets de TSM y Chl a se reestructuraron de formato ancho a formato largo. En esta estructura, cada fila representa una única observación por estación, mes y año. Se incluyeron variables auxiliares como:

* Año y mes de medición
* Estación del año (Primavera, Verano, Otoño, Invierno)
* Clasificación de evento interanual (Niño, Niña o Neutro, original del dataset)

#### 2.2 Unión de Variables Oceanográficas

Se realizó una unión por claves comunes entre TSM y Chl a, consolidando las observaciones por estación y fecha en un único dataframe (`data_long`).

#### 2.3 Asociación Geoespacial

Mediante un mapeo explícito de nombres, se incorporaron las coordenadas geográficas (latitud y longitud) a cada estación, asegurando la disponibilidad de variables espaciales para posteriores análisis geoespaciales y de clustering.

#### 2.4 Enriquecimiento con ENSO a Nivel Mensual

El índice ONI original se encontraba a nivel trimestral. Para convertirlo a un formato mensual, se definió una estrategia de expansión: cada trimestre se descompuso en los meses correspondientes, asignando el mismo valor de ONI.

Posteriormente, se clasificó cada valor mensual de ONI como:

* **Niño:** ONI ≥ 0.5
* **Niña:** ONI ≤ -0.5
* **Neutro:** -0.5 < ONI < 0.5

Esta clasificación fue incorporada como variable `ENSO_CLASE`.

---

### 3. Consolidación Final del Dataset

El dataframe final (`data_final`) resultó de unir la información enriquecida de TSM, Chl a, coordenadas y ENSO. Este dataset cuenta con la siguiente estructura para cada observación mensual por estación:

* **Variables temporales:** Año, mes (nombre y número), estación del año
* **Variables físicas:** TSM, Chl a
* **Variables espaciales:** Latitud, longitud, estación de medición
* **Información ENSO:** Valor ONI y su clasificación (Niño, Niña, Neutro)

Ejemplo de observaciones:

| FECHA      | AÑO  | MES     | ESTACIÓN DEL AÑO | estacion | TSM     | Chla   | lon    | lat  | MES\_NUM | ONI | ENSO\_CLASE |
| ---------- | ---- | ------- | ---------------- | -------- | ------- | ------ | ------ | ---- | -------- | --- | ----------- |
| 2018-10-01 | 2018 | Octubre | Otoño            | Est 1°   | 29.9133 | 0.1522 | -109.3 | 23.8 | 10       | 0.5 | Niño        |
| 2018-10-01 | 2018 | Octubre | Otoño            | Est 2°   | 29.7672 | 0.1781 | -109.7 | 24.2 | 10       | 0.5 | Niño        |
| ...        | ...  | ...     | ...              | ...      | ...     | ...    | ...    | ...  | ...      | ... | ...         |

---

### 4. Justificación Metodológica

Esta etapa fue esencial para cumplir los tres objetivos específicos del proyecto, ya que:

* Permite analizar la variabilidad temporal y espacial de TSM y Chl a, con integración completa de ENSO como variable explicativa.
* Habilita análisis de clustering geoespacial y temporal para regionalizar dinámicamente el Golfo de California.
* Establece una base robusta para explorar relaciones entre ENSO y cambios en la productividad marina.

---

Excelente material. Con base en todo lo que compartiste, aquí tienes una **redacción técnica organizada por objetivo específico**, que puedes usar en el documento final del proyecto. También incluyo sugerencias para nombrar los clusters de forma descriptiva.

---

# Parte 1. Regionalización Fija por Agrupamiento de Estaciones

Esta sección presenta un análisis exploratorio y de agrupamiento sobre las estaciones de monitoreo distribuidas a lo largo de la zona costera occidental del Golfo de California. El objetivo es proponer una **regionalización objetiva** basada en estadísticas resumen de Temperatura Superficial del Mar (TSM), Clorofila a (Chl a) y su relación promedio con el fenómeno ENSO.

## Preparación de los datos

Se calcularon estadísticas agregadas por estación considerando:

- Media, desviación estándar, mínimo y máximo de TSM y Chl a
- Promedio del índice ONI (como indicador promedio de influencia ENSO por estación)
- Coordenadas geográficas de cada estación

Estas variables fueron estandarizadas para aplicar técnicas de agrupamiento.

## Determinación del número óptimo de clusters

Se aplicó el **método del codo** sobre el valor de inercia (SSE) para distintas cantidades de clusters. El punto de inflexión sugiere que **4 clusters** representa una solución adecuada que equilibra simplicidad y diferenciación estadística.

![Método del codo para determinar número óptimo de clusters](metodo_codo.png)

## Resultados del agrupamiento

Utilizando K-Means con k=4 se asignó una etiqueta de cluster a cada estación. A continuación se visualiza la distribución geográfica de las estaciones agrupadas:

![Mapa con distribución espacial de clusters](mapa_clusters.png)

La regionalización resultante distingue claramente zonas con diferentes características ambientales:

| Cluster | TSM media (°C) | Chl a media (mg/m³) | Latitud media | Descripción general |
|--------:|----------------|----------------------|----------------|----------------------|
| 0       | 22.99          | 2.01                 | 29.6           | Alta productividad, baja TSM (norte) |
| 1       | 25.02          | 0.84                 | 25.8           | Zona cálida de baja productividad (centro-sur) |
| 2       | 23.55          | 1.38                 | 28.4           | Intermedia en TSM y productividad (centro-norte) |
| 3       | 25.98          | 0.48                 | 24.2           | Región cálida y oligotrófica (sur) |

## Variabilidad intra-cluster en función de ENSO

A continuación, se analiza cómo se comportan TSM y Chl a dentro de cada cluster bajo distintas fases del ENSO: Neutro, Niño y Niña.

### TSM por fase ENSO

Se observa que los valores de TSM tienden a incrementarse durante fases Niño en todos los clusters, siendo más notorio en los clusters cálidos (1 y 3).

![Boxplot de TSM por ENSO y Cluster](boxplot_tsm_enso.png)

### Chl a por fase ENSO

En cuanto a la Clorofila a, los valores más altos se presentan en el Cluster 0, mientras que los más bajos se concentran en el Cluster 3. La fase ENSO influye en la variabilidad, con ligeros aumentos durante eventos Niño.

![Boxplot de Chl a por ENSO y Cluster](boxplot_chla_enso.png)

## Estacionalidad de las variables por cluster

Se identificaron patrones estacionales bien diferenciados en cada agrupación:

- TSM muestra una marcada **estacionalidad térmica**, con máximos en verano y mínimos en invierno.
- Chl a presenta **picos de productividad en invierno y primavera** en los clusters del norte, lo cual es consistente con procesos de mezcla vertical y surgencia.

### TSM mensual promedio por cluster

![Estacionalidad de TSM por mes y cluster](tsm_mensual_cluster.png)

### Chl a mensual promedio por cluster

![Estacionalidad de Clorofila a por mes y cluster](chla_mensual_cluster.png)

## Tendencia interanual por cluster

Finalmente, se observó la evolución anual de TSM y Chl a dentro de cada cluster.

### TSM interanual promedio por cluster (1981–2018)

![Tendencia de TSM por año y cluster](tsm_interanual_cluster.png)

### Clorofila a interanual promedio por cluster (1997–2018)

![Tendencia de Chl a por año y cluster](chla_interanual_cluster.png)

Los clusters más cálidos (1 y 3) muestran una tendencia leve al aumento en TSM en las últimas décadas, mientras que los valores de Clorofila a permanecen relativamente estables con ligeras oscilaciones. El cluster norte (Cluster 0), caracterizado por alta productividad, muestra mayor variabilidad interanual.

---

## Contribución a los objetivos específicos

Este análisis contribuye directamente a:

✅ **Objetivo 1**: Al describir las principales estadísticas de TSM y Chl a por estación, e identificar patrones estacionales e interanuales.  
✅ **Objetivo 2**: Al establecer una primera propuesta de regionalización basada en características térmicas y biológicas agregadas.  
✅ **Objetivo 3**: Al mostrar cómo la fase ENSO influye en los valores promedio de TSM y Chl a por región.

---

# Parte 2. Clustering Dinámico Interanual (Estación × Año)

En esta sección se presenta un análisis de clustering dinámico, donde cada observación representa una estación en un año específico. Esto permite capturar variaciones temporales en las condiciones oceanográficas y establecer patrones interanuales de similitud entre estaciones.

## Preparación y características

Se calcularon los siguientes indicadores para cada par `(estación, año)`:

- TSM: media y desviación estándar anual
- Chl a: media y desviación estándar anual
- ONI: índice medio anual ENSO por observación
- Coordenadas geográficas (constantes por estación)

Se estandarizaron las variables y se aplicó el algoritmo K-Means con `k=4` para identificar patrones comunes a través del tiempo.

## Distribución y evolución de los clusters

La siguiente gráfica muestra la distribución de las estaciones en cada cluster a lo largo de los años:

![Distribución de clusters por año](clusters_por_anio.png)

Se observa que los clusters no son estáticos; hay años donde dominan ciertas condiciones (e.g., Cluster 3 en años recientes) y otros donde la distribución está más fragmentada.

En el siguiente **mapa de calor** se puede ver cómo cada estación cambia de cluster con el tiempo:

![Evolución de clusters por estación](evolucion_clusters_heatmap.png)

Algunas estaciones presentan mayor estabilidad en su clasificación, mientras que otras transitan entre múltiples agrupaciones.

## Estabilidad espacio-temporal

Para visualizar esta estabilidad, se construyó un mapa con el **número de cambios de cluster por estación**. A mayor número de cambios, menor estabilidad:

![Mapa de estabilidad por estación](mapa_estabilidad.png)

Las estaciones en rojo muestran **alta inestabilidad** (más de 10 cambios de cluster en el periodo), mientras que las estaciones en verde presentan **mayor consistencia temporal**.

## Relación con ENSO

Se analizó cómo se distribuyen los clusters en función de la **fase dominante del ENSO**:

![Conteo de clusters por fase ENSO](conteo_clusters_enso.png)

Aunque el cluster 1 está más representado en años Niña y el cluster 3 en años Niño, no se observa una dominancia clara que permita asociar directamente cada cluster con una fase ENSO, aunque hay indicios de relación que pueden explorarse en análisis complementarios.

## Comparación de TSM y Chl a por cluster

Los siguientes gráficos muestran la distribución de TSM y Chl a anuales por cluster dinámico:

![Boxplots de TSM y Chl a por cluster dinámico](boxplot_tsm_chla_dinamico.png)

- El **cluster 0** tiene la mayor concentración de clorofila a.
- El **cluster 3** presenta las **temperaturas más elevadas** y la **productividad más baja**.

Estas diferencias sugieren que los clusters reflejan bien las condiciones ambientales anuales.

## Permanencia de estaciones en un mismo cluster

Para evaluar la estabilidad interna de las estaciones, se calculó la duración promedio (en años consecutivos) que cada estación permaneció dentro de un mismo cluster:

![Duración promedio por estación](duracion_cluster_por_estacion.png)

Algunas estaciones (Est 11°, 14°) muestran alta estabilidad con permanencias de hasta 7 años en el mismo cluster, mientras que otras estaciones (Est 9°, 15°) cambian frecuentemente de agrupación.

## Matriz de transición entre clusters

La siguiente tabla resume las **transiciones de un cluster al siguiente** para años consecutivos:

| Cluster Actual | Hacia Cluster 0 | 1 | 2 | 3 |
|----------------|------------------|---|---|---|
| 0              | 18               | 0 | 16 | 1 |
| 1              | 2                | 38 | 8 | 26 |
| 2              | 17               | 11 | 88 | 3 |
| 3              | 0                | 29 | 5 | 78 |

Esto permite identificar la **estabilidad relativa** de cada cluster. Por ejemplo, el Cluster 2 presenta alta retención (88 transiciones consigo mismo), mientras que el Cluster 1 muestra mayor propensión a cambiar hacia otros estados (principalmente hacia 3).

---

## Contribución a los objetivos específicos

✅ **Objetivo 1**: Se capturan las principales frecuencias de variación anual en TSM y Chl a a través de agrupaciones dinámicas.  
✅ **Objetivo 2**: Se refuerza la regionalización desde un enfoque **temporalmente variable**, complementando la Parte 1.  
✅ **Objetivo 3**: Se evalúa la relación entre fases del ENSO y la distribución de clusters en distintas estaciones y años.

---
# Parte 3. Clustering Dinámico Estacional (Estación × Año × Estación del Año)

En esta etapa se aplicó un análisis de clustering con mayor granularidad temporal: cada observación representa una combinación de **estación de monitoreo fija**, **año** y **estación del año** (primavera, verano, otoño, invierno). El objetivo fue identificar agrupaciones de comportamiento ambiental recurrentes en escalas **intra-anuales**, capturando efectos estacionales y transitorios.

## Estructura de los datos y metodología

Las variables incluidas en el clustering fueron:

- TSM media y desviación estándar por estación del año
- Chl a media y desviación estándar por estación del año
- Índice ENSO (ONI) promedio por registro

Se aplicó escalado estándar y posteriormente K-Means con `k=4` para clasificar los perfiles estacionales. La asignación de clusters resultó en patrones diferenciados que se exploran a continuación.

## Caracterización de los clusters estacionales

| Cluster | TSM (°C) | Chl a (mg/m³) | ONI | Características |
|--------:|----------|----------------|------|-----------------|
| 0       | 24.0     | 2.41           | -0.30 | Intermedio-cálido con productividad alta |
| 1       | 28.4     | 0.66           | -0.03 | Cálido, oligotrófico (probablemente verano) |
| 2       | 20.7     | 1.51           | +0.73 | Frío y productivo (posiblemente invierno con Niño) |
| 3       | 20.2     | 1.37           | -0.73 | Frío, menor productividad (posible Niña) |

## Distribución por estación del año

La siguiente gráfica muestra cómo se distribuyen los clusters entre estaciones del año:

![Distribución de clusters por estación del año](d8671e5e-0a63-41b1-a1d6-80fd42045221.png)

El **cluster 1**, caracterizado por temperaturas más altas y baja concentración de clorofila, domina en **verano y otoño**, mientras que **invierno y primavera** presentan una mayor variedad de condiciones.

## Evolución estacional interanual

En este gráfico se observa cómo los clusters estacionales evolucionan a lo largo de los años:

![Evolución de clusters estacionales por año](fe0d9929-240f-4600-bb43-ae40fbc5ab77.png)

Si bien hay cierta persistencia en algunos patrones (e.g., el cluster 1), también se detectan años con mayor presencia de clusters fríos (2 y 3), lo cual puede estar relacionado con eventos ENSO u otros factores climáticos.

## Variabilidad espacio-temporal detallada

El siguiente **heatmap** muestra cómo cambian los clusters estacionales en cada estación fija, año y estación del año:

![Variabilidad por estación y temporada](d574f95f-589c-446e-933e-954bf9787a00.png)

Se identifican estaciones con comportamientos más variables (e.g., Est 10° a 17°) y otras más estables (Est 1° a 5°). Estos patrones refuerzan la importancia de considerar la dimensión estacional además del año.

## Estabilidad estacional por estación

Se calculó el número total de **cambios de cluster entre estaciones del año**, por estación fija. Esto permite visualizar qué estaciones presentan mayor variabilidad **intra-anual**.

![Mapa de inestabilidad estacional](89d0c7df-e5ad-49d0-9fca-9e94917108a3.png)

- Las estaciones con **inestabilidad muy alta** (rojo) muestran más de 60 cambios estacionales en el periodo.
- Las estaciones en verde muestran menor variación entre estaciones del año, a lo largo del tiempo.

## Matriz de transición entre estaciones del año

Se calculó la **frecuencia de transición** de un cluster a otro dentro del mismo año, entre estaciones consecutivas:

| Cluster Actual → Siguiente | 0   | 1   | 2   | 3   |
|----------------------------|-----|-----|-----|-----|
| 0                          | 48  | 74  | 23  | 29  |
| 1                          | 48  | 122 | 55  | 102 |
| 2                          | 44  | 181 | 6   | 6   |
| 3                          | 55  | 269 | 5   | 4   |

La mayoría de las transiciones ocurren hacia el **cluster 1**, indicando que muchas estaciones tienden a entrar en condiciones cálidas y menos productivas a lo largo del año. El **cluster 2** tiene muy baja retención, posiblemente reflejando condiciones más inestables o transitorias.

---

## Contribución a los objetivos específicos

✅ **Objetivo 1**: Se identifica variabilidad significativa intra-anual, revelando diferencias entre estaciones del año.  
✅ **Objetivo 2**: Se complementa la regionalización con un enfoque **dinámico estacional**, más sensible a la variación temporal.  
✅ **Objetivo 3**: Se asocian patrones estacionales con posibles fases del ENSO, reflejadas en los promedios del índice ONI por cluster.

---
# Parte 4. Clustering Dinámico Mensual (Estación × Año × Mes)

Este análisis representa el nivel más detallado del proyecto, con una resolución temporal mensual. Cada observación está compuesta por una estación fija, un año y un mes. El objetivo es detectar con mayor precisión las variaciones ambientales de alta frecuencia y los cambios que podrían estar asociados a fenómenos de corto plazo.

## Variables consideradas

- TSM mensual promedio
- Clorofila a mensual promedio
- ONI mensual (índice ENSO)

Se aplicó escalado estándar y se usó K-Means con `k=4` para clasificar perfiles mensuales en función de estas variables.

## Caracterización de clusters mensuales

| Cluster | TSM (°C) | Chl a (mg/m³) | ONI | Interpretación posible |
|--------:|----------|----------------|------|-------------------------|
| 0       | 28.91    | 0.64           | -0.15 | Muy cálido, baja productividad |
| 1       | 20.91    | 3.65           | -0.10 | Frío y altamente productivo |
| 2       | 20.24    | 1.39           | -0.84 | Frío con productividad media, asociado a Niña |
| 3       | 22.41    | 1.26           | +1.11 | Moderadamente cálido, posible influencia de Niño |

## Heatmap mensual de variabilidad espacio-temporal

La siguiente visualización muestra cómo varían los clusters mensuales en cada estación, año y mes:

![Heatmap mensual](d47e474b-5641-42f5-ab8b-29afe834b4a2.png)

Este nivel de resolución evidencia una alta dinámica mensual, especialmente en estaciones intermedias y sureñas.

## Distribución mensual de clusters

El siguiente gráfico muestra cómo se distribuyen los clusters a lo largo de los 12 meses del año:

![Distribución mensual por cluster](15cb3a45-2e65-4711-ac31-8c3afa59f085.png)

El **cluster 0** (cálido y poco productivo) domina en los meses de verano (julio-septiembre), mientras que el **cluster 1** (frío y productivo) predomina en los primeros meses del año.

## Evolución anual de clusters mensuales

Se agruparon los resultados por año para visualizar la evolución de los patrones mensuales agregados:

![Evolución anual de clusters mensuales](07b43088-9bb4-40e0-813b-011b0f0ff344.png)

Este análisis refleja eventos de cambio abrupto, como en 2015, y también una posible transición de regímenes en periodos multianuales.

## Estabilidad mensual por estación

Se cuantificaron los cambios de cluster de un mes a otro dentro de cada estación para evaluar inestabilidad:

| Estación | Cambios Mensuales Totales |
|----------|----------------------------|
| Est 12°  | 89                         |
| Est 13°  | 77                         |
| Est 16°  | 77                         |
| Est 17°  | 77                         |
| ...      | ...                        |
| Est 1°   | 36                         |

En el siguiente mapa se clasifica el grado de **inestabilidad mensual** por estación:

![Mapa de inestabilidad mensual](47caf905-eb06-48bd-848f-295fbc106669.png)

- Verde: estaciones con menor variabilidad mensual
- Rojo: estaciones con múltiples cambios mes a mes

## Matriz de transición entre clusters mensuales

Se estimó la frecuencia con la que las estaciones cambian de un cluster a otro de un mes al siguiente:

| Cluster Actual → Siguiente | 0    | 1   | 2   | 3   |
|----------------------------|------|-----|-----|-----|
| 0                          | 1533 | 43  | 176 | 115 |
| 1                          | 58   | 134 | 85  | 58  |
| 2                          | 182  | 97  | 714 | 12  |
| 3                          | 119  | 65  | 16  | 486 |

Se observa que el **cluster 0** tiene una gran retención (persistencia estacional), mientras que el cluster 1 presenta una mayor movilidad hacia otros estados.

---

## Contribución a los objetivos específicos

✅ **Objetivo 1**: Este análisis permite caracterizar variabilidad mensual con precisión, observando ciclos cortos.  
✅ **Objetivo 2**: Aporta una perspectiva alternativa de regionalización basada en perfiles dinámicos mensuales.  
✅ **Objetivo 3**: Se identifican patrones que coinciden con eventos ENSO (e.g., alta prevalencia del cluster 3 con Niño).

---
