# TECHSTORE — BUSINESS RULES

**Documento:** `business_rules.md`  
**Proyecto:** TechStore  
**Tipo:** Reglas de negocio y lógica analítica  
**Base de datos:** Neon PostgreSQL  
**Database:** techstore  
**Schema:** public  
**Modelo:** Gold — Data Warehouse  
**Última actualización:** 2026-11-27

---

# 1. PROPÓSITO

Este documento define las reglas de negocio que deben utilizarse para interpretar correctamente los datos de TechStore.

Su objetivo es establecer cómo deben entenderse las operaciones comerciales, las ventas, los clientes, los productos, las sucursales, las devoluciones y las garantías.

Este documento es especialmente importante para el agente de inteligencia artificial que se construirá sobre TechStore.

El agente no debe limitarse a ejecutar consultas SQL. Debe comprender el significado de los datos y utilizar reglas de negocio para generar respuestas correctas.

Por ejemplo:

Una consulta que devuelve 5,822,400 filas de `fact_sales` no significa que TechStore haya realizado 5,822,400 ventas.

Significa que existen 5,822,400 registros de líneas de detalle de venta.

Esta diferencia debe ser comprendida por el agente.

---

# 2. CONTEXTO DEL NEGOCIO

TechStore representa una empresa comercial dedicada a la venta de productos tecnológicos.

El modelo analítico permite estudiar las operaciones comerciales desde diferentes perspectivas:

- Clientes.
- Productos.
- Marcas.
- Sucursales.
- Métodos de pago.
- Fechas.
- Ventas.
- Devoluciones.
- Garantías.

El propósito de la plataforma analítica es transformar los datos operacionales en información útil para la toma de decisiones.

Los análisis pueden utilizarse para:

1. Evaluar el rendimiento comercial.
2. Identificar productos de mayor demanda.
3. Comparar sucursales.
4. Analizar el comportamiento de los clientes.
5. Medir los ingresos.
6. Estudiar los descuentos.
7. Identificar tendencias temporales.
8. Analizar devoluciones.
9. Analizar garantías.
10. Detectar oportunidades de mejora.

---

# 3. REGLAS GENERALES DEL MODELO

## BR-001. La base de datos es analítica

La base de datos Neon contiene las ocho tablas Gold del proyecto.

No debe tratarse como una copia completa del sistema transaccional original.

El agente debe utilizarla para análisis, agregaciones, consultas y generación de indicadores.

## BR-002. El modelo es dimensional

El modelo está compuesto por:

### Dimensiones

- `dim_branch`
- `dim_customer`
- `dim_date`
- `dim_payment_method`
- `dim_product`

### Hechos

- `fact_sales`
- `fact_returns`
- `fact_warranties`

Las dimensiones proporcionan contexto y las tablas de hechos contienen las operaciones que se desean analizar.

## BR-003. La granularidad debe respetarse

Cada tabla debe analizarse de acuerdo con su granularidad.

En particular:

`fact_sales` tiene granularidad de línea de detalle.

Una fila representa una línea de una venta.

No debe asumirse que cada fila representa una venta completa.

## BR-004. Los identificadores deben interpretarse correctamente

Las claves sustitutas y los identificadores originales tienen propósitos diferentes.

El agente debe utilizar las claves correspondientes para relacionar dimensiones y hechos.

## BR-005. Las métricas deben tener una definición explícita

Antes de calcular una métrica, el agente debe identificar:

- Qué representa.
- Qué tabla contiene la información.
- Qué columna debe utilizarse.
- Qué nivel de granularidad tiene.
- Qué filtros deben aplicarse.
- Qué período debe analizarse.
- Qué registros deben excluirse.

No debe generar indicadores sin conocer su significado.

---

# 4. REGLAS DE VENTAS

## BR-010. Definición de una venta

Una venta representa una operación comercial identificada mediante `sale_id`.

Una venta puede contener uno o varios productos.

Por tanto, una venta puede generar múltiples líneas de detalle.

## BR-011. Definición de línea de venta

Una línea de venta representa un producto incluido dentro de una operación comercial.

La tabla `fact_sales` utiliza `sale_detail_id` para identificar las líneas.

La granularidad confirmada es:

**Una fila = una línea de detalle de venta.**

