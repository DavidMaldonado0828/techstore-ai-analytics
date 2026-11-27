# TECHSTORE — GLOSSARY

**Documento:** `glossary.md`  
**Proyecto:** TechStore  
**Tipo:** Diccionario de datos y glosario de negocio  
**Base de datos:** techstore  
**Schema:** public  
**Motor:** PostgreSQL  
**Proveedor:** Neon  
**Modelo:** Gold — Data Warehouse  
**Última actualización:** 2026-11-27

---

# 1. PROPÓSITO

Este documento define los términos técnicos, comerciales y analíticos utilizados en TechStore.

Su propósito es establecer un lenguaje común entre:

- Usuarios de negocio.
- Analistas.
- Desarrolladores.
- Ingenieros de datos.
- Sistemas de inteligencia artificial.
- Aplicaciones de análisis de información.

El agente de IA debe utilizar este documento para interpretar correctamente las preguntas de los usuarios.

No debe depender exclusivamente de los nombres de las columnas.

Debe comprender el significado de los conceptos y su relación con las tablas de la base de datos.

---

# 2. CONCEPTOS GENERALES

## TechStore

Proyecto de análisis de información comercial basado en una arquitectura Lakehouse y un modelo dimensional Gold.

La información analítica se encuentra actualmente migrada a PostgreSQL mediante Neon.

## Data Warehouse

Sistema de almacenamiento orientado al análisis de información histórica y comercial.

A diferencia de una base de datos transaccional, su estructura está preparada para consultas analíticas, agregaciones y toma de decisiones.

## Data Lakehouse

Arquitectura que combina características de Data Lake y Data Warehouse.

TechStore utilizó esta arquitectura en AWS antes de migrar sus tablas Gold a Neon.

## Bronze

Capa inicial del procesamiento de datos.

Contiene información de origen con transformaciones limitadas.

En el proyecto original, esta capa utilizaba tablas `raw_*`.

No forma parte de las ocho tablas disponibles actualmente en Neon.

## Silver

Capa de datos procesados y estandarizados.

En TechStore, se utilizó para limpiar, validar y transformar la información Bronze.

No forma parte de las ocho tablas disponibles actualmente en Neon.

## Gold

Capa analítica final del Lakehouse.

Contiene las dimensiones y tablas de hechos preparadas para consultas analíticas.

Las ocho tablas Gold de TechStore fueron migradas a Neon.

## ETL

Proceso de:

- Extract: extracción.
- Transform: transformación.
- Load: carga.

Permite extraer datos de las fuentes, aplicar reglas de procesamiento y cargarlos en una capa de destino.

## ELT

Proceso de:

- Extract.
- Load.
- Transform.

La transformación ocurre después de cargar la información en el sistema de destino.

No debe confundirse automáticamente con el ETL utilizado en los procesos originales de TechStore.

## Neon

Proveedor de PostgreSQL utilizado para alojar la base de datos analítica de TechStore.

## PostgreSQL

Sistema de gestión de bases de datos relacional utilizado como motor de la base de datos Neon.

## Schema

Espacio lógico dentro de PostgreSQL que organiza tablas y otros objetos.

El schema principal de TechStore es `public`.

## Branch

Rama o entorno de desarrollo de Neon.

La rama de producción documentada es `production`.

---

# 3. CONCEPTOS DEL MODELO DIMENSIONAL

## Modelo dimensional

Diseño de base de datos que organiza la información en dimensiones y hechos.

Permite realizar análisis desde diferentes perspectivas.

## Dimensión

Tabla que contiene información descriptiva sobre una entidad.

Ejemplos:

- Cliente.
- Producto.
- Sucursal.
- Fecha.
- Método de pago.

## Tabla de hechos

Tabla que registra eventos u operaciones que pueden analizarse mediante métricas.

Ejemplos:

- Ventas.
- Devoluciones.
- Garantías.

## Hecho

Evento comercial o registro cuantificable dentro del modelo analítico.

## Granularidad

Nivel de detalle que representa cada fila de una tabla.

Es uno de los conceptos más importantes del modelo.

En `fact_sales`, una fila representa una línea de detalle de venta.

## Clave primaria (PK)

Columna o conjunto de columnas que identifica de forma única cada registro de una tabla.

## Clave foránea (FK)

Columna o conjunto de columnas que establece una referencia a otra tabla.

## Clave sustituta (Surrogate Key)

Identificador generado para representar una entidad dentro del modelo dimensional.

En TechStore se utilizan claves como:

- `customer_sk`
- `product_sk`
- `branch_sk`
- `payment_method_sk`
- `date_sk`

