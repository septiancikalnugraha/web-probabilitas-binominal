from flask import Flask, jsonify, render_template, request
from math import comb

app = Flask(__name__)

# Fungsi untuk menghitung probabilitas binomial
def binomial_probability(n, p, k):
    kombinasi = comb(n, k)
    peluang_berhasil = p ** k
    peluang_gagal = (1 - p) ** (n - k)
    probabilitas = kombinasi * peluang_berhasil * peluang_gagal
    return {
        "kombinasi": kombinasi,
        "peluang_berhasil": peluang_berhasil,
        "peluang_gagal": peluang_gagal,
        "probabilitas": probabilitas,
        "steps": [
            f"Kombinasi (C(n, k)) = C({n}, {k}) = {kombinasi}",
            f"Peluang Berhasil (p^k) = {p} ^ {k} = {peluang_berhasil:.6f}",
            f"Peluang Gagal ((1-p)^(n-k)) = (1-{p}) ^ ({n}-{k}) = {peluang_gagal:.6f}",
            f"Probabilitas Total = C(n, k) * p^k * (1-p)^(n-k) = {kombinasi} * {peluang_berhasil:.6f} * {peluang_gagal:.6f} = {probabilitas:.6f}"
        ]
    }

# Rute untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Rute untuk menghitung probabilitas
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        n = int(data.get('n'))
        p = float(data.get('p'))
        k = int(data.get('k'))

        # Validasi
        if not (0 <= p <= 1):
            return jsonify({"success": False, "error": "Probability p must be between 0 and 1"}), 400
        if not (0 <= k <= n):
            return jsonify({"success": False, "error": "k must be between 0 and n"}), 400

        # Hitung probabilitas spesifik
        step_by_step = binomial_probability(n, p, k)

        # Hitung distribusi probabilitas
        distribution = [
            {
                "k": i,
                "probability": binomial_probability(n, p, i)["probabilitas"]
            }
            for i in range(n + 1)
        ]

        return jsonify({
            "success": True,
            "data": {
                "n": n,
                "p": p,
                "k": k,
                "step_by_step": step_by_step,
                "distribution": distribution
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