## BR-012. Conteo de ventas

Para contar operaciones comerciales distintas, se debe utilizar:

```sql
COUNT(DISTINCT sale_id)
```

No se debe utilizar:

```sql
COUNT(*)
```

como equivalente de número de ventas.

`COUNT(*)` cuenta líneas de detalle.

## BR-013. Conteo de líneas

Para contar líneas de detalle:

```sql
COUNT(*)
```

o:

```sql
COUNT(sale_detail_id)
```

siempre que se conozca la nulabilidad de la columna.

## BR-014. Cantidad de productos vendidos

La cantidad de unidades vendidas debe calcularse utilizando:

```sql
SUM(quantity)
```

Esta métrica representa unidades, no operaciones comerciales.

## BR-015. Precio unitario

`unit_price` representa el precio unitario registrado para una línea de venta.

No representa necesariamente el importe total de la línea.

Para calcular un importe comercial se debe utilizar la métrica monetaria correspondiente.

## BR-016. Descuentos

`line_discount_amount` representa el importe de descuento aplicado a una línea.

El agente debe evitar sumar dos veces el descuento.

Si `line_subtotal_amount` ya representa el subtotal después de aplicar el descuento, no debe restarse nuevamente.

La semántica exacta de los importes debe contrastarse con la transformación ETL y los datos reales.

## BR-017. Subtotal de línea

`line_subtotal_amount` representa el subtotal de la línea de venta.

Puede utilizarse para analizar importes comerciales por producto, sucursal, cliente o período.

El agente debe verificar la definición exacta del subtotal antes de presentarlo como ingreso neto, ingreso bruto o utilidad.

**Importante:** un subtotal de venta no equivale automáticamente a utilidad.

Para calcular utilidad se necesitaría información de costos y una definición de costos aplicable.

No se debe inventar el margen de ganancia.

## BR-018. Ingresos por ventas

Una métrica inicial para analizar el importe comercial registrado es:

```sql
SUM(line_subtotal_amount)
```

La consulta debe utilizar los filtros de estado correspondientes.

El resultado debe describirse como suma de subtotales de línea, salvo que la definición contable del indicador haya sido validada.

## BR-019. Estados de venta

La tabla `fact_sales` contiene `sale_status`.

El agente debe utilizar esta columna cuando el análisis dependa de distinguir operaciones por estado.

No debe asumir cuáles son todos los estados posibles.

Antes de construir un filtro de estado, debe consultar los valores existentes:

```sql
SELECT
    sale_status,
    COUNT(*) AS total_lines,
    COUNT(DISTINCT sale_id) AS total_sales
FROM public.fact_sales
GROUP BY sale_status
ORDER BY total_lines DESC;
```

No debe excluir automáticamente un estado sin conocer su significado.

## BR-020. Ventas por producto

El análisis de ventas por producto debe relacionar `fact_sales` con `dim_product` mediante:

```sql
fact_sales.product_sk = dim_product.product_sk
```

La columna de identificación de la dimensión debe confirmarse en Neon.

El agente debe diferenciar:

- Cantidad de unidades.
- Cantidad de líneas.
- Cantidad de ventas.
- Importe vendido.

## BR-021. Ventas por cliente

El análisis de ventas por cliente debe utilizar la relación entre `fact_sales` y `dim_customer`.

Debe distinguir:

- Clientes registrados.
- Clientes compradores.
- Número de compras por cliente.
- Número de líneas compradas.
- Unidades compradas.
- Importe acumulado.

## BR-022. Ventas por sucursal

El análisis de ventas por sucursal debe relacionar `fact_sales` con `dim_branch`.

Permite estudiar:

- Volumen de ventas.
- Ingresos registrados.
- Unidades vendidas.
- Distribución geográfica.
- Rendimiento comercial.

El agente no debe asumir que una sucursal tiene el mismo volumen de ventas que otra.

## BR-023. Ventas por método de pago

El análisis debe utilizar `payment_method_sk` y su dimensión correspondiente.

El agente puede calcular cantidad de ventas, líneas e importes por método de pago.

No debe confundir cantidad de ventas con cantidad de pagos independientes, salvo que exista una tabla que permita analizar esa distinción.

---

# 5. REGLAS DE CLIENTES