## Clave natural

Identificador proveniente del sistema de origen que representa una entidad de negocio.

Ejemplos:

- `customer_id`
- `product_id`
- `branch_id`

## Unknown Member

Registro especial de una dimensión utilizado para representar información desconocida.

En TechStore se utiliza el identificador `-1`.

## Desnormalización

Técnica que consiste en incorporar información relacionada dentro de una misma estructura para facilitar consultas.

En TechStore, la dimensión de productos incorpora información de marcas.

---

# 4. TABLAS DEL PROYECTO

## dim_branch

Dimensión que representa las sucursales comerciales de TechStore.

Permite analizar las operaciones por ubicación geográfica.

Conceptos relacionados:

- Sucursal.
- Ciudad.
- Departamento.
- Dirección.
- Fecha de apertura.
- Estado de sucursal.

## dim_customer

Dimensión que representa los clientes de TechStore.

Permite analizar el comportamiento comercial de los compradores.

Conceptos relacionados:

- Cliente registrado.
- Cliente comprador.
- Identificador de cliente.
- Comportamiento de compra.

## dim_date

Dimensión temporal.

Permite analizar operaciones por períodos de tiempo.

Conceptos relacionados:

- Fecha.
- Día.
- Mes.
- Año.
- Trimestre.
- Semana.
- Período.

La clave temporal utiliza el formato `YYYYMMDD`.

## dim_payment_method

Dimensión que representa los métodos de pago utilizados en las operaciones comerciales.

Permite analizar la distribución de las ventas según el método de pago.

## dim_product

Dimensión que representa los productos comercializados por TechStore.

Incluye información de marcas para facilitar el análisis comercial.

Conceptos relacionados:

- Producto.
- Marca.
- Categoría, si está disponible.
- Precio, si está disponible.
- Identificador de producto.

## fact_sales

Tabla de hechos que registra las líneas de detalle de las ventas.

Granularidad:

Una fila representa una línea de detalle de una venta.

Conceptos relacionados:

- Venta.
- Línea de venta.
- Cantidad.
- Precio unitario.
- Descuento.
- Subtotal.
- Estado de venta.

## fact_returns

Tabla de hechos que contiene los registros relacionados con las devoluciones.

Permite analizar el comportamiento de las devoluciones.

La granularidad exacta debe verificarse en el esquema y ETL.

## fact_warranties

Tabla de hechos que contiene los registros relacionados con las garantías.

Permite analizar la actividad de garantías.

La granularidad exacta debe verificarse en el esquema y ETL.

---

# 5. CONCEPTOS COMERCIALES

## Venta

Operación comercial mediante la cual se realiza la comercialización de uno o varios productos.

En TechStore se identifica mediante `sale_id`.

## Línea de venta

Registro individual que representa un producto dentro de una venta.

En TechStore se identifica mediante `sale_detail_id`.

Una venta puede contener varias líneas de detalle.

## Producto vendido

Producto que aparece en una o más líneas de `fact_sales`.

## Cliente registrado

Cliente existente en `dim_customer`.

## Cliente comprador

Cliente que tiene al menos una operación comercial registrada en `fact_sales`.

## Sucursal

Establecimiento físico donde se realizan operaciones comerciales.

## Marca

Identidad comercial asociada a uno o varios productos.

En el modelo de TechStore, la información de marcas se encuentra incorporada en `dim_product`.

## Método de pago

Medio utilizado para realizar el pago de una operación comercial.

## Devolución

Evento relacionado con la devolución de un producto o parte de una operación comercial.

## Garantía

Registro relacionado con la cobertura o atención de un producto vendido.

Una garantía registrada no implica necesariamente que el producto tenga un defecto.

---

# 6. CONCEPTOS DE MÉTRICAS

## Métrica

Valor cuantitativo utilizado para medir un aspecto del negocio.

## KPI

Indicador clave de rendimiento.

Permite evaluar el desempeño de una actividad o proceso comercial.

## Ventas totales

Expresión ambigua que puede referirse a diferentes indicadores.

El agente debe determinar si el usuario solicita:

- Número de operaciones comerciales.
- Número de líneas de venta.
- Unidades vendidas.
- Importe comercial registrado.

No debe interpretar automáticamente "ventas totales" como una suma monetaria.

## Número de ventas

Cantidad de operaciones comerciales distintas.

Referencia conceptual:

`COUNT(DISTINCT sale_id)`.

## Número de líneas de venta

Cantidad de registros de detalle de venta.

Referencia:

`COUNT(*)` en `fact_sales`.

## Unidades vendidas

Suma de las cantidades de productos registradas en las líneas de venta.

