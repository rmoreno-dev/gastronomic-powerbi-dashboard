# fix_precio_integer.py
import pandas as pd

PATH = r"C:\Users\Usuario\gastronomic-powerbi-dashboard\data\product_summary.csv"

df = pd.read_csv(PATH, encoding='utf-8-sig')

print("ANTES:")
print(df['precio_promedio'].head(5).to_string())

# Redondear a entero — precios CLP no tienen centavos
df['precio_promedio'] = df['precio_promedio'].round(0).astype(int)
df['menu_mix_pct']    = df['menu_mix_pct'].round(3)

print("\nDESPUES:")
print(df['precio_promedio'].head(5).to_string())
print(f"\nMin: {df['precio_promedio'].min()} | Max: {df['precio_promedio'].max()}")

df.to_csv(PATH, index=False, encoding='utf-8-sig')
print("\n✅ CSV guardado con precios enteros")