## BR-030. Clientes registrados

La dimensión `dim_customer` contiene los clientes disponibles en el modelo analítico.

El número de filas de esta dimensión no equivale necesariamente al número de clientes que realizaron compras.

## BR-031. Clientes compradores

Un cliente comprador es aquel que tiene al menos una operación registrada en `fact_sales`.

Para calcular clientes compradores identificados:

```sql
SELECT
    COUNT(DISTINCT customer_sk) AS unique_buyers
FROM public.fact_sales
WHERE customer_sk <> -1;
```

Esta consulta utiliza la clave sustituta para contar clientes identificados.

Debe verificarse que la columna exista y tenga el comportamiento esperado en Neon.

## BR-032. Clientes sin compras

Un cliente registrado puede no tener operaciones de venta.

El agente no debe afirmar que todos los clientes registrados son compradores.

## BR-033. Clientes desconocidos

El identificador `-1` representa un miembro desconocido.

No debe contarse como cliente real.

Cuando se calcule la cantidad de clientes reales identificados, debe excluirse.

Cuando se estudie la calidad de los datos, puede ser importante contar los registros asociados a `-1`.

---

# 6. REGLAS DE PRODUCTOS Y MARCAS

## BR-040. Productos registrados

La dimensión `dim_product` representa los productos disponibles en el modelo analítico.

## BR-041. Productos vendidos

Un producto vendido debe tener registros relacionados en `fact_sales`.

La existencia de un producto en la dimensión no demuestra que haya sido vendido.

## BR-042. Productos más vendidos

La clasificación de productos más vendidos debe realizarse según unidades:

```sql
SUM(quantity)
```

No debe utilizarse automáticamente el número de líneas como equivalente de unidades.

## BR-043. Productos con mayores ingresos

Para clasificar productos según el importe comercial registrado, se debe utilizar la suma del subtotal de línea.

El agente debe explicar qué medida utilizó.

## BR-044. Marcas

La dimensión de productos incorpora información de marcas.

No existe una tabla independiente `dim_brand` entre las ocho tablas documentadas de Neon.

Por tanto, el agente debe analizar las marcas a través de `dim_product`.

## BR-045. Productos desconocidos

Si existe un miembro desconocido identificado mediante `-1`, debe tratarse como información no identificada.

No debe presentarse como un producto real.

---

# 7. REGLAS TEMPORALES

## BR-050. Fechas del conjunto de datos

El período histórico del conjunto de datos original de ventas se definió entre:

- Fecha inicial: 2023-01-01.
- Fecha final: 2026-10-31.

Este rango corresponde al diseño del conjunto de datos original y no debe asumirse como el rango definitivo de todas las tablas de hechos.

El agente debe consultar los datos actuales antes de responder preguntas sobre el período disponible.

## BR-051. Clave temporal

La dimensión `dim_date` utiliza una clave con formato:

`YYYYMMDD`

Ejemplo:

2026-11-27 → 20261127.

## BR-052. Análisis por período

Las consultas temporales pueden agrupar los datos por:

- Día.
- Semana.
- Mes.
- Trimestre.
- Año.

La agrupación debe utilizar atributos temporales reales de la dimensión o columnas verificadas.

## BR-053. Comparaciones temporales

Para comparar períodos, el agente debe utilizar intervalos equivalentes cuando corresponda.

Ejemplo:

Comparar enero de 2025 con enero de 2026.

No debe comparar un mes completo con un mes incompleto sin advertirlo.

## BR-054. Fecha del evento

Cada tabla de hechos puede representar eventos diferentes.

El agente debe utilizar la fecha correspondiente al evento que desea estudiar.

No debe asumir que la fecha de venta es también la fecha de devolución o de garantía.

---

# 8. REGLAS DE DEVOLUCIONES

## BR-060. Definición

Una devolución representa un evento relacionado con la devolución de productos o líneas de una operación comercial.

La información se encuentra en `fact_returns`.

## BR-061. Conteo de devoluciones

El conteo debe utilizar la granularidad real de `fact_returns`.

Antes de definir un indicador definitivo, el agente debe verificar si cada fila representa:

- Una devolución completa.
- Una línea devuelta.
- Un producto devuelto.
- Otro nivel de detalle.

