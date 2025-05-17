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

# 1. Cluster Global por Estación (promedios fijos)

## Objetivo específico 1: Determinar la variabilidad de la TSM y Chl a y sus principales frecuencias de variación

### Resultados

* Se realizó una agregación mensual y anual de TSM y Chl a por estación.
* Las gráficas de estacionalidad muestran un **patrón claro anual de temperatura**, con máximos en agosto y mínimos en febrero, consistente con el ciclo solar.
* La **clorofila a** presenta una distribución estacional inversa: mayores concentraciones en invierno-primavera y una disminución marcada en verano.
* Las tendencias interanuales muestran una **ligera disminución en Chl a** (posible indicio de desnutrición del sistema), y una **tendencia al alza en TSM**, especialmente en estaciones agrupadas en el Cluster 3.

### Interpretación

* Las fluctuaciones estacionales en TSM reflejan el forzamiento térmico anual, mientras que los picos de clorofila a en primavera probablemente responden a procesos de surgencia y mezcla vertical.
* La disminución en la clorofila a puede estar relacionada con eventos de calentamiento sostenido y estratificación más prolongada.

---

## Objetivo específico 2: Establecer una regionalización mediante análisis de TSM y Chl a

### Metodología

* Se agruparon las estaciones usando **KMeans con K=4**, determinado mediante el método del codo.
* Las variables incluidas fueron: media y desviación estándar de TSM y Chl a, así como el promedio del índice ONI.
* Las estaciones se visualizaron en un mapa interactivo según su pertenencia a cada cluster.

### Resultados

A continuación se presentan las características medias por cluster:

| Cluster | TSM\_media | Chla\_media | Descripción propuesta                                     |
| ------- | ---------- | ----------- | --------------------------------------------------------- |
| 0       | \~23.0 °C  | \~2.0 mg/m³ | **Productivo Norte**: frío y muy productivo               |
| 1       | \~25.0 °C  | \~0.8 mg/m³ | **Centro cálido**: cálido con baja productividad          |
| 2       | \~23.5 °C  | \~1.4 mg/m³ | **Transicional**: zona intermedia                         |
| 3       | \~26.0 °C  | \~0.5 mg/m³ | **Sur cálido oligotrófico**: cálido y pobre en nutrientes |

### Interpretación

* El análisis permite establecer **cuatro regiones oceanográficas funcionales**, determinadas por condiciones térmicas y biológicas agregadas.
* Los clusters muestran un gradiente claro norte-sur: mayor productividad al norte, mayor temperatura al sur.

---

## Objetivo específico 3: Analizar el efecto interanual, intranual y estacional del ENSO

### Resultados

**Boxplots por cluster y fase ENSO:**

* Durante eventos **Niño**, la TSM tiende a aumentar ligeramente, con menor dispersión en los clusters cálidos (1 y 3).
* Durante **Niña**, la TSM desciende de forma visible, particularmente en el Cluster 0 (más frío).
* La clorofila a presenta **descensos marcados durante eventos Niño** en todos los clusters, especialmente en el Cluster 0, lo que sugiere inhibición de procesos de mezcla.

**Estacionalidad:**

* Todos los clusters siguen una misma dinámica estacional, pero con diferentes magnitudes:

  * Cluster 0 muestra **máximos de clorofila a** en primavera y **mínimos de TSM** en invierno.
  * Cluster 3 tiene **TSM constantemente altas** y clorofila baja todo el año.

**Tendencia interanual:**

* La TSM muestra una tendencia ascendente en todos los clusters, más marcada en el Cluster 3.
* La clorofila a muestra tendencia a la baja en los clusters 1 y 3.

---

## Sugerencias de nombres para los clusters

| Cluster | Nombre descriptivo          | Justificación                                      |
| ------- | --------------------------- | -------------------------------------------------- |
| 0       | **Norte productivo**        | TSM baja, Chla alta, al norte del golfo            |
| 1       | **Centro cálido**           | TSM media-alta, Chla baja, transición hacia el sur |
| 2       | **Franja intermedia**       | Térmicamente y biológicamente intermedio           |
| 3       | **Sur cálido oligotrófico** | Altas TSM, baja productividad, al sur del golfo    |


---

# 2. Cluster por Año (interanual dinámico)

## Objetivo específico 1: Determinar la variabilidad interanual de TSM y Chl a

### Resultados principales

* Se agruparon las estaciones **por año** y se aplicó KMeans (K=4) sobre estadísticas anuales de TSM, Chl a y ONI.
* Se identificaron **cuatro clusters dinámicos**, que agrupan condiciones ambientales similares:

| Cluster | TSM\_mean | Chla\_mean | ONI\_mean | Descripción funcional           |
| ------- | --------- | ---------- | --------- | ------------------------------- |
| 0       | 23.2 °C   | 2.37 mg/m³ | -0.06     | Frío y altamente productivo     |
| 1       | 24.8 °C   | 0.90 mg/m³ | -0.65     | Moderadamente cálido – La Niña  |
| 2       | 23.5 °C   | 1.57 mg/m³ | -0.07     | Intermedio (neutro)             |
| 3       | 25.9 °C   | 0.69 mg/m³ | +0.20     | Cálido y oligotrófico – El Niño |

### Visualizaciones clave

* **Boxplots de TSM y Chl a por cluster:** muestran una progresión clara entre condiciones frías-productivas (Cluster 0) y cálidas-oligotróficas (Cluster 3).
* **Gráfico de área de distribución anual de clusters:** revela cómo varía la composición ambiental del Golfo de año en año.

### Interpretación

* La variabilidad anual es significativa: hay años dominados por condiciones frías/productivas (2002, 2005) y otros por condiciones cálidas/pobres (1998, 2007, 2012).
* El clustering dinámico evidencia los **efectos interanuales de ENSO sobre la productividad y temperatura** en toda la región.

---

## Objetivo específico 2: Regionalización espacio-temporal dinámica

### Resultados

* Se elaboró una **matriz de evolución de cluster por estación** (heatmap), que muestra cómo cada estación cambia de cluster a lo largo de los años.
* Se cuantificó la **inestabilidad de cada estación** (número de cambios de cluster en 20 años):

| Estaciones más inestables | Cambios | Duración promedio en un cluster |
| ------------------------- | ------- | ------------------------------- |
| Est. 9°, Est. 15°         | 14–12   | \~1.5 años                      |
| Est. 11°, Est. 14°        | 2–3     | \~7.0 años                      |

* Se clasificaron las estaciones según **estabilidad**:

  * **Alta (rojo):** norte-centro del golfo
  * **Media (naranja):** franja media
  * **Baja (verde):** extremo sur

### Visualizaciones clave

* **Mapa de estabilidad de estaciones:** usando círculos codificados por color y tamaño según número de cambios.
* **Gráfica de barras de duración promedio por estación.**

### Interpretación

* La dinámica espacial del Golfo no es homogénea: hay estaciones persistentemente estables (Est. 11°) y otras muy volátiles (Est. 9°, Est. 15°), lo cual refleja diferencias en la sensibilidad local al clima.
* Esta regionalización **dinámica** complementa la visión estática del clustering espacial previo.

---

## Objetivo específico 3: Impacto del ENSO en la dinámica interanual

### Resultados

* Se clasificaron los años por su condición ENSO dominante (Niño, Neutro, Niña).
* Se observó lo siguiente:

| ENSO   | Cluster más común                |
| ------ | -------------------------------- |
| Niño   | Cluster 3 (cálido-oligotrófico)  |
| Niña   | Cluster 1 (moderado, baja Chla)  |
| Neutro | Clusters 2 y 0 (más productivos) |

* La **matriz de transición entre años consecutivos** muestra:

| De / A | C0 | C1 | C2 | C3 |
| ------ | -- | -- | -- | -- |
| C0     | 18 | 0  | 16 | 1  |
| C1     | 2  | 38 | 8  | 26 |
| C2     | 17 | 11 | 88 | 3  |
| C3     | 0  | 29 | 5  | 78 |

* El Cluster 2 es el más **estable** (88 repeticiones), seguido del 3 (78); los clusters más variables son el 0 y 1.

### Visualizaciones clave

* **Countplot ENSO vs Cluster dinámico:** destaca la relación Niño ↔ Cluster 3, y Niña ↔ Cluster 1.
* **Matriz de transiciones** entre clusters por año.
* **Mapa y gráfica de permanencias:** muestran patrones de estabilidad temporal por estación.

### Interpretación

* ENSO tiene un **efecto directo y observable** sobre la clasificación anual de las estaciones.
* Los cambios más comunes (ej. C1 → C3) podrían reflejar **transiciones entre fases ENSO**.
* La alta estabilidad de C2 sugiere que **los años neutros permiten mayor persistencia** de condiciones intermedias.

---

## Conclusión general del análisis dinámico

El clustering interanual permite capturar la **dimensión temporal de la variabilidad ambiental** del Golfo de California, ofreciendo una visión más rica que el clustering estático. Al incorporar la variación año a año, se identifican:

* Patrones de cambio vinculados a ENSO.
* Zonas del golfo más sensibles o estables.
* Trayectorias comunes entre condiciones ambientales.

Este enfoque es útil para generar **alertas tempranas, identificar zonas vulnerables o resilientes**, y apoyar la gestión pesquera y ambiental.

---
Perfecto, aquí tienes el análisis completo del **clustering mensual por estación y mes (dinámico)** siguiendo el mismo formato estructurado que los bloques anteriores:

---

# 3. Cluster por Mes (espacio-temporal dinámico mensual)

## Objetivo específico 1: Detectar la variabilidad mensual de TSM y Clorofila a

### Resultados principales

* Se agruparon las estaciones **por mes y año**, aplicando KMeans (K=4) sobre TSM media, Chl a media y ONI mensual.
* Se identificaron **cuatro clusters dinámicos mensuales**, reflejando distintos regímenes ambientales:

| Cluster | TSM\_mean | Chla\_mean | ONI\_mean | Descripción funcional                    |
| ------- | --------- | ---------- | --------- | ---------------------------------------- |
| 0       | 28.9 °C   | 0.64 mg/m³ | -0.15     | Muy cálido y oligotrófico (verano)       |
| 1       | 20.9 °C   | 3.65 mg/m³ | -0.10     | Frío y muy productivo (invierno extremo) |
| 2       | 20.2 °C   | 1.39 mg/m³ | -0.83     | Frío intermedio – fase Niña              |
| 3       | 22.4 °C   | 1.26 mg/m³ | +1.10     | Cálido-moderado – fase Niño              |

### Visualizaciones clave

* **Distribución por mes del año:** muestra transiciones estacionales claras: el Cluster 0 domina de julio a septiembre, el 1 en enero-marzo, el 3 en primavera.
* **Gráfico de área por año:** refleja la estacionalidad interanual del sistema.

### Interpretación

* El Golfo presenta una **estacionalidad ambiental clara**, con presencia alternante de condiciones frías-productivas y cálidas-oligotróficas.
* El Cluster 0 representa **condiciones veraniegas extremas**, mientras que el Cluster 1 refleja **invierno profundo con alta productividad**.

---

## Objetivo específico 2: Regionalización espacio-temporal detallada por mes

### Resultados

* Se generó un **heatmap mensual por estación**, evidenciando patrones únicos de variación intra-anual por sitio.
* Se cuantificó la **inestabilidad mensual** por estación (cambios de cluster entre meses consecutivos):

| Estaciones más inestables              | Cambios mensuales totales |
| -------------------------------------- | ------------------------- |
| Est. 12°, Est. 13°, Est. 16°, Est. 17° | 75–89                     |
| Est. 1°, Est. 2°, Est. 3°              | 35–45                     |

* Clasificación espacial:

  * **Alta inestabilidad (rojo):** norte-centro
  * **Media (naranja):** centro
  * **Baja (verde):** sur del Golfo

### Visualizaciones clave

* **Mapa de inestabilidad mensual:** codificado por color y tamaño de círculo.
* **Heatmap por estación y mes:** permite seguir la evolución clusterizada de cada estación a nivel mensual.

### Interpretación

* La escala mensual revela una **gran variabilidad ambiental incluso dentro del mismo año**.
* Algunas estaciones (ej. Est. 12°) experimentan frecuentes cambios de régimen, lo que podría implicar una **mayor sensibilidad ambiental** o transición de masas de agua.

---

## Objetivo específico 3: Evaluar la estabilidad y transiciones entre clusters

### Resultados

* Se calculó la **matriz de transición mensual**, es decir, la probabilidad de pasar de un cluster a otro en el siguiente mes:

| De / A | C0   | C1  | C2  | C3  |
| ------ | ---- | --- | --- | --- |
| C0     | 1533 | 43  | 176 | 115 |
| C1     | 58   | 134 | 85  | 58  |
| C2     | 182  | 97  | 714 | 12  |
| C3     | 119  | 65  | 16  | 486 |

* Los clusters más estables son:

  * **C0 (verano cálido):** 1533 repeticiones.
  * **C2 (frío tipo Niña):** 714 repeticiones.
* Las transiciones más comunes incluyen:

  * **C2 → C0 (frío a cálido):** 182 veces.
  * **C3 → C0 (primavera → verano):** 119 veces.

### Visualizaciones clave

* **Matriz de transición normalizada.**
* **Gráfico de evolución anual:** revela estacionalidad climática interanual.

### Interpretación

* La transición entre **clusters de invierno (C1/C2)** hacia **verano (C0)** es regular y esperable.
* La **estabilidad de C0 y C2** destaca patrones climáticos bien definidos en el Golfo de California.
* El **Cluster 3** (asociado a fase Niño) presenta menor permanencia.

---

## Conclusión general del análisis mensual

El clustering mensual ofrece una visión **fina y altamente detallada** de la dinámica ambiental del Golfo de California. A diferencia del análisis anual o estacional, este enfoque permite:

* Detectar **patrones intra-anuales** y eventos breves de transición.
* Identificar estaciones **con alta variabilidad mes a mes**.
* Evaluar cómo cambian los regímenes ambientales de **manera rápida y localizada**.

Este enfoque mensual es útil para:

* Estudios de **reclutamiento de especies**, productividad primaria, o detección de **anomalías climáticas rápidas**.
* Fortalecer la planificación **pesquera o de conservación** con base en condiciones de alta resolución.

---
