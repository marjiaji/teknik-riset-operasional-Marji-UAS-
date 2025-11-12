from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

# Membuat model optimasi
model = LpProblem("Optimalisasi_Distribusi_Barang", LpMinimize)

# Data biaya pengiriman (Rp/unit)
biaya = {
    ('G1', 'T1'): 6, ('G1', 'T2'): 8, ('G1', 'T3'): 10,
    ('G2', 'T1'): 7, ('G2', 'T2'): 11, ('G2', 'T3'): 11,
    ('G3', 'T1'): 4, ('G3', 'T2'): 5, ('G3', 'T3'): 12
}

# Kapasitas tiap gudang
kapasitas = {'G1': 100, 'G2': 120, 'G3': 80}

# Permintaan tiap toko
permintaan = {'T1': 80, 'T2': 70, 'T3': 150}

# Variabel keputusan (jumlah barang dikirim)
x = LpVariable.dicts("x", biaya, lowBound=0)

# Fungsi tujuan (minimasi total biaya)
model += lpSum(biaya[i, j] * x[i, j] for (i, j) in biaya)

# Kendala kapasitas gudang
for i in kapasitas:
    model += lpSum(x[i, j] for j in permintaan) <= kapasitas[i], f"Kapasitas_{i}"

# Kendala permintaan toko
for j in permintaan:
    model += lpSum(x[i, j] for i in kapasitas) == permintaan[j], f"Permintaan_{j}"

# Jalankan optimasi
model.solve()

# Hasil
print("=== HASIL DISTRIBUSI OPTIMAL ===")
for (i, j) in biaya:
    print(f"{i} ke {j} = {x[i, j].value()} unit")
print(f"\nTotal Biaya Minimum = Rp {value(model.objective):,.0f}")
