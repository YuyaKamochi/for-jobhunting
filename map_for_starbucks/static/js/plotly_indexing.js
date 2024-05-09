function intensity(data,maxY) {
  // Divide y value by the maximum y value
  data.y = data.y.map(function(value) {
      return (value / maxY) * 100;
  });

  return data;
}

function offset(data,offset_sum) {
  // Divide y value by the maximum y value
  data.y = data.y.map(function(value) {
      return value + offset_sum;
  });

  return data;
}

function processFile(file) {
  return new Promise(function (resolve) {
      const reader = new FileReader();
      let x = [];
      let y = [];

      reader.onload = function (e) {
          const contents = e.target.result;
          const lines = contents.split('\n');

          for (let i = 0; i < lines.length; i++) {
              let line = lines[i].trim();
              if (line !== '' && !isNaN(line.charAt(0))) {
                  let values = line.split('\t');
                  x.push(values[0]);
                  y.push(parseFloat(values[1])); // Convert y values to float
              }
          }

          // Check if the file name ends with "_peak"
          const isPeakFile = file.name.endsWith('_peak.txt');

          // Resolve the promise with the data, file name, and peak flag
          resolve({ x: x, y: y, type: 'scatter', fileName: file.name, isPeakFile: isPeakFile });
      };

      reader.readAsText(file);
  });
}

function readFile(files, tableData) {
  let promises = [];

  for (let j = 0; j < files.length; j++) {
      promises.push(processFile(files[j]));
  }

  // Wait for all promises to resolve
  Promise.all(promises).then(async function (data_set) {
      const intensityCheckbox = document.getElementById('intensityCheckbox');
      const offsetCheckbox = document.getElementById('offsetCheckbox');
      let intensityData = [];
      let offsetData = [];
      let offset_sum = 0;

      for (let i = 0; i < data_set.length; i++) {
          let data = Object.assign({}, data_set[i]);

          // Check if the file is a "_peak" file and has data
          if (data.isPeakFile && data.x.length > 0 && !document.getElementById('isReadingPeakList').checked) {
              // Assuming the X values in the "_peak" file should be added to the indexingTable
              let table = document.getElementById('indexingTable').getElementsByTagName('tbody')[0];
              for (let i = 0; i < data.x.length; i++) {
                  let newRow = table.insertRow(table.rows.length);
                  let cell0 = newRow.insertCell(0);
                  cell0.contentEditable = true;
                  cell0.innerText = data.x[i];
                  let cell1 = newRow.insertCell(1);
                  cell1.contentEditable = true;
                  cell1.innerText = data.y[i];
                  newRow.insertCell(2).contentEditable = true;
                  newRow.insertCell(3).contentEditable = true;
                  newRow.insertCell(4).contentEditable = true;
              }
          }

          // Skip plotting if it's a "_peak" file
          if (data.isPeakFile) {
              continue;
          }

          if (intensityCheckbox.checked) {
              intensityData.push(intensity(data, Math.max(...data.y)));
          } else {
              intensityData.push(data);
          }

          if (offsetCheckbox.checked) {
              offsetData.push(offset(Object.assign({}, intensityData[i]), offset_sum));
          } else {
              offsetData.push(intensityData[i]);
          }

          offset_sum += Math.max(...intensityData[i].y)/2;

      }
      
      tableData = fillTableData(tableData, offsetData);
      document.getElementById('isReadingPeakList').checked = true;

      // Call plotData function after reading all files
      plotData(offsetData, intensityData, tableData);
  });
}


function plotData(data,disp_data,indexingData) {
  const offset = document.getElementById('offsetCheckbox').checked;
  const intensity = document.getElementById('intensityCheckbox').checked;

  const font_size = 15;
  let annotations = [];

  for (let i = 0; i < indexingData.length; i++) {
      if (indexingData[i][2] === "") {continue;}
      annotations.push({
              x: Number(indexingData[i][0]), // x座標
              y: Number(indexingData[i][1])+Number(indexingData[i][5]), // y座標
              xref: 'x', // x座標の基準（'x'または'paper'）
              yref: 'y', // y座標の基準（'y'または'paper'）
              text: indexingData[i][2], // 表示するテキスト
              showarrow: false, // 矢印を表示するか
              textangle: 0,
              font:{
                  size:indexingData[i][4],
              }
      });
  }

  for (let i = 0; i < indexingData.length; i++) {
      if (indexingData[i][3] === "") {continue;}
      annotations.push({
              x: Number(indexingData[i][0]), // x座標
              y: Number(indexingData[i][1])+Number(indexingData[i][5]), // y座標
              xref: 'x', // x座標の基準（'x'または'paper'）
              yref: 'y', // y座標の基準（'y'または'paper'）
              text: indexingData[i][3], // 表示するテキスト
              showarrow: false, // 矢印を表示するか
              textangle: 270,
              font:{
                  size:indexingData[i][4],
              }
      });
  }

  const layout = {
      aspectratio: 1,
      xaxis: {
          title: {
              text:'2θ/deg.(CuKα)',
              standoff: 5,
              family: 'Times New Roman'},
          font:{
              family: 'Times New Roman',
          },
          showline: true,
          zeroline: false,
          tick0: 20,
          dtick: 20,
          mirror: true,
          showgrid: false,
      },
      yaxis: {
          title:{
              text:'Intensity/arb.unit',
              family: 'Arial',
          },
          showline: true,
          zeroline: false,
          rangemode: 'tozero',
          showticklabels: !intensity,
          mirror: true,
          showgrid: false,
      },
      annotations:annotations,
      title:{
          text: document.getElementById('Title').value,
          y: '0.05',
      },
      width: 1000,
      height: 600,
  };

  // Create an array to hold plot traces
  let traces = [];

  // Loop through each data object and create a trace for the plot
  for (let i = 0; i < data.length; i++) {
      let trace = {
          x: data[i].x,
          y: data[i].y,
          type: 'scatter',
          name: data[i].fileName,
          customdata: disp_data[i].y,
          hovertemplate: 'x: <b>%{x}</b><br>' +
                         'y: %{customdata:.2f}<br>',
      };
      traces.push(trace);
  }

  // console.log(indexingData)
  Plotly.newPlot('plot', traces, layout); // Display the plot in the 'plot' div
  let clicked = false;
  document.getElementById('plot').on('plotly_click', function(data){
      if (clicked) {
          clicked = false;
          return;
      } else {
          clicked = true;
      }

      setTimeout(function () {
          // ダブルクリックによりclickedフラグがリセットされていない
          //     -> シングルクリックだった
          if (clicked) {
              let x = data.points[0].x;
              let y = data.points[0].y;
              let row_data = [x,y,"","","",""]
          
              let table = document.getElementById('indexingTable')
              if (table.rows[1].cells[0].innerText == "" && table.rows[1].cells[1].innerText == ""){table.deleteRow(1);}
              
              let newRow = table.insertRow(table.rows.length);
  
              for (let i = 0; i < table.rows[0].cells.length; i++) {
                  let cell = newRow.insertCell(i);
                  cell.contentEditable = true;
                  cell.innerText = row_data[i];
              }
          }
  
          clicked = false;
      }, 200);
  });
}

