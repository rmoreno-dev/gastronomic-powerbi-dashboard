# fix_csv_encoding.py
# Propósito: Corregir encoding UTF-8 y verificar tipos numéricos en product_summary.csv
# Autor: Rodolfo Moreno | github.com/rmoreno-dev

import pandas as pd
import os

# ─── RUTAS ────────────────────────────────────────────────────────────────────
INPUT_PATH  = r"C:\Users\Usuario\gastronomic-powerbi-dashboard\data\product_summary.csv"
OUTPUT_PATH = r"C:\Users\Usuario\gastronomic-powerbi-dashboard\data\product_summary.csv"
BACKUP_PATH = r"C:\Users\Usuario\gastronomic-powerbi-dashboard\data\product_summary_backup.csv"

# ─── PASO 1: BACKUP ────────────────────────────────────────────────────────────
import shutil
shutil.copy2(INPUT_PATH, BACKUP_PATH)
print(f"✅ Backup creado en: {BACKUP_PATH}")

# ─── PASO 2: LEER CON ENCODING CORRECTO ───────────────────────────────────────
# Intentar múltiples encodings hasta que uno funcione
encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
df = None

for enc in encodings_to_try:
    try:
        df = pd.read_csv(INPUT_PATH, encoding=enc)
        # Verificar que los caracteres especiales se ven bien
        sample = df['producto'].iloc[0]
        if 'Ã' not in sample and 'â' not in sample:
            print(f"✅ Encoding correcto encontrado: {enc}")
            break
        else:
            print(f"❌ Encoding {enc} no funcionó (todavía hay caracteres rotos)")
            df = None
    except Exception as e:
        print(f"❌ Error con encoding {enc}: {e}")
        df = None

if df is None:
    # Forzar latin-1 que siempre lee sin error
    df = pd.read_csv(INPUT_PATH, encoding='latin-1')
    print("⚠️  Usando latin-1 como fallback")

# ─── PASO 3: DIAGNÓSTICO ANTES DE CORREGIR ────────────────────────────────────
print("\n=== DIAGNÓSTICO: TIPOS DE DATOS ACTUALES ===")
print(df.dtypes)
print(f"\nShape: {df.shape[0]} filas × {df.shape[1]} columnas")

print("\n=== MUESTRA DE DATOS (3 filas) ===")
print(df[['producto', 'seccion', 'precio_promedio', 'clasificacion_menu']].head(3).to_string())

# ─── PASO 4: FORZAR TIPOS NUMÉRICOS CORRECTOS ─────────────────────────────────
# Estas columnas DEBEN ser numéricas — las convertimos explícitamente
numeric_columns = {
    'cantidad'        : 'int64',
    'ingresos_totales': 'int64',
    'precio_promedio' : 'float64',   # ← LA COLUMNA CRÍTICA
    'n_transacciones' : 'int64',
    'menu_mix_pct'    : 'float64',
}

print("\n=== CORRIGIENDO TIPOS DE DATOS ===")
for col, dtype in numeric_columns.items():
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if dtype == 'int64':
            df[col] = df[col].fillna(0).astype('int64')
        print(f"  ✅ {col} → {dtype} | Min: {df[col].min():,.2f} | Max: {df[col].max():,.2f}")
    else:
        print(f"  ⚠️  Columna '{col}' no encontrada en el CSV")

# ─── PASO 5: VERIFICAR RANGO DE PRECIOS ───────────────────────────────────────
print("\n=== VERIFICACIÓN RANGO DE PRECIOS ===")
print(f"  precio_promedio mínimo : {df['precio_promedio'].min():>12,.2f} CLP")
print(f"  precio_promedio máximo : {df['precio_promedio'].max():>12,.2f} CLP")
print(f"  precio_promedio promedio: {df['precio_promedio'].mean():>12,.2f} CLP")
print(f"  Valores nulos          : {df['precio_promedio'].isna().sum()}")

# ─── PASO 6: VERIFICAR PRODUCTOS Y SECCIONES ──────────────────────────────────
print("\n=== VERIFICACIÓN TEXTO (primeros 5 productos) ===")
for i, row in df.head(5).iterrows():
    print(f"  {row['producto']} | {row['seccion']}")

# ─── PASO 7: GUARDAR CON UTF-8-SIG (BOM) — formato que Power BI lee perfecto ──
df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig', float_format='%.4f')
print(f"\n✅ Archivo guardado con UTF-8 BOM en: {OUTPUT_PATH}")

# ─── PASO 8: VERIFICACIÓN FINAL ───────────────────────────────────────────────
df_check = pd.read_csv(OUTPUT_PATH, encoding='utf-8-sig')
print("\n=== VERIFICACIÓN FINAL DEL ARCHIVO GUARDADO ===")
print(df_check.dtypes)
print(f"\nPrimer producto: {df_check['producto'].iloc[0]}")
print(f"Primer precio  : {df_check['precio_promedio'].iloc[0]}")
print("\n🎉 Fix de encoding completado exitosamente")