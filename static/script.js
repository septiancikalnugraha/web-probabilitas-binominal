
let pmfChart;
let cdfChart;

document.getElementById('calculator-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const n = parseInt(document.getElementById('n').value);
    const p = parseFloat(document.getElementById('p').value);
    const k = parseInt(document.getElementById('k').value);

    if (isNaN(n) || isNaN(p) || isNaN(k)) {
        document.getElementById('result').innerHTML = `<p>Error: Pastikan semua input diisi dengan benar.</p>`;
        return;
    }

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ n, p, k })
        });

        const data = await response.json();

        if (data.success) {
            const { pmf, cdf, distribution } = data.data;

            const pmfSteps = pmf.steps || [];
            const cdfSteps = cdf.steps || [];

            document.getElementById('result').innerHTML = `
                <h3>Langkah-Langkah Penyelesaian:</h3>
                <p><strong>PMF (P(X = k)):</strong></p>
                <ul>${pmfSteps.map(step => `<li>${step}</li>`).join('')}</ul>
                <p><strong>CDF (P(X ≤ k)):</strong></p>
                <ul>${cdfSteps.map(step => `<li>${step}</li>`).join('')}</ul>
            `;

            const labels = distribution.map((item) => item.k);
            const pmfData = distribution.map((item) => item.pmf);
            const cdfData = distribution.map((item) => item.cdf);

            if (pmfChart) pmfChart.destroy();
            const pmfCtx = document.getElementById('pmf-chart').getContext('2d');
            pmfChart = new Chart(pmfCtx, {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'PMF (P(X = k))',
                        data: pmfData,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { title: { display: true, text: 'Jumlah Keberhasilan (k)' } },
                        y: { title: { display: true, text: 'Probabilitas' } }
                    }
                }
            });

            if (cdfChart) cdfChart.destroy();
            const cdfCtx = document.getElementById('cdf-chart').getContext('2d');
            cdfChart = new Chart(cdfCtx, {
                type: 'line',
                data: {
                    labels,
                    datasets: [{
                        label: 'CDF (P(X ≤ k))',
                        data: cdfData,
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { title: { display: true, text: 'Jumlah Keberhasilan (k)' } },
                        y: { title: { display: true, text: 'Kumulatif Probabilitas' } }
                    }
                }
            });
        } else {
            document.getElementById('result').innerHTML = `<p>Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `<p>Error: ${error.message}</p>`;
    }
});

document.getElementById('reset-button').addEventListener('click', () => {
    document.getElementById('n').value = '';
    document.getElementById('p').value = '';
    document.getElementById('k').value = '';
    document.getElementById('result').innerHTML = '';

    if (pmfChart) pmfChart.destroy();
    if (cdfChart) cdfChart.destroy();
});
