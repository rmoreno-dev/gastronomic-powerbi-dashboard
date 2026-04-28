# Medidas DAX — Dashboard Cafetería Artesanal Japonesa

## Medidas de ingresos

### Ingresos Totales
```dax
Ingresos Totales = SUM(transactions_clean[total])
```
**Uso:** KPI principal en todas las páginas.

---

### Ingresos Items
```dax
Ingresos Items = SUM(items_clean[revenue])
```
**Uso:** Análisis por producto y sección.

---

### Ingresos Mes Anterior
```dax
Ingresos Mes Anterior = 
CALCULATE(
    [Ingresos Totales],
    PREVIOUSMONTH(DimFecha[Date])
)
```
**Uso:** Comparativo mensual.

---

### Variación Mes %
```dax
Variación Mes % = 
DIVIDE(
    [Ingresos Totales] - [Ingresos Mes Anterior],
    [Ingresos Mes Anterior]
)
```
**Uso:** Tendencia de crecimiento mensual.

---

### Ingresos Diario Promedio
```dax
Ingresos Diario Promedio = 
DIVIDE(
    [Ingresos Totales],
    DISTINCTCOUNT(transactions_clean[fecha])
)
```
**Uso:** Planificación operacional diaria.

---

## Medidas de transacciones

### Total Transacciones
```dax
Total Transacciones = COUNTROWS(transactions_clean)
```

---

### Ticket Promedio
```dax
Ticket Promedio = 
DIVIDE(
    SUM(transactions_clean[total]),
    COUNTROWS(transactions_clean)
)
```

---

### Ticket Fin de Semana
```dax
Ticket Fin de Semana = 
CALCULATE(
    [Ticket Promedio],
    transactions_clean[is_weekend] = TRUE()
)
```

---

### Ticket Día de Semana
```dax
Ticket Día de Semana = 
CALCULATE(
    [Ticket Promedio],
    transactions_clean[is_weekend] = FALSE()
)
```

---

### Total Días Operación
```dax
Total Días Operación = 
DISTINCTCOUNT(transactions_clean[fecha])
```

---

### Promedio Transacciones Diarias
```dax
Promedio Transacciones Diarias = 
DIVIDE(
    [Total Transacciones],
    [Total Días Operación]
)
```

---

### Unidades Vendidas
```dax
Unidades Vendidas = COUNTROWS(items_clean)
```

---

## Medidas de Ingeniería de Menú

### Productos Estrella
```dax
Productos Estrella = 
CALCULATE(
    COUNTROWS(product_summary),
    product_summary[clasificacion_menu] = "Estrella"
)
```

---

### Productos Caballo
```dax
Productos Caballo = 
CALCULATE(
    COUNTROWS(product_summary),
    product_summary[clasificacion_menu] = "Caballo de Trabajo"
)
```

---

### Productos Interrogante
```dax
Productos Interrogante = 
CALCULATE(
    COUNTROWS(product_summary),
    product_summary[clasificacion_menu] = "Interrogante"
)
```

---

### Productos Perro
```dax
Productos Perro = 
CALCULATE(
    COUNTROWS(product_summary),
    product_summary[clasificacion_menu] = "Perro"
)
```