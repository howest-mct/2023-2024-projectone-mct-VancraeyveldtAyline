const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

const listenToUI = function () {
  loadMoreBtn = document.querySelector('load-more-btn');
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  // Voeg hier meer socket event listeners toe, indien nodig
};

const voegRijToe = function (data, type) {
  let rijHTML = ``;
  if (type == 'inv') {
    const tableBody = document.querySelector('.myTable');
    if (data[3] < data[4]) {
      rijHTML += `<tr class="below-min">`;
      for (let i of data) {
        if (i == data[3]) {
          rijHTML += `<td class="below-min__quantity">${i}</td>`;
        } else {
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
    tableBody.insertAdjacentHTML('beforeend', rijHTML);
  }
  if (type == 'his1') {
    const tableBody = document.querySelector('.myTable1');
    rijHTML = `<tr>`;
      for (let i of data) {
        rijHTML += `<td>${i}</td>`;
      }
    rijHTML += `</tr>`;
    tableBody.insertAdjacentHTML('beforeend', rijHTML);
  }
  if (type == 'his2') {
    const tableBody = document.querySelector('.myTable2');
    rijHTML = `<tr>`;
      for (let i of data) {
        rijHTML += `<td>${i}</td>`;
      }
    rijHTML += `</tr>`;
    tableBody.insertAdjacentHTML('beforeend', rijHTML);
  }
  if (type == 'his3') {
    const tableBody = document.querySelector('.myTable3');
    rijHTML = `<tr>`;
      for (let i of data) {
        rijHTML += `<td>${i}</td>`;
      }
    rijHTML += `</tr>`;
    tableBody.insertAdjacentHTML('beforeend', rijHTML);
  }
  if (type == 'prodhis') {
    const tableBody = document.querySelector('.myTable');
    if (data[3] < 0) {
      rijHTML = `<tr class="row-negative">`;
      for (let i of data) {
        if (i == data[3]) {
          rijHTML += `<td class="row-negative__number">${i}</td>`;
        } else {
          rijHTML += `<td>${i}</td>`;
        }
      }
    }
    else {
      rijHTML = `<tr class="row-positive">`;
      for (let i of data) {
        if (i == data[3]) {
          rijHTML += `<td class="row-positive__number">${i}</td>`;
        } else {
          rijHTML += `<td>${i}</td>`;
        }
      }
    }


    
      
    rijHTML += `</tr>`;
    tableBody.insertAdjacentHTML('beforeend', rijHTML);
  }
};

const showInventory = function (inventory) {
  try {
    console.log('Inventory ontvangen:', inventory);
    if (inventory && inventory.inventory) {
      for (let product of inventory.inventory) {
        let data = [
          product.product_naam,
          product.product_type,
          product['max(tijdstip)'],
          product.totaal_aantal,
          product.minimum_waarde,
        ];
        voegRijToe(data, 'inv');
      }
    } else {
      console.error('Ongeldige records data ontvangen:', inventory);
    }
  } catch (e) {
    console.log(e);
  }
};

const showSensorHistoryBarcode = function (history) {
  try {
    console.log('History ontvangen:', history);
    if (history && history.history) {
      for (let record of history.history) {
        let data = [
          record.waarde,
          record.tijdstip_waarde,
          record.opmerking
        ];
        voegRijToe(data, 'his1');
      }
    } else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
}
const showSensorHistoryLight = function (history) {
  try {
    console.log('History ontvangen:', history);
    if (history && history.history) {
      for (let record of history.history) {
        let data = [
          record.waarde,
          record.tijdstip_waarde,
          record.opmerking
        ];
        voegRijToe(data, 'his2');
      }
    } else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
}
const showSensorHistoryJoy = function (history) {
  try {
    console.log('History ontvangen:', history);
    if (history && history.history) {
      for (let record of history.history) {
        let data = [
          record.waarde,
          record.tijdstip_waarde,
          record.opmerking
        ];
        voegRijToe(data, 'his3');
      }
    } else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
}

const showProductHistory = function (history) {
  try {
    console.log('History ontvangen:', history);
    if (history && history.history) {
      for (let record of history.history) {
        let data = [
          record.product_naam,
          record.product_type,
          record.tijdstip, 
          record.product_aantal_wijziging
        ];
        voegRijToe(data, 'prodhis');
      }
    } else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
}

const getInventory = function () {
  const url = `http://${lanIP}/inventory/`;
  handleData(url, showInventory);
};
const getSensorHistoryBarcode = function () {
  const url = `http://${lanIP}/historiek/2/`;
  handleData(url, showSensorHistoryBarcode);
}
const getSensorHistoryLight = function () {
  const url = `http://${lanIP}/historiek/1/`;
  handleData(url, showSensorHistoryLight);
}
const getSensorHistoryJoy = function () {
  const url = `http://${lanIP}/historiek/3/`;
  handleData(url, showSensorHistoryJoy);
}

const getProductHistory = function () {
  const url = `http://${lanIP}/product-history/`;
  handleData(url, showProductHistory); 
}

const init = function () {
  console.info('DOM geladen');
  inventory_page = document.querySelector('.js-inventory');
  settings_page = document.querySelector('.js-settings');
  cart_page = document.querySelector('.js-cart');
  sensor_history_page = document.querySelector('.js-sensor-history');
  product_history_page = document.querySelector('.js-product-history');

  listenToUI();
  listenToSocket();
  if (inventory_page) {
    getInventory();
  }
  if (settings_page) {
  }
  if (cart_page) {
  }
  if (sensor_history_page) {
    getSensorHistoryBarcode();
    getSensorHistoryLight();
    getSensorHistoryJoy();
  }
  if (product_history_page) {
    getProductHistory();
  }
};

document.addEventListener('DOMContentLoaded', init);
