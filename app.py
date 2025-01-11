from flask import Flask, jsonify, render_template, request
from math import comb

app = Flask(__name__)

# Fungsi untuk menghitung PMF
def binomial_pmf(n, p, k):
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
            f"Peluang Berhasil (p^k) = {p}^{k} = {peluang_berhasil:.6f}",
            f"Peluang Gagal ((1-p)^(n-k)) = (1-{p})^{n-k} = {peluang_gagal:.6f}",
            f"Probabilitas (PMF) = C(n, k) * p^k * (1-p)^(n-k) = {kombinasi} * {peluang_berhasil:.6f} * {peluang_gagal:.6f} = {probabilitas:.6f}"
        ]
    }

# Fungsi untuk menghitung CDF
def binomial_cdf(n, p, k):
    cdf = 0
    steps = []
    for i in range(k + 1):
        pmf = binomial_pmf(n, p, i)["probabilitas"]
        cdf += pmf
        steps.append(f"CDF hingga k={i}: {cdf:.6f}")
    return {"cdf": cdf, "steps": steps}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        n = int(data.get('n'))
        p = float(data.get('p'))
        k = int(data.get('k'))

        # Validasi input
        if not (0 <= p <= 1):
            return jsonify({"success": False, "error": "Probabilitas (p) harus antara 0 dan 1"}), 400
        if not (0 <= k <= n):
            return jsonify({"success": False, "error": "k harus antara 0 dan n"}), 400

        # Hitung PMF dan CDF
        pmf_result = binomial_pmf(n, p, k)
        cdf_result = binomial_cdf(n, p, k)

        print("PMF Result:", pmf_result)  # Debug log
        print("CDF Result:", cdf_result)  # Debug log

        distribution = [
            {
                "k": i,
                "pmf": binomial_pmf(n, p, i)["probabilitas"],
                "cdf": binomial_cdf(n, p, i)["cdf"]
            }
            for i in range(n + 1)
        ]

        return jsonify({
            "success": True,
            "data": {
                "n": n,
                "p": p,
                "k": k,
                "pmf": pmf_result,
                "cdf": cdf_result,
                "distribution": distribution
            }
        })
    except Exception as e:
        print("Error:", e)  # Debug log
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
