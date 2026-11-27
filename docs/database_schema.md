# Esquema de la base de datos — TechStore

## 1. Descripción general

La base de datos de TechStore contiene un modelo dimensional compuesto por ocho tablas, diseñado para facilitar el análisis de ventas, clientes, productos, sucursales, garantías y devoluciones.

El modelo sigue una estructura de **esquema en estrella (Star Schema)**, organizada en dos grupos:

- **Tablas de dimensiones:** contienen información descriptiva que permite contextualizar y segmentar los datos.
- **Tablas de hechos:** contienen los registros de eventos y operaciones del negocio que se utilizan para realizar cálculos y análisis.

La base de datos está compuesta por las siguientes tablas:

| Tabla | Tipo | Descripción |
|---|---|---|
| `dim_branch` | Dimensión | Información de las sucursales. |
| `dim_customer` | Dimensión | Información de los clientes. |
| `dim_date` | Dimensión | Información de las fechas para análisis temporales. |
| `dim_payment_method` | Dimensión | Información de los métodos de pago. |
| `dim_product` | Dimensión | Información de los productos y sus marcas. |
| `fact_sales` | Hechos | Detalles de las ventas realizadas. |
| `fact_warranties` | Hechos | Registros de garantías. |
| `fact_returns` | Hechos | Registros de devoluciones. |

**Volumen actual de información:**

| Tabla | Registros |
|---|---:|
| `dim_branch` | 53 |
| `dim_customer` | 500.301 |
| `dim_date` | 5.845 |
| `dim_payment_method` | 6 |
| `dim_product` | 100.151 |
| `fact_returns` | 494.658 |
| `fact_sales` | 5.822.400 |
| `fact_warranties` | 500.180 |
| **Total** | **7.423.594** |

Estos valores representan el volumen de referencia de las tablas y pueden cambiar si se actualiza la información.

---

## 2. Estructura del modelo dimensional

### 2.1. Tablas de dimensiones

Las dimensiones proporcionan información descriptiva para interpretar y clasificar los registros de las tablas de hechos.

Las cinco dimensiones disponibles son:

- `dim_branch`
- `dim_customer`
- `dim_date`
- `dim_payment_method`
- `dim_product`

Cada dimensión contiene una clave sustituta (*Surrogate Key*) que permite identificar sus registros y establecer relaciones con las tablas de hechos correspondientes.

### 2.2. Tablas de hechos

Las tablas de hechos almacenan los eventos principales del negocio.

TechStore cuenta con tres tablas de hechos:

- `fact_sales`: registra los detalles individuales de las ventas.
- `fact_warranties`: registra los eventos de garantías.
- `fact_returns`: registra los eventos de devoluciones.

Cada tabla tiene una granularidad diferente. Esta característica es fundamental para construir consultas SQL correctas y evitar duplicaciones en los resultados.

### 2.3. Relaciones entre dimensiones y hechos

Las relaciones conceptuales del modelo son las siguientes:

| Tabla de hechos | Dimensiones relacionadas |
|---|---|
| `fact_sales` | `dim_branch`, `dim_customer`, `dim_date`, `dim_payment_method`, `dim_product` |
| `fact_warranties` | `dim_branch`, `dim_customer`, `dim_date`, `dim_product` |
| `fact_returns` | `dim_branch`, `dim_customer`, `dim_date`, `dim_product` |

Las relaciones se establecen mediante las claves de las dimensiones almacenadas en las respectivas tablas de hechos.

Estas relaciones representan la estructura lógica del modelo. No se debe asumir que existen restricciones físicas de clave primaria o foránea en PostgreSQL sin verificarlas directamente.

---

## 3. Descripción de las tablas de dimensiones

### 3.1. `dim_branch` — Dimensión de sucursales

**Descripción:**

Almacena la información descriptiva de las sucursales de TechStore. Permite analizar el comportamiento comercial según la ubicación geográfica y las características de cada establecimiento.

**Granularidad:**

Un registro por cada sucursal.

**Cantidad de registros de referencia:** 53.

**Atributos conocidos:**