No debe asumir la granularidad de la tabla.

## BR-062. Porcentaje de devoluciones

El porcentaje de devoluciones requiere definir primero el numerador y el denominador.

Posibles indicadores:

- Devoluciones por líneas vendidas.
- Ventas con devoluciones sobre ventas totales.
- Unidades devueltas sobre unidades vendidas.
- Importe devuelto sobre importe vendido.

Estos indicadores son diferentes.

El agente debe seleccionar el indicador que corresponda a la pregunta y explicar su definición.

No debe dividir directamente el número de filas de `fact_returns` entre el número de filas de `fact_sales` sin comprobar que las granularidades sean compatibles.

## BR-063. Productos con devoluciones

El análisis debe utilizar las relaciones disponibles en la tabla de hechos y su esquema real.

No debe asumir que una devolución corresponde a una venta completa.

## BR-064. Motivos de devolución

Si existe un atributo de motivo, el agente puede clasificar las devoluciones por ese atributo.

No debe inventar motivos de devolución.

---

# 9. REGLAS DE GARANTÍAS

## BR-070. Definición

Una garantía representa un registro relacionado con la cobertura o atención de un producto vendido.

La información se encuentra en `fact_warranties`.

## BR-071. Interpretación

Una garantía registrada no demuestra automáticamente que exista un defecto de fabricación.

El agente debe diferenciar entre:

- Garantía registrada.
- Garantía activa.
- Garantía vencida.
- Solicitud de garantía.
- Reclamo por defecto.
- Garantía aprobada.

Estas categorías solo pueden utilizarse si existen campos que permitan identificarlas.

## BR-072. Conteo de garantías

El conteo debe respetar la granularidad real de `fact_warranties`.

No se debe asumir que cada fila representa una garantía única hasta verificar la clave correspondiente.

## BR-073. Análisis de garantías

El agente puede analizar las garantías por:

- Producto.
- Marca.
- Sucursal.
- Cliente.
- Período.

Solo cuando las relaciones correspondientes estén confirmadas en el esquema.

## BR-074. Indicadores de garantías

El porcentaje de garantías requiere una definición explícita.

Por ejemplo:

- Garantías registradas por cada 100 líneas vendidas.
- Productos con garantía sobre productos vendidos.
- Garantías por producto.
- Garantías por marca.

El agente no debe presentar estas métricas como equivalentes.

---

# 10. REGLAS DE GARANTÍAS Y DEVOLUCIONES

## BR-080. Exclusividad en el conjunto de datos original

Durante la generación del conjunto de datos se definió que una misma venta podía tener:

- Una garantía.
- Una devolución.
- Ninguno de los dos eventos.

Una venta no debía tener simultáneamente garantía y devolución dentro de esa regla de generación.

Esta regla describe la lógica del conjunto de datos original.

No debe extrapolarse automáticamente a cualquier futuro conjunto de datos o a operaciones reales que se incorporen posteriormente.

## BR-081. Interpretación de registros

El agente debe distinguir entre la cantidad de ventas, devoluciones y garantías.

No debe asumir que una garantía o devolución representa una nueva venta.

## BR-082. Indicadores combinados

Si se calcula un indicador que combine ventas, devoluciones y garantías, se debe comprobar que no existan duplicaciones por JOIN.

No se deben unir directamente varias tablas de hechos entre sí sin identificar primero sus granularidades.

---

# 11. REGLAS DEL PROCESAMIENTO INCREMENTAL

## BR-090. Lotes de datos

El conjunto de datos original fue construido mediante lotes de procesamiento.

Se utilizaron identificadores de lote para distinguir la información procesada.

## BR-091. Lote 1

El primer conjunto de datos tenía una cantidad objetivo de 7,920,155 registros distribuidos entre las entidades originales.

Incluía:

- Clientes.
- Marcas.
- Productos.
- Sucursales.
- Métodos de pago.
- Ventas.
- Detalles de ventas.
- Garantías.
- Devoluciones.

Estas cantidades pertenecen al conjunto original de datos Bronze y no deben confundirse con los conteos finales de Neon.

## BR-092. Lote 2

El segundo lote incorporó registros nuevos y actualizaciones.

Se generaron:

| Tipo | Operaciones |
|---|---:|
| CSV nuevos y actualizaciones | 4,467 |
| JSON nuevos y actualizaciones | 533 |
| Total | 5,000 |

La lógica del lote contempló tanto inserciones como actualizaciones.

## BR-093. Actualizaciones

Un registro actualizado no debe contarse como un registro nuevo.

El agente debe diferenciar entre:

- Filas actuales.
- Filas insertadas.
- Filas actualizadas.
- Operaciones de procesamiento.

## BR-094. Trazabilidad

Los procesos ETL utilizaron identificadores de lote y atributos de auditoría.

La presencia de columnas técnicas en la base Neon debe comprobarse directamente.

El agente no debe asumir que todas las columnas de auditoría originales se conservaron durante la migración.

---

# 12. REGLAS DE MIEMBRO DESCONOCIDO

## BR-100. Identificador desconocido

Las dimensiones utilizan un registro especial con clave `-1`.

Este registro representa información desconocida.

## BR-101. Conteos comerciales

Para análisis de clientes, productos, sucursales o métodos identificados, se debe excluir el miembro desconocido cuando corresponda.

## BR-102. Calidad de datos

Cuando el objetivo sea evaluar la calidad de la información, los registros desconocidos deben incluirse y analizarse.

## BR-103. Transparencia

Si una respuesta excluye miembros desconocidos, el agente debe comunicarlo cuando esa decisión afecte la interpretación del resultado.

Ejemplo:

"El análisis excluye los registros asociados al miembro desconocido (-1)."

---

# 13. REGLAS PARA INDICADORES COMERCIALES

## BR-110. Ventas totales

Definición:

Cantidad de operaciones comerciales distintas.

Referencia:

`COUNT(DISTINCT sale_id)`

## BR-111. Líneas de venta

Definición:

Cantidad de líneas de detalle registradas.

Referencia:

`COUNT(*)` en `fact_sales`.

## BR-112. Unidades vendidas

Definición:

Suma de las cantidades de productos registrados en las líneas.

Referencia:

`SUM(quantity)`.

## BR-113. Importe comercial registrado

Definición:

Suma del subtotal de las líneas de venta.

Referencia:

`SUM(line_subtotal_amount)`.

Debe verificarse la semántica exacta del subtotal antes de denominarlo ingreso neto o bruto.

## BR-114. Descuentos

Definición:

Suma de los importes de descuento registrados en las líneas.

Referencia:

`SUM(line_discount_amount)`.

## BR-115. Clientes compradores

Definición:

Cantidad de clientes distintos con ventas registradas.

Referencia:

`COUNT(DISTINCT customer_sk)` excluyendo `-1`.

## BR-116. Ticket promedio

Una posible definición:

Importe comercial registrado dividido entre el número de ventas distintas.

Conceptualmente:

`SUM(line_subtotal_amount) / COUNT(DISTINCT sale_id)`

Debe utilizar filtros consistentes y evitar la división por cero.

El resultado debe describirse según la definición del importe utilizado.

## BR-117. Promedio de unidades por venta

Definición:

Total de unidades vendidas dividido entre ventas distintas.

Conceptualmente:

`SUM(quantity) / COUNT(DISTINCT sale_id)`

## BR-118. Precio promedio ponderado

Una posible definición:

Importe comercial dividido entre unidades vendidas.

Conceptualmente:

`SUM(line_subtotal_amount) / SUM(quantity)`

Debe excluir cantidades inválidas y utilizar el mismo universo de registros en numerador y denominador.

## BR-119. Participación porcentual

Definición:

Valor de una categoría dividido entre el total correspondiente, multiplicado por 100.

El agente debe asegurarse de que ambos valores utilizan:

- El mismo período.
- Los mismos filtros.
- La misma definición de métrica.

## BR-120. Rentabilidad

No debe calcularse utilidad o rentabilidad únicamente con `unit_price`, `quantity` y `line_subtotal_amount`.

Se necesita información de costos y una definición explícita de utilidad.

Si no existe información suficiente, el agente debe indicar que no puede calcularla correctamente.

---

# 14. PREVENCIÓN DE ERRORES ANALÍTICOS

El agente debe evitar especialmente los siguientes errores:

| Error | Interpretación correcta |
|---|---|
| Contar filas de fact_sales como ventas | Contar `DISTINCT sale_id` |
| Contar líneas como unidades | Sumar `quantity` |
| Confundir clientes registrados con compradores | Consultar los hechos |
| Confundir precio unitario con subtotal | Utilizar la métrica adecuada |
| Restar dos veces los descuentos | Verificar la semántica del subtotal |
| Contar -1 como cliente real | Tratarlo como desconocido |
| Dividir devoluciones entre líneas sin validar granularidad | Definir el indicador primero |
| Suponer que una garantía implica un defecto | Diferenciar evento de diagnóstico |
| Unir hechos directamente sin analizar cardinalidad | Respetar granularidades |
| Calcular utilidad sin costos | Declarar que falta información |

---

# 15. INSTRUCCIONES PARA EL AGENTE DE IA

Estas reglas son obligatorias para cualquier respuesta analítica generada por el agente.

## 15.1 Antes de generar una consulta

El agente debe:

1. Identificar la intención del usuario.
2. Determinar qué indicador se solicita.
3. Identificar la tabla de hechos correspondiente.
4. Identificar las dimensiones necesarias.
5. Verificar las relaciones.
6. Determinar la granularidad.
7. Definir los filtros.
8. Identificar el período.
9. Comprobar los miembros desconocidos.
10. Construir la consulta SQL.

## 15.2 Antes de responder

El agente debe comprobar:

- Que la consulta sea coherente con el modelo.
- Que los JOIN no multipliquen registros indebidamente.
- Que las agregaciones sean correctas.
- Que no exista una división por cero.
- Que las fechas sean correctas.
- Que los filtros sean adecuados.
- Que la métrica tenga una definición clara.

## 15.3 Presentación de resultados

Cuando responda, debe explicar:

1. Qué se calculó.
2. Qué período se utilizó.
3. Qué tablas se consultaron.
4. Qué filtros se aplicaron.
5. Qué significa el resultado.

Ejemplo:

"Durante enero de 2026 se registraron X ventas distintas. El cálculo utiliza COUNT(DISTINCT sale_id), por lo que no cuenta cada línea de detalle como una venta independiente."

## 15.4 Cuando falte información

Si una pregunta requiere información que no existe en la base de datos, debe indicarlo.

Ejemplo:

Usuario: "¿Cuál fue la utilidad neta de la empresa?"

Respuesta esperada:

"No puedo calcular la utilidad neta únicamente con los datos de ventas disponibles. Necesitaría información de costos, gastos y una definición contable de utilidad neta."

No debe inventar resultados.

---

# 16. SEGURIDAD Y OPERACIONES PERMITIDAS

El agente está diseñado principalmente para consultas analíticas.

Debe priorizar:

- SELECT.
- JOIN.
- GROUP BY.
- ORDER BY.
- CTE.
- Subconsultas.
- Funciones de agregación.
- Funciones temporales.

No debe ejecutar operaciones destructivas.

Operaciones prohibidas sin autorización explícita:

- DROP.
- TRUNCATE.
- DELETE.
- UPDATE.
- INSERT.
- ALTER.
- CREATE.
- GRANT.
- REVOKE.

La conexión del agente debe utilizar credenciales protegidas y permisos mínimos.

No debe exponer:

- Contraseñas.
- DATABASE_URL.
- Tokens.
- Secretos.
- Credenciales de Neon.

---

# 17. MANTENIMIENTO DE LAS REGLAS

Este documento debe actualizarse cuando:

- Cambie la definición de una métrica.
- Se modifique una regla comercial.
- Se incorpore una nueva fuente.
- Se modifique la lógica ETL.
- Cambie la granularidad de una tabla.
- Se agregue una nueva operación comercial.
- Se modifique la interpretación de ventas, devoluciones o garantías.

Toda regla nueva debe incluir:

1. Identificador único.
2. Nombre.
3. Descripción.
4. Justificación.
5. Tablas involucradas.
6. Métricas afectadas.
7. Fecha de actualización.

**Última actualización:** 2026-11-27.

**Estado:** reglas analíticas iniciales documentadas. Las definiciones monetarias definitivas y las granularidades de devoluciones y garantías deben contrastarse con el ETL y el esquema real.