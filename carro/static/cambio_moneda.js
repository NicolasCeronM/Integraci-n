document.addEventListener('DOMContentLoaded', function() {
    // Obtener tasas de cambio cuando se carga la página
    fetch('/get_exchange_rates/')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('currency-select');
            const rates = data.conversion_rates;
            
            // Llenar el select con las opciones de monedas
            for (let currency in rates) {
                let option = document.createElement('option');
                option.value = rates[currency];
                option.text = currency;
                select.appendChild(option);
            }
        });

    // Convertir el importe total cuando se selecciona una moneda
    document.getElementById('currency-select').addEventListener('change', function() {
        const rate = parseFloat(this.value);
        const total = parseFloat(document.getElementById('importe-total').dataset.value);
        const convertedTotal = (total * rate).toFixed(2);
        document.getElementById('converted-importe-total').textContent = convertedTotal;
    });
});