document.getElementById('calculator-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const n = parseInt(document.getElementById('n').value);
    const p = parseFloat(document.getElementById('p').value);
    const k = parseInt(document.getElementById('k').value);

    const requestData = { n, p, k };

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const responseData = await response.json();

        if (responseData.success) {
            const { step_by_step, distribution } = responseData.data;

            document.getElementById('result').innerHTML = `
                <p>Langkah-Langkah Perhitungan:</p>
                <ol>
                    ${step_by_step.steps.map(step => `<li>${step}</li>`).join('')}
                </ol>
            `;

            const labels = distribution.map(item => item.k);
            const probabilities = distribution.map(item => item.probability);

            const ctx = document.getElementById('probability-chart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Probabilitas',
                        data: probabilities,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true },
                        x: { title: { display: true, text: 'Jumlah Keberhasilan (k)' } }
                    }
                }
            });
        } else {
            document.getElementById('result').innerHTML = `<p>Error: ${responseData.error}</p>`;
        }
    } catch (error) {
        document.getElementById('result').innerText = `Error: ${error.message}`;
    }
});
