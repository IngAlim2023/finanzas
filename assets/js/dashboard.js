let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] },
        { orderable: false, targets: [1, 2] },
        { searchable: false, targets: [1, 2, 3, 4] }
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
        const response = await fetch("http://127.0.0.1:8000/datos/");
        const data = await response.json();
        let content = ``;
        data.base_datos.forEach((base_datos, index) => {
            content += `
            <tr>
                <td>${index + 1} </td>
                <td>${base_datos.id} </td>
                <td>${base_datos.user_id} </td>
                <td>${base_datos.movimiento_id} </td>
                <td>${base_datos.motivos_id} </td>
                <td>${base_datos.descripcion} </td>
                <td>${base_datos.monto} </td>
                <td>${base_datos.fecha} </td>
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
