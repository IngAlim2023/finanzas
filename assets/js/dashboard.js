let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [1] },
        { searchable: false, targets: [5, 6] }
    ],
    pageLength: 15,
    destroy: true

};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listaBase();

    dataTable = $("#datos").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listaBase = async () => {
    try {
        const response = await fetch("/datos/");
        const data = await response.json();
        let content = ``;
        data.base_datos.forEach((base_datos, index) => {
            content += `
            <tr>
                <td>${index + 1} </td>
                <td>${base_datos.id} </td>
                <td>${base_datos.descripcion} </td>
                <td>${base_datos.monto} </td>
                <td>${base_datos.fecha} </td>
                <td>${base_datos.modified} </td>
                <td>${base_datos.created} </td>
            </tr>
          `;
        });
        tableBody_datos.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
}
window.addEventListener('load', async()=>{
    await initDataTable();
});

const fetchData = async (url) => {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
};

const initChart = async (chartId, dataUrl) => {
    const myChart = echarts.init(document.getElementById(chartId));
    myChart.setOption(await fetchData(dataUrl));
    myChart.resize();
};

window.addEventListener("load", async () => {
    await initChart("chart", "/get_chart/");
    await initChart("chartdos", "/get_chart_dos/");
    await initChart('charttres', "/get_chart_tres/");
});