function readTableData(table){
  let data = [];
  for (let i = 1; i < table.rows.length; i++) {
      let rowData = [];
      for (let j = 0; j < table.rows[i].cells.length; j++) {
          rowData.push(table.rows[i].cells[j].innerText);
      }
      data.push(rowData);
  }

  return data;
}

function fillTableData(tableData, offsetData) {
  console.log(tableData)
  for (let i = 0; i < tableData.length; i++) {
      if (tableData[i][0] === "") {tableData.splice(i,1); continue;}
      if (tableData[i][1] === "") {
          // If Y value is empty, find matching X value in offsetData and fill Y value
          let matchingIndex = offsetData[offsetData.length - 1].x.indexOf(tableData[i][0]);
          if (matchingIndex !== -1) {
              tableData[i][1] = offsetData[offsetData.length - 1].y[matchingIndex].toString();
          }
      }

      if (tableData[i][2] === "" && tableData[i][3]==="") {tableData[i][2] = "▽";}
      if (tableData[i][4] === "") {tableData[i][4] = "15";}
      if (tableData[i][5] === "" || tableData[i][5] == "\n") {tableData[i][5] = "3";}
  }

  return tableData;
}


document.getElementById('fileForm').addEventListener('submit', function(event) {
  event.preventDefault();

  let table = document.getElementById('indexingTable');
  let tableData = readTableData(table);

  let fileInput = document.getElementById('file-form-label');
  let files = fileInput.files;
  readFile(files,tableData);
});

document.getElementById('addRowBtn').addEventListener('click', function (event) {
  event.preventDefault();
  let table = document.getElementById('indexingTable').getElementsByTagName('tbody')[0];
  let newRow = table.insertRow(table.rows.length);

  for (let i = 0; i < table.rows[0].cells.length; i++) {
      let cell = newRow.insertCell(i);
      cell.contentEditable = true;
  }
});

document.getElementById('exportBtn').addEventListener('click', function(event) {
  event.preventDefault();
  const table = document.getElementById('indexingTable');
  const rows = table.getElementsByTagName('tr');
  const graphTitle = document.getElementById('Title').value;
  let csv = ['\uFEFF']; // UTF-8のBOMを追加

  for (let i = 0; i < rows.length; i++) {
      let cells = i === 0 ? rows[i].getElementsByTagName('th') : rows[i].getElementsByTagName('td');
      let rowData = [];

      for (let j = 0; j < cells.length; j++) {
          rowData.push(cells[j].innerText);
      }

      csv.push(rowData.join(','));
  }

  let csvData = new Blob([csv.join('\n')], { type: 'text/csv;charset=utf-8;' });
  let url = window.URL.createObjectURL(csvData);
  let link = document.createElement('a');
  link.href = url;
  link.download = graphTitle + '_indexing.csv';
  link.click();
});

document.getElementById('importBtn').addEventListener('change', function(event) {
    const file = event.target.files[0];
    let reader = new FileReader();

    reader.onload = function(e) {
        const contents = e.target.result;
        let lines = contents.split('\n');
        const table = document.getElementById('indexingTable');

        // Clear table data
        while (table.rows.length > 1) {
            table.deleteRow(1);
        }

        // CSVデータをテーブルに反映
        for (let i = 0; i < lines.length; i++) { // 一行目を読み飛ばす
            let cells = lines[i].split(',');
            if (cells[0] === "" || cells[0] == "X") {continue;}
            let row = table.insertRow(-1);
            for (let j = 0; j < cells.length; j++) {
                let cell = row.insertCell(-1);
                cell.contentEditable = true;
                cell.innerText = cells[j];
            }
        }
    };

    reader.readAsText(file, 'UTF-8');
});

document.getElementById("file-form-label").addEventListener("change", function(e){
    e.target.nextSibling.nodeValue = e.target.files.length ? e.target.files[0].name.toString() + "他" + (e.target.files.length-1) : "txtファイルを選択";
});

