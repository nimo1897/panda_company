 // JavaScript for Chart.js
 const totalClientsChart = new Chart(document.getElementById("totalClientsChart"), {
    type: 'bar',
    data: {
        labels: ['Client 1', 'Client 2', 'Client 3', 'Client 4'],
        datasets: [{
            label: 'Total Clients',
            data: [10, 15, 30, 20],
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

const totalBalanceChart = new Chart(document.getElementById("totalBalanceChart"), {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April'],
        datasets: [{
            label: 'Total Balance',
            data: [1000, 1200, 1500, 1300],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false,
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
    }
});

const accountBalanceChart = new Chart(document.getElementById("accountBalanceChart"), {
    type: 'pie',
    data: {
        labels: ['Balance A', 'Balance B', 'Balance C'],
        datasets: [{
            label: 'Account Balance',
            data: [300, 500, 200],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
    },
    options: {
        responsive: true,
    }
});

const profitChart = new Chart(document.getElementById("profitChart"), {
    type: 'doughnut',
    data: {
        labels: ['Profit A', 'Profit B', 'Profit C'],
        datasets: [{
            label: 'Profit',
            data: [500, 700, 1000],
            backgroundColor: ['#FF5733', '#C70039', '#900C3F']
        }]
    },
    options: {
        responsive: true,
    }
});




