const voegRijToe = function (data, type) {
    console.log("data:", data);
    let rijHTML = ``;
    let tableBody;
  
    if (type === 'inv') {
      tableBody = document.querySelector('.myTable');
      if (data[3] < data[4]) {
        rijHTML += `<tr class="below-min">`;
        for (let i of data) {
            if (i == data[3]) {
                rijHTML += `<td class="below-min__quantity">${i}</td>`;
              } 
            else {
                rijHTML += `<td>${i}</td>`;
              }
        }
        rijHTML += `</tr>`;
      } else {
        rijHTML = `<tr>`;
        for (let i of data) {
          rijHTML += `<td>${i}</td>`;
        }
        rijHTML += `</tr>`;
      }
    } 
    
    else if (type === 'his1') {
      tableBody = document.querySelector('.myTable1');
      rijHTML += `<tr>`;
      for (let i of data) {
        rijHTML += `<td>${i}</td>`;
      }
      rijHTML += `</tr>`;
    } 
    
    else if (type === 'his2') {
      tableBody = document.querySelector('.myTable2');
      rijHTML = `<tr>`;
      for (let i of data) {
        rijHTML += `<td>${i}</td>`;
      }
      rijHTML += `</tr>`;
    } 
    
    else if (type === 'his3') {
      tableBody = document.querySelector('.myTable3');
      rijHTML = `<tr>`;
      for (let i of data) {
        rijHTML += `<td>${i}</td>`;
      }
      rijHTML += `</tr>`;
    } 
    
    else if (type === 'prodhis') {
      tableBody = document.querySelector('.myTable');
      rijHTML = data[3] < 0 ? `<tr class="row-negative">` : `<tr class="row-positive">`;
      for (let i of data) {
        rijHTML += (i == data[3]) ? `<td class="${data[3] < 0 ? 'row-negative__number' : 'row-positive__number'}">${i}</td>` : `<td>${i}</td>`;
      }
      rijHTML += `</tr>`;
    } else if (type === 'cart') {
      tableBody = document.querySelector('.myTable');
      rijHTML = `<tr>`;
      for (let i of data) {
        rijHTML += `<td>${i}</td>`;
      }
      rijHTML += `</tr>`;
    }
  
    if (tableBody) {
      tableBody.insertAdjacentHTML('beforeend', rijHTML);
    }
  };
  