| Columna | Descripción |
|---|---|
| `branch_sk` | Clave sustituta de la sucursal. |
| `branch_id` | Identificador de negocio de la sucursal. |
| `branch_name` | Nombre de la sucursal. |
| `city` | Ciudad donde se encuentra ubicada. |
| `department` | Departamento al que pertenece. |
| `address` | Dirección física de la sucursal. |
| `opening_date` | Fecha de apertura de la sucursal. |
| `status` | Estado de la sucursal. |

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Qué sucursales generan mayores ingresos?
- ¿Qué ciudades presentan mayores ventas?
- ¿Cuántas ventas se realizan por departamento?
- ¿Qué sucursales tienen mayor volumen de operaciones?
- ¿Cómo se distribuyen las ventas geográficamente?

### 3.2. `dim_customer` — Dimensión de clientes

**Descripción:**

Almacena la información descriptiva de los clientes de TechStore. Permite analizar el comportamiento de compra y segmentar las ventas según las características de los consumidores.

**Granularidad:**

Un registro por cada cliente.

**Cantidad de registros de referencia:** 500.301.

**Atributos:**

Los nombres, tipos de datos y descripciones de todas las columnas deben corresponder exactamente con el esquema existente en Neon.

| Columna | Descripción |
|---|---|
| `customer_sk` | Clave sustituta del cliente. |
| Otras columnas | Atributos descriptivos del cliente. |

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Cuáles son los clientes que más compran?
- ¿Cuántos clientes únicos realizaron compras?
- ¿Cómo se distribuyen los clientes?
- ¿Qué clientes generan mayores ingresos?
- ¿Cuál es el comportamiento de compra de los clientes?

### 3.3. `dim_date` — Dimensión de fechas

**Descripción:**

Contiene los atributos temporales utilizados para analizar las operaciones de TechStore.

Esta dimensión permite realizar agrupaciones y comparaciones por día, semana, mes, trimestre y año, según los atributos disponibles en la tabla.

**Granularidad:**

Un registro por cada fecha del calendario.

**Cantidad de registros de referencia:** 5.845.

**Atributos conocidos:**

| Columna | Descripción |
|---|---|
| `date_sk` | Clave de fecha en formato numérico `YYYYMMDD`. |
| Otras columnas | Atributos de calendario para análisis temporal. |

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Cuáles fueron las ventas de cada mes?
- ¿Qué año presentó mayores ingresos?
- ¿Cómo evolucionaron las ventas?
- ¿Qué meses registraron mayor actividad comercial?
- ¿Cómo se comportaron las ventas entre diferentes períodos?

**Consideración importante:**

La clave `date_sk` utiliza el formato `YYYYMMDD`. Por ejemplo, una fecha como el 27 de noviembre de 2026 se representa mediante la clave `20261127`.

Para realizar análisis temporales se deben utilizar los atributos reales disponibles en esta dimensión y verificar las relaciones correspondientes con las tablas de hechos.

### 3.4. `dim_payment_method` — Dimensión de métodos de pago

**Descripción:**

Almacena los métodos de pago disponibles para las operaciones comerciales de TechStore.

Permite clasificar las ventas según el medio utilizado por los clientes para realizar sus pagos.

**Granularidad:**

Un registro por cada método de pago.

**Cantidad de registros de referencia:** 6.

**Atributos:**

| Columna | Descripción |
|---|---|
| `payment_method_sk` | Clave sustituta del método de pago. |
| Otras columnas | Identificador y atributos descriptivos del método de pago. |

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Cuál es el método de pago más utilizado?
- ¿Qué porcentaje de las ventas corresponde a cada método?
- ¿Cuánto dinero se ha recaudado por método de pago?
- ¿Cómo se distribuyen las operaciones según el medio de pago?

### 3.5. `dim_product` — Dimensión de productos

**Descripción:**

Almacena la información descriptiva de los productos comercializados por TechStore.

Incluye información relacionada con las marcas, por lo que los atributos de marca se encuentran integrados en esta dimensión. No se debe asumir que existe una dimensión independiente de marcas.

**Granularidad:**

Un registro por cada producto.

**Cantidad de registros de referencia:** 100.151.

**Atributos:**

| Columna | Descripción |
|---|---|
| `product_sk` | Clave sustituta del producto. |
| Otras columnas | Identificador, nombre, características y atributos del producto, incluyendo la información de marca disponible. |

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Cuáles son los productos más vendidos?
- ¿Qué marcas generan mayores ingresos?
- ¿Qué productos presentan mayor demanda?
- ¿Cuáles son los productos con menor movimiento?
- ¿Cómo se distribuyen las ventas por marca?
- ¿Qué productos presentan más devoluciones o garantías?

