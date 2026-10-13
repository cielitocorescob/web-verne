# Pendientes de implementación · eBook Marca Directiva

Los botones y formularios están preparados, pero varios destinos aún no se han entregado. No se usan enlaces inventados: cada destino se configura en el objeto `CTA_CONFIG` del script de `marca-directiva.html`. Mientras un valor sea `null`, el botón no navega y el formulario no envía ni guarda datos.

| CTA | Ubicación | Botón | Pendiente | Responsable | Dónde se configura |
|---|---|---|---|---|---|
| 1 | Después de la introducción | Descarga la guía de 1 página | Integración de envío del formulario (Nombre, correo, celular, cargo, empresa) y archivo de la guía | Por definir | `CTA_CONFIG.cta1.formEndpoint` y `.recurso` |
| 4 | Después de los arquetipos | Haz el test (3 min) | URL del test de arquetipos en la web de Verne | Nuria Peláez | `CTA_CONFIG.cta4.url` |
| 5 | Después de «Donde el sistema todavía falla» | Conoce tu nota (30 min) | URL del calendario de reservas de Julio Talledo o Víctor Lozano | Por definir | `CTA_CONFIG.cta5.url` |
| 8 | Final de la sección 5 | Descarga el checklist GEO (1 hoja) | Integración de envío del formulario y archivo del checklist GEO | Por definir | `CTA_CONFIG.cta8.formEndpoint` y `.recurso` |
| 10 | Cierre del eBook | Agenda y conoce tu nota | URL del calendario de reservas de Julio Talledo o Víctor Lozano | Por definir | `CTA_CONFIG.cta10.url` |
| 10 | Cierre del eBook | Enlace «¿Prefieres algo más directo? Escríbenos por WhatsApp.» | Enlace de WhatsApp de Julio Talledo (confirmar número y formato internacional) | Por definir | `CTA_CONFIG.whatsapp.url` |
| 10 | Cierre del eBook | QR al calendario de reservas | Generar el código QR cuando el calendario esté confirmado; hoy se muestra un marco con el ícono, sin código activo | Por definir | `CTA_CONFIG.qr.url` y el bloque `.qr[data-cta-qr]` |

## Comportamiento actual de los formularios (CTA 1 y 8)

- Validan los cinco campos: nombre y cargo/empresa con al menos 2 caracteres, correo con formato válido y celular con 9 a 15 dígitos.
- Marcan los campos con error (`aria-invalid`) y muestran el mensaje debajo de cada campo.
- Con datos válidos muestran: «Gracias, {nombre}. Tus datos están completos. La descarga estará disponible muy pronto.». No envían ni guardan nada, y no simulan una descarga.
- Al configurar `formEndpoint`, completar el bloque marcado como «Integración pendiente» en el script: enviar los datos y, si la respuesta es correcta, entregar `recurso`.

## Otros pendientes del documento

- Revisar redacción en el Word, sección 3: «el principal uso de la IA generativa ese fue la terapia…».
- Cargo de Marco Fragale: la lámina del Ranking dice «CEO Orygen» y el caso de la sección 6 dice «Country Manager de Enel Perú».
- La imagen «Confían en nosotros» del Word incluye dos veces el logo de la Universidad de Piura; se mantuvo.
- Fotos de los directivos destacados tomadas de las láminas del Word (unos 100 px); conviene recibir los retratos originales.
- Fotografía de apertura: imagen de la plantilla Verne. La fotografía generada en Magnific no pudo descargarse desde el entorno de trabajo.
- El documento no detalla los temas en las posiciones 2.ª a 4.ª del ranking de temas publicados.