Referencia:

`SUM(quantity)`.

## Precio unitario

Precio correspondiente a una unidad de producto.

Columna observada:

`unit_price`.

## Descuento

Importe descontado de una línea de venta.

Columna observada:

`line_discount_amount`.

## Subtotal de línea

Importe subtotal correspondiente a una línea de venta.

Columna observada:

`line_subtotal_amount`.

La interpretación exacta del subtotal debe respetar la lógica de transformación del proyecto.

## Importe comercial registrado

Suma de los subtotales de las líneas de venta.

Referencia conceptual:

`SUM(line_subtotal_amount)`.

No equivale automáticamente a utilidad.

## Ingreso bruto

Concepto financiero cuyo cálculo depende de la definición contable utilizada.

No debe utilizarse como sinónimo automático de `SUM(line_subtotal_amount)` sin validar la definición.

## Ingreso neto

Concepto financiero que depende de las reglas de reconocimiento de ingresos, descuentos y devoluciones.

No debe calcularse sin una definición explícita.

## Utilidad

Diferencia entre ingresos y costos según una definición contable determinada.

TechStore no debe presentar utilidad calculada únicamente con información de precios de venta.

## Rentabilidad

Indicador que relaciona beneficios con costos, inversiones o ingresos.

Requiere información suficiente para su cálculo.

## Ticket promedio

Importe comercial promedio por operación de venta.

Una definición posible es:

`SUM(line_subtotal_amount) / COUNT(DISTINCT sale_id)`.

Debe utilizar filtros coherentes.

## Promedio de unidades por venta

Cantidad promedio de unidades vendidas por operación comercial.

Definición posible:

`SUM(quantity) / COUNT(DISTINCT sale_id)`.

## Precio promedio ponderado

Importe comercial promedio por unidad vendida.

Definición posible:

`SUM(line_subtotal_amount) / SUM(quantity)`.

## Participación porcentual

Porcentaje que representa una categoría frente a un total.

Ejemplo:

Participación de una sucursal sobre el importe comercial total.

## Ranking

Clasificación de elementos según una métrica.

Ejemplos:

- Productos más vendidos.
- Clientes con mayores compras.
- Sucursales con mayor importe comercial.

El ranking debe indicar qué métrica utiliza.

---

# 7. CONCEPTOS TEMPORALES

## Fecha de venta

Fecha en que se registró la operación comercial.

En `fact_sales` existe `sale_timestamp`.

## Fecha de evento

Fecha correspondiente a un evento específico, como una devolución o garantía.

No debe confundirse con la fecha de venta.

## Período

Intervalo de tiempo utilizado para analizar datos.

Ejemplos:

- Día.
- Semana.
- Mes.
- Trimestre.
- Año.

## Año

Período de doce meses utilizado para agrupar operaciones.

## Mes

Unidad temporal utilizada para agrupar operaciones comerciales.

## Trimestre

División del año en cuatro períodos de tres meses.

## Comparación interanual

Comparación de períodos equivalentes de años diferentes.

Ejemplo:

Enero de 2025 frente a enero de 2026.

## Tendencia

Comportamiento de una métrica a lo largo del tiempo.

## Crecimiento porcentual

Variación relativa de una métrica entre dos períodos.

Fórmula:

`((valor_actual - valor_anterior) / valor_anterior) * 100`

Si el valor anterior es cero, debe tratarse el caso de manera especial.

---

# 8. CONCEPTOS DE CALIDAD DE DATOS

## Integridad referencial

Propiedad que garantiza que las referencias entre tablas correspondan a registros válidos.

## Unicidad

Propiedad que indica que un identificador no se repite dentro del conjunto que debe ser único.

## Duplicado

Registro repetido de acuerdo con una clave o criterio de identificación.

## Valor nulo

Ausencia de valor representada por NULL.

No es equivalente a cero ni a una cadena vacía.

## Valor desconocido

Valor que representa información que no se pudo identificar.

En las dimensiones de TechStore se utiliza el miembro especial `-1`.

## Dato inválido

Valor que no cumple las reglas de formato, dominio o integridad esperadas.

## Validación

Proceso que comprueba que la información cumple condiciones determinadas.

## Rechazo

Registro que no puede continuar en un proceso de transformación debido a una condición de calidad o integridad.

## Trazabilidad

Capacidad de identificar el origen y el procesamiento de un registro.

## Lote

Conjunto de registros procesados bajo una misma ejecución o identificador de procesamiento.

## Idempotencia

Propiedad de un proceso que permite ejecutarlo varias veces sin producir duplicaciones o cambios incorrectos.