---

## 4. Descripción de las tablas de hechos

### 4.1. `fact_sales` — Hechos de ventas

**Descripción:**

Almacena los detalles individuales de las ventas realizadas en TechStore.

Es la tabla principal para analizar el comportamiento comercial, los ingresos generados, las cantidades vendidas y el desempeño de los productos, clientes y sucursales.

**Granularidad:**

Un registro por cada detalle de venta, identificado mediante `sale_detail_id`.

Esto significa que una venta puede contener varios productos y, por tanto, generar múltiples registros en esta tabla.

**Cantidad de registros de referencia:** 5.822.400.

**Dimensiones relacionadas:**

- `dim_branch`
- `dim_customer`
- `dim_date`
- `dim_payment_method`
- `dim_product`

**Claves y atributos:**

La tabla contiene las referencias a las dimensiones y los atributos propios del detalle de venta.

| Columna | Descripción |
|---|---|
| `sale_detail_id` | Identificador del detalle individual de venta. |
| Otras columnas | Claves dimensionales, identificadores de negocio y métricas del detalle de venta. |

Los nombres y tipos de datos exactos deben obtenerse del esquema real de Neon.

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Cuánto ha vendido TechStore?
- ¿Cuántas unidades se han vendido?
- ¿Cuál es el ingreso generado por producto?
- ¿Cuáles son los productos más vendidos?
- ¿Qué sucursales generan mayores ingresos?
- ¿Cuáles son los clientes que más compran?
- ¿Cómo evolucionan las ventas a lo largo del tiempo?
- ¿Qué métodos de pago generan mayor volumen de operaciones?

**Consideraciones importantes:**

1. El nivel de detalle de esta tabla es el producto vendido dentro de una operación, no la venta completa.
2. Una misma venta puede aparecer en múltiples registros.
3. Para calcular el número de ventas se debe utilizar el identificador de la venta y contar sus valores únicos, no contar directamente las filas.
4. Los ingresos deben calcularse utilizando los importes correspondientes al detalle de venta.
5. No se deben asumir importes de cabecera duplicados en cada detalle.
6. Para calcular cantidades vendidas se debe utilizar la columna real que representa las unidades del detalle.

### 4.2. `fact_warranties` — Hechos de garantías

**Descripción:**

Almacena los eventos de garantías asociados a los productos comercializados por TechStore.

Permite analizar el comportamiento de las garantías y estudiar su distribución según productos, clientes, sucursales y períodos de tiempo.

**Granularidad:**

Un registro por cada evento de garantía.

**Cantidad de registros de referencia:** 500.180.

**Dimensiones relacionadas:**

- `dim_branch`
- `dim_customer`
- `dim_date`
- `dim_product`

**Claves y atributos:**

La tabla contiene referencias a las dimensiones correspondientes y los atributos propios de cada evento de garantía.

| Columna | Descripción |
|---|---|
| Otras columnas | Identificadores, claves dimensionales y atributos del evento de garantía. |

Los nombres y tipos de datos exactos deben obtenerse del esquema real de Neon.

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Cuántas garantías se han registrado?
- ¿Qué productos presentan más garantías?
- ¿Qué marcas concentran más eventos de garantía?
- ¿Cómo se distribuyen las garantías por sucursal?
- ¿Cuántas garantías se registraron durante un período determinado?
- ¿Qué clientes registran más garantías?

### 4.3. `fact_returns` — Hechos de devoluciones

**Descripción:**

Almacena los eventos de devolución asociados a los productos comercializados por TechStore.

Permite estudiar el comportamiento de las devoluciones y analizar su distribución por productos, clientes, sucursales y períodos de tiempo.

**Granularidad:**

Un registro por cada evento de devolución.

**Cantidad de registros de referencia:** 494.658.

**Dimensiones relacionadas:**

- `dim_branch`
- `dim_customer`
- `dim_date`
- `dim_product`

**Claves y atributos:**

La tabla contiene referencias a las dimensiones correspondientes y los atributos propios de cada evento de devolución.

| Columna | Descripción |
|---|---|
| Otras columnas | Identificadores, claves dimensionales y atributos del evento de devolución. |

Los nombres y tipos de datos exactos deben obtenerse del esquema real de Neon.

**Utilidad analítica:**

Permite responder preguntas como:

