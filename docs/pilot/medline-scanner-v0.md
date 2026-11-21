# Scanner v0 de Medline

Piloto local de investigación para MDLN (CIK 0002046386) basado en el [diseño aprobado del PR #2](https://github.com/vjack666/social-arbitrage-scanner/pull/2). Requiere Python 3.12 con SQLite, ambos de la biblioteca estándar. No usa servicios de pago ni instala dependencias. Cada ejecución es manual. Los datos y resultados permanecen locales salvo exportación explícita por el operador.

## Fuentes y verificación

| Fuente | Uso y estado |
| --- | --- |
| SEC EDGAR | Submissions pública sin clave. Se verificaron el directorio de APIs y documentos públicos de Medline. El adaptador usa como máximo una solicitud por ejecución, una por segundo por base local, sin reintentos automáticos ni redirecciones. Identificarse con nombre/organización y correo real en `SEC_USER_AGENT`. No se verificó una respuesta automatizada de Submissions desde este entorno con un contacto autorizado. Se probó el analizador con una transcripción de datos reales del índice 8-K. Se guardan metadatos, enlaces y resúmenes originales. La API devuelve la sección reciente y las páginas históricas se informan como cobertura parcial cuando se superponen. [SEC API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) · [Fair Access](https://www.sec.gov/about/developer-resources#fair-access) · [Índice 8-K de Medline](https://www.sec.gov/Archives/edgar/data/1193125/000119312526467193/0001193125-26-467193-index.htm) |
| Medline IR y FDA | Entrada manual de citas y resúmenes. Se verificaron el prospecto definitivo con fecha de registro 19 de noviembre y la ficha FDA publicada el 20 que corresponde a un retiro iniciado el 8 de octubre. La consulta exploratoria en openFDA para la ventana devolvió HTTP 404; el registro de FDA se verificó por separado. La API se actualiza semanalmente y queda fuera de la colección automática de v0. [Medline IR](https://medline.gcs-web.com/sec-filings/sec-filing/424b4/0001193125-26-468586) · [Ficha FDA](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRes/res.cfm?id=223519) · [openFDA](https://open.fda.gov/apis/device/enforcement/) |
| Noticias públicas | Importación manual de referencias y resúmenes originales cuando el operador puede conservarlos. Proporcionar identidad editorial compartida para republicaciones. Sin descarga de artículos ni scraping. |
| Cotizaciones | Se verificaron cierres y volúmenes de Medline mediante consulta manual de históricos públicos. El operador importa un archivo local autorizado y consigna la fuente y política de uso. Alpha Vantage documenta series diarias compactas para clave gratuita y una cuota estándar de 25 solicitudes diarias. Sus términos limitan el uso de acceso personal. No se verificaron clave, respuesta MDLN ni permisos de retención/republicación. El proveedor automatizado queda desactivado y no se publican bases de datos ni series. [Alpha Vantage, API diaria](https://www.alphavantage.co/documentation/#daily) · [Cuota](https://www.alphavantage.co/premium/) · [Términos](https://www.alphavantage.co/terms_of_service/) |

La licencia consignada en el archivo acompaña cada observación. El operador valida que puede guardar y exportar sus entradas. Conservar archivos de mercado, snapshots y credenciales fuera de Git. Los términos y permisos de cada fuente determinan la retención admisible. X, Reddit, Stocktwits y conectores de órdenes están fuera del piloto.

## Ejecutar

Desde la raíz del repositorio, con Python 3.12 en el entorno:

```text
python -m scanner --db .scanner/medline.sqlite3 collect --start 2026-11-16 --cutoff 2026-11-19T16:05:00-05:00 --input .scanner/medline.json
python -m scanner --db .scanner/medline.sqlite3 collect --start 2026-11-16 --cutoff 2026-11-20T16:05:00-05:00 --input .scanner/medline.json --baseline ID_ANTERIOR
python -m scanner --db .scanner/medline.sqlite3 compare --snapshot ID_ACTUAL
python -m scanner --db .scanner/medline.sqlite3 report --snapshot ID_ACTUAL
python -m scanner --db .scanner/medline.sqlite3 report --snapshot ID_ACTUAL --format json
```

`collect` devuelve el ID. Usar el primer ID como `ID_ANTERIOR` y el segundo como `ID_ACTUAL`. En capturas sucesivas utilizar la misma fecha inicial y un corte igual o posterior. El corte con offset conserva el día local para referencias que solo traen fecha. `compare` y `report` leen SQLite en modo de solo lectura y funcionan sin red. Para consultar la SEC agregar `--sec` a `collect` después de configurar el contacto válido en el entorno. Para una exportación local auténtica de Submissions, usar `--sec-json ARCHIVO --sec-retrieved-at FECHA_ISO`. El reporte muestra errores y coberturas faltantes. Una captura incompleta sigue siendo consultable y nunca convierte un faltante en cero.

### Entrada JSON

El objeto acepta arrays `documents` y `prices`. El programa procesa solamente entradas de Medline. En ambos arrays se requieren `publisher`, `url` HTTPS y `license` con la política de uso. Fechas de calendario usan `YYYY-MM-DD` y horas ISO 8601 con offset. Registrar `published_at` o `published_date`, `event_at` o `event_date` y, cuando se pueda probar, `available_at`. El programa registra `retrieved_at` al importar salvo que el archivo incluya la recuperación original comprobada. Una corrección retrospectiva necesita su propia disponibilidad; usar la hora de la corrección para `available_at` y `source_version` para identificarla.

- Cada documento requiere `claim` (resumen original), `category` (`earnings`, `capital`, `regulatory`, `listing`, `product`, `other`), `source_type` (`filing`, `issuer_release`, `regulator`, `exchange` para una fuente primaria o un tipo descriptivo para el resto) y `verification` (`primary_source`, `corroborated`, `unverified`, `disputed`, `retracted`). Usar `id` para agrupar el mismo evento, `origin` para distinguir orígenes independientes y `notes` para limitaciones. Para unir una nota curada con EDGAR usar `sec:NUMERO_DE_ACCESO` como ID y origen. `impact` admite `binding_terms`, `guidance` y `process_status` cuando el documento respalda el cambio, y se omite cuando la materialidad siga abierta.
- Cada barra requiere `provider`, `session`, hora de fin de sesión regular en `event_at`, `currency`, `adjustment` (`as_traded`, `split_adjusted`, `total_return_adjusted`, `unknown`) y al menos uno de `open`, `high`, `low`, `close`. Precios decimales, preferiblemente como texto. `volume` es cantidad entera de acciones o nulo. Registrar la hora de disponibilidad solo cuando la fuente permita verificarla para **todos** los campos importados. El timestamp de cierre por sí solo no valida la hora de publicación del volumen.

### Qué compara

- Huellas y claves estables colapsan duplicados exactos. Las copias con el mismo origen cuentan como una sola fuente independiente y conservan los enlaces. Las versiones previas y sus diferencias quedan disponibles por ID. Una referencia ausente se etiqueta como cobertura parcial o no observada.
- Las evidencias con disponibilidad demostrada al corte se distinguen de las observaciones retrospectivas. El prospecto y la ficha FDA del piloto conservan la fecha conocida sin asignarles una hora.
- Cierres y volúmenes por sesión, divisa y criterio de ajuste conservan las diferencias entre proveedores. El cambio de cierre usa la barra anterior observada de la misma serie. Con 20 observaciones de volumen válidas se calcula la razón frente a su mediana. El calendario de mercado completo no se valida en v0, por lo que una entrada con huecos no demuestra secuencia diaria completa. Una variación de cierre de al menos 5% o volumen de al menos 2 veces su mediana se marca para revisión de mercado. La clasificación documental de materialidad requiere evidencia primaria y una razón consignada.

## Pruebas

```text
python -m unittest discover -s tests -v
```

La suite cubre corte, deduplicación, revisiones, procedencia, conservación de conflictos, formato inválido, fallos de cobertura, parser SEC y reproducción local. La prueba con fuentes públicas compara los cortes del 19 y 20 de noviembre a las 16:05 de Nueva York y Ecuador. MarketScreener marca el cierre de USD 37,04 con hora de cotización de 16:00:01 ET. Dos históricos coinciden en el cierre y discrepan en el volumen. Estas observaciones aparecen en el anexo retrospectivo porque la hora de publicación no está verificada. [MarketScreener](https://www.marketscreener.com/quote/stock/MEDLINE-INC-200622770/quotes/) · [Stock Analysis](https://stockanalysis.com/stocks/mdln/history/) · [Stocknear](https://www.stocknear.com/stocks/MDLN/history)