## Auditoría

Información técnica que permite conocer cuándo o cómo se procesó un registro.

---

# 9. DICCIONARIO DE COLUMNAS CONFIRMADAS

Las siguientes columnas han sido identificadas mediante la inspección del modelo.

## 9.1 fact_sales

| Columna | Significado |
|---|---|
| sale_detail_id | Identificador de la línea de detalle. |
| sale_id | Identificador de la operación comercial. |
| customer_sk | Clave sustituta del cliente. |
| product_sk | Clave sustituta del producto. |
| branch_sk | Clave sustituta de la sucursal. |
| payment_method_sk | Clave sustituta del método de pago. |
| date_sk | Clave de la dimensión temporal. |
| sale_timestamp | Fecha y hora de la venta. |
| quantity | Unidades vendidas en la línea. |
| unit_price | Precio unitario registrado. |
| line_discount_amount | Importe de descuento de la línea. |
| line_subtotal_amount | Subtotal de la línea. |
| sale_status | Estado de la venta. |
| _ingestion_timestamp | Marca temporal de ingesta observada. |
| _ingestion_batch | Identificador de lote de ingesta observado. |

Las columnas técnicas deben verificarse contra la estructura actual de Neon.

---

# 10. TÉRMINOS QUE EL AGENTE DEBE DIFERENCIAR

Esta sección es especialmente importante para evitar interpretaciones incorrectas.

## Venta vs. línea de venta

Venta:

Operación comercial completa.

Línea de venta:

Producto incluido dentro de una operación.

Una venta puede contener varias líneas.

## Unidades vs. operaciones

Unidades:

Cantidad de productos comercializados.

Operaciones:

Cantidad de ventas distintas.

Una operación puede contener varias unidades.

## Cliente registrado vs. cliente comprador

Cliente registrado:

Existe en la dimensión de clientes.

Cliente comprador:

Tiene al menos una venta registrada.

## Precio vs. importe

Precio:

Valor correspondiente a una unidad.

Importe:

Valor monetario asociado a una cantidad o transacción.

## Descuento vs. subtotal

Descuento:

Importe descontado.

Subtotal:

Importe resultante de la línea según la lógica de cálculo aplicada.

## Ingresos vs. utilidad

Ingresos:

Importes asociados a las ventas según la definición contable utilizada.

Utilidad:

Resultado después de considerar los costos correspondientes.

No son equivalentes.

## Garantía vs. defecto

Garantía:

Registro relacionado con cobertura o atención.

Defecto:

Problema o falla de un producto.

La existencia de una garantía no demuestra automáticamente un defecto.

## Devolución vs. venta

Venta:

Operación comercial de venta.

Devolución:

Evento posterior o relacionado con la devolución de un producto.

No deben contarse como la misma operación.

## Clave sustituta vs. identificador original

Clave sustituta:

Identificador utilizado por el modelo dimensional.

Identificador original:

Identificador procedente de los datos de origen.

## Cero vs. desconocido

Cero:

Valor numérico igual a cero.

Desconocido:

Información no identificada.

No deben intercambiarse.

---

# 11. INTERPRETACIÓN DE PREGUNTAS DE USUARIO

El agente debe utilizar este apartado para traducir lenguaje natural a conceptos analíticos.

| Pregunta del usuario | Interpretación recomendada |
|---|---|
| ¿Cuánto vendimos? | Aclarar si solicita importe comercial o cantidad de operaciones. |
| ¿Cuántas ventas hicimos? | COUNT(DISTINCT sale_id). |
| ¿Cuántos productos vendimos? | SUM(quantity). |
| ¿Cuántas líneas vendimos? | COUNT(*) en fact_sales. |
| ¿Cuál es el producto más vendido? | Producto con mayor SUM(quantity). |
| ¿Cuál es el producto que más dinero genera? | Producto con mayor SUM(line_subtotal_amount). |
| ¿Quién es nuestro mejor cliente? | Aclarar si se refiere a importe, unidades o frecuencia. |
| ¿Qué sucursal vende más? | Definir si se mide por operaciones, unidades o importe. |
| ¿Qué método de pago se utiliza más? | Analizar ventas por método de pago y definir el conteo. |
| ¿Cuánto descontamos? | SUM(line_discount_amount). |
| ¿Cuál es el ticket promedio? | Importe comercial dividido entre ventas distintas, según definición validada. |
| ¿Cuántos clientes tenemos? | COUNT de la dimensión, diferenciando Unknown Member. |
| ¿Cuántos clientes compraron? | Clientes distintos presentes en fact_sales, excluyendo -1. |
| ¿Cuántas devoluciones hay? | Consultar fact_returns y verificar su granularidad. |
| ¿Cuántas garantías hay? | Consultar fact_warranties y verificar su granularidad. |
| ¿Cuál es la utilidad? | No calcular sin información de costos y definición contable. |
| ¿Cuál fue el crecimiento? | Comparar períodos equivalentes y definir la métrica. |
| ¿Qué marca vende más? | Analizar dim_product mediante su atributo de marca. |