- ¿Cuántas devoluciones se han registrado?
- ¿Qué productos presentan más devoluciones?
- ¿Qué marcas concentran más devoluciones?
- ¿Qué sucursales registran más devoluciones?
- ¿Cómo evolucionan las devoluciones a lo largo del tiempo?
- ¿Qué clientes registran más devoluciones?

---

## 5. Claves sustitutas y registros desconocidos

### 5.1. Claves sustitutas

Las dimensiones utilizan claves sustitutas (*Surrogate Keys*) para identificar sus registros.

Estas claves permiten establecer relaciones entre las dimensiones y las tablas de hechos sin depender directamente de los identificadores originales del negocio.

Las claves sustitutas se utilizan como referencias dentro del modelo dimensional.

### 5.2. Registro desconocido (Unknown Member)

Las dimensiones cuentan con un registro especial identificado mediante la clave `-1`.

Este registro representa un valor desconocido o no identificado.

Su finalidad es permitir que los registros de las tablas de hechos mantengan una referencia válida cuando no existe información dimensional disponible.

**Regla importante:**

El valor `-1` no representa un cliente, producto, sucursal o método de pago real. Representa un registro desconocido dentro del modelo dimensional.

Por esta razón, los análisis que involucren dimensiones deben considerar este registro y decidir si se incluye o excluye según el objetivo de la consulta.

---

## 6. Consideraciones para construir consultas SQL

Las siguientes reglas son fundamentales para consultar correctamente el modelo dimensional.

### 6.1. Utilizar las dimensiones para contextualizar los hechos

Cuando se necesite analizar información por producto, cliente, sucursal, fecha o método de pago, se deben relacionar las tablas de hechos con las dimensiones correspondientes.

Las relaciones deben utilizar las claves dimensionales reales existentes en las tablas.

### 6.2. Respetar la granularidad de cada tabla

Cada tabla de hechos representa un tipo diferente de evento:

| Tabla | Granularidad |
|---|---|
| `fact_sales` | Un registro por detalle de venta. |
| `fact_warranties` | Un registro por evento de garantía. |
| `fact_returns` | Un registro por evento de devolución. |

No se deben interpretar las filas de estas tablas como si todas representaran el mismo tipo de operación.

### 6.3. Evitar duplicaciones al relacionar tablas de hechos

No se recomienda unir directamente `fact_sales`, `fact_warranties` y `fact_returns` utilizando únicamente las claves dimensionales.

Una unión de este tipo puede multiplicar los registros cuando existen múltiples eventos asociados a una misma dimensión.

Por ejemplo, si un producto tiene varios detalles de venta, garantías y devoluciones, una unión directa entre las tres tablas puede generar combinaciones de registros que alteren los resultados.

**Recomendación:**

Cuando se necesite comparar métricas de diferentes tablas de hechos:

1. Consultar cada tabla de hechos de manera independiente.
2. Agrupar los resultados según las dimensiones necesarias.
3. Calcular las métricas correspondientes.
4. Relacionar los resultados agregados mediante las dimensiones comunes.

### 6.4. Diferenciar cantidad de registros y cantidad de operaciones

En `fact_sales`, contar las filas no equivale a contar las ventas.

Debido a que cada fila representa un detalle de venta, se debe utilizar el identificador de la venta para calcular el número de operaciones únicas.

De igual manera, se debe distinguir entre:

- Cantidad de detalles de venta.
- Cantidad de ventas únicas.
- Cantidad de unidades vendidas.
- Ingresos generados.

Cada métrica debe calcularse utilizando el atributo correspondiente.

### 6.5. Utilizar correctamente las fechas

Para realizar análisis temporales se deben utilizar las relaciones con `dim_date` y los atributos de calendario disponibles.

No se deben asumir nombres de columnas temporales ni formatos que no estén presentes en el esquema real.

### 6.6. Identificar correctamente los importes

Los cálculos financieros deben utilizar las columnas monetarias correspondientes a cada tabla.

No se deben inventar columnas de ingresos, costos, precios, descuentos o totales.

Antes de construir una consulta, se debe verificar qué métricas están disponibles y qué representa cada una.

---

## 7. Resumen de relaciones y granularidad

