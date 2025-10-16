async function loadData() {
  const res = await fetch("/api/get_data");
  const data = await res.json();

  const labels = data.map(row => row.timestamp).reverse();
  const suhu = data.map(row => row.temperature).reverse();
  const kelembaban = data.map(row => row.humidity).reverse();
  const level = data.map(row => row.level_air).reverse();

  const ctx1 = document.getElementById("chartSuhu");
  const ctx2 = document.getElementById("chartKelembaban");
  const ctx3 = document.getElementById("chartLevel");

  new Chart(ctx1, {
    type: "line",
    data: { labels, datasets: [{ label: "Suhu (°C)", data: suhu, borderWidth: 2 }] }
  });

  new Chart(ctx2, {
    type: "line",
    data: { labels, datasets: [{ label: "Kelembaban (%)", data: kelembaban, borderWidth: 2 }] }
  });

  new Chart(ctx3, {
    type: "line",
    data: { labels, datasets: [{ label: "Level Air (cm)", data: level, borderWidth: 2 }] }
  });
}

loadData();
setInterval(loadData, 10000); // refresh tiap 10 detik