---

# 12. REGLAS SEMÁNTICAS PARA EL AGENTE

El agente debe aplicar las siguientes reglas al interpretar preguntas.

## 12.1 Preguntas ambiguas

Si una pregunta admite diferentes interpretaciones, debe:

1. Identificar la ambigüedad.
2. Determinar si existe una interpretación estándar.
3. Solicitar aclaración cuando sea necesario.
4. Explicar qué indicador utilizará.

Ejemplo:

"¿Cuál es la sucursal que más vende?"

Puede significar:

- Mayor número de ventas.
- Mayor número de unidades.
- Mayor importe comercial.

Si el contexto no permite identificar la intención, debe solicitar aclaración.

## 12.2 Lenguaje comercial

El agente debe comprender expresiones comunes como:

- Vender más.
- Generar más ingresos.
- Tener más clientes.
- Tener más movimiento.
- Producto estrella.
- Mejor sucursal.
- Cliente frecuente.
- Temporada de mayor demanda.

Sin embargo, debe traducir estas expresiones a métricas concretas antes de consultar.

## 12.3 Explicabilidad

El agente debe poder explicar cómo obtuvo un resultado.

No debe presentar únicamente un número.

Debe identificar la métrica utilizada y el período analizado.

## 12.4 Datos insuficientes

Cuando la base de datos no permita responder una pregunta, debe indicarlo claramente.

No debe inventar columnas, valores ni resultados.

---

# 13. CONTEXTO HISTÓRICO DEL CONJUNTO DE DATOS

El conjunto de datos original de TechStore fue generado para simular operaciones comerciales.

## 13.1 Entidades originales

Se trabajó con:

- Clientes.
- Marcas.
- Productos.
- Sucursales.
- Métodos de pago.
- Ventas.
- Detalles de ventas.
- Garantías.
- Devoluciones.

## 13.2 Volumen inicial objetivo

El primer lote tenía un objetivo de 7,920,155 registros distribuidos entre las entidades originales.

Este volumen corresponde al conjunto de datos previo a la transformación y no debe confundirse con el total de registros de las ocho tablas Gold migradas a Neon.

## 13.3 Período de generación

Las operaciones comerciales originales fueron diseñadas para cubrir:

2023-01-01 a 2026-10-31.

## 13.4 Lote incremental

El segundo lote incorporó 5,000 operaciones de inserción y actualización.

Estas operaciones se distribuyeron entre datos CSV y JSON.

## 13.5 Resultado Gold migrado

El modelo Gold migrado contiene:

7,423,594 registros distribuidos en ocho tablas.

Esta es la referencia histórica inicial de Neon.

---

# 14. INSTRUCCIONES PARA MANTENER EL GLOSARIO

Cuando se incorpore un nuevo concepto, debe documentarse utilizando el siguiente formato:

## Nombre del concepto

**Categoría:** técnica, comercial, temporal, métrica o calidad de datos.

**Definición:** descripción precisa.

**Tablas relacionadas:** tablas involucradas.

**Columnas relacionadas:** columnas utilizadas, si corresponde.

**Regla de cálculo:** fórmula o lógica, si corresponde.

**Ejemplo:** ejemplo de interpretación.

**Restricciones:** errores o interpretaciones que deben evitarse.

Los términos deben mantenerse consistentes en todos los documentos.

---

# 15. PRINCIPIO FUNDAMENTAL PARA EL AGENTE

El agente de TechStore debe comprender que los datos no son simplemente números almacenados en tablas.

Cada registro representa una entidad, una característica o un evento dentro del contexto comercial.

Por tanto:

- Debe entender el negocio antes de consultar.
- Debe comprender el modelo antes de relacionar tablas.
- Debe identificar la granularidad antes de agregar datos.
- Debe conocer la definición de cada métrica antes de calcularla.
- Debe reconocer las limitaciones de la información disponible.
- Debe explicar sus resultados.
- Debe evitar inventar información.

**El objetivo no es únicamente generar SQL. El objetivo es transformar los datos de TechStore en conocimiento útil para la toma de decisiones.**

**Última actualización:** 2026-11-27.

**Estado:** glosario inicial del proyecto.