| Tabla | Tipo | Granularidad | Registros de referencia |
|---|---|---|---:|
| `dim_branch` | Dimensión | Una sucursal | 53 |
| `dim_customer` | Dimensión | Un cliente | 500.301 |
| `dim_date` | Dimensión | Una fecha | 5.845 |
| `dim_payment_method` | Dimensión | Un método de pago | 6 |
| `dim_product` | Dimensión | Un producto | 100.151 |
| `fact_sales` | Hechos | Un detalle de venta | 5.822.400 |
| `fact_warranties` | Hechos | Un evento de garantía | 500.180 |
| `fact_returns` | Hechos | Un evento de devolución | 494.658 |

---

## 8. Verificación del esquema real en Neon

Para mantener la documentación sincronizada con la base de datos, se deben consultar directamente los metadatos del esquema `public`.

Las siguientes consultas permiten obtener los nombres de las columnas, sus tipos de datos, restricciones y relaciones existentes.

### 8.1. Consultar las columnas y tipos de datos

```sql
SELECT
    table_name,
    ordinal_position,
    column_name,
    data_type,
    udt_name,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN (
      'dim_branch',
      'dim_customer',
      'dim_date',
      'dim_payment_method',
      'dim_product',
      'fact_sales',
      'fact_warranties',
      'fact_returns'
  )
ORDER BY
    table_name,
    ordinal_position;
```

Esta consulta permite identificar todas las columnas de las ocho tablas, respetando su orden original y mostrando sus tipos de datos.

### 8.2. Consultar las claves primarias

```sql
SELECT
    tc.table_name,
    kcu.column_name,
    tc.constraint_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
   AND tc.constraint_schema = kcu.constraint_schema
WHERE tc.table_schema = 'public'
  AND tc.constraint_type = 'PRIMARY KEY'
  AND tc.table_name IN (
      'dim_branch',
      'dim_customer',
      'dim_date',
      'dim_payment_method',
      'dim_product',
      'fact_sales',
      'fact_warranties',
      'fact_returns'
  )
ORDER BY
    tc.table_name,
    kcu.ordinal_position;
```

Esta consulta permite verificar qué claves primarias están implementadas físicamente en PostgreSQL.

### 8.3. Consultar las claves foráneas

```sql
SELECT
    tc.table_name AS source_table,
    kcu.column_name AS source_column,
    ccu.table_name AS referenced_table,
    ccu.column_name AS referenced_column,
    tc.constraint_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
   AND tc.constraint_schema = kcu.constraint_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
   AND ccu.constraint_schema = tc.constraint_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY
    tc.table_name,
    kcu.column_name;
```

Esta consulta permite verificar las relaciones implementadas mediante restricciones de clave foránea.

**Importante:** que una relación no aparezca en esta consulta no significa necesariamente que no exista una relación lógica entre las tablas. Puede tratarse de una relación utilizada por el modelo dimensional sin una restricción física implementada.

### 8.4. Consultar la cantidad actual de registros

```sql
SELECT 'dim_branch' AS table_name, COUNT(*) AS total_records
FROM public.dim_branch

UNION ALL

SELECT 'dim_customer', COUNT(*)
FROM public.dim_customer

UNION ALL

SELECT 'dim_date', COUNT(*)
FROM public.dim_date

UNION ALL

SELECT 'dim_payment_method', COUNT(*)
FROM public.dim_payment_method

UNION ALL

SELECT 'dim_product', COUNT(*)
FROM public.dim_product

UNION ALL

SELECT 'fact_sales', COUNT(*)
FROM public.fact_sales

UNION ALL

SELECT 'fact_warranties', COUNT(*)
FROM public.fact_warranties

UNION ALL

SELECT 'fact_returns', COUNT(*)
FROM public.fact_returns

ORDER BY table_name;
```

---

## 9. Consideraciones finales

La base de datos de TechStore está organizada mediante un modelo dimensional de ocho tablas, compuesto por cinco dimensiones y tres tablas de hechos.

Su estructura permite realizar análisis sobre:

- Ventas e ingresos.
- Clientes y comportamiento de compra.
- Productos y marcas.
- Sucursales y ubicación geográfica.
- Métodos de pago.
- Garantías.
- Devoluciones.
- Evolución temporal de las operaciones.

Para construir consultas confiables es indispensable respetar la granularidad de cada tabla, utilizar las relaciones dimensionales correctas y evitar operaciones que puedan duplicar registros o alterar las métricas.

**Regla general:** todas las consultas deben basarse exclusivamente en las columnas, tipos de datos, relaciones y métricas que realmente existen en las ocho tablas de la base de datos de Neon.