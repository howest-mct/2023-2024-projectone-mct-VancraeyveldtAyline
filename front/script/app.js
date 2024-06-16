const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);
let buttons;
let rows_to_be_loaded_sensor_barcode = 10;
let rows_to_be_loaded_sensor_light = 10;
let rows_to_be_loaded_sensor_joy = 10;
let rows_to_be_loaded_product = 10;
let storedProductHistory;
let storedBarcodeHistory;
let storedLightHistory;
let storedJoyHistory;



const listenToUI = function () {

  const shutdownBtn = document.querySelector('.shutdown-btn');
  if (shutdownBtn) {
    shutdownBtn.addEventListener('click', function () {
      console.log('SHUTTING DOWN')
      socketio.emit("F2B_shutdown", {"status":1})
    })
  }

  const loadMoreBtnBar = document.querySelector('.btn__barcode');
  if (loadMoreBtnBar) {
    loadMoreBtnBar.addEventListener('click', function () {
      console.log('Button was clicked!');
      rows_to_be_loaded_sensor_barcode = 5;
      showSensorHistoryBarcode(storedBarcodeHistory);
  })
 } else {
    console.error('Button not found!');
  }

  const loadMoreBtnLight = document.querySelector('.btn__light');
  if (loadMoreBtnLight) {
    loadMoreBtnLight.addEventListener('click', function () {
      console.log('Button was clicked!');
      rows_to_be_loaded_sensor_light = 5;
      showSensorHistoryLight(storedLightHistory);
  })
 } else {
    console.error('Button not found!');
  }

  const loadMoreBtnJoy = document.querySelector('.btn__joy');
  if (loadMoreBtnJoy) {
    loadMoreBtnJoy.addEventListener('click', function () {
      console.log('Button was clicked!');
      rows_to_be_loaded_sensor_joy = 5;
      showSensorHistoryJoy(storedJoyHistory);
  })
 } else {
    console.error('Button not found!');
  }

  const loadMoreBtnProd = document.querySelector('.btn__product');
  if (loadMoreBtnProd) {
    loadMoreBtnProd.addEventListener('click', function () {
      console.log('Button was clicked!');
      rows_to_be_loaded_sensor_joy = 5;
      showProductHistory(storedProductHistory);
  })
 } else {
    console.error('Button not found!');
  }


  buttons = document.querySelectorAll('.toggle-button'); // Definieer buttons hier
  buttons.forEach(button => {
      button.addEventListener('click', function () {
          // Verwijder 'active' class van alle knoppen
          buttons.forEach(btn => {
              btn.classList.remove('active');
          });
          // Voeg 'active' class toe aan de geklikte knop
          button.classList.add('active');
          const color = button.classList[1]; // Verkrijg kleur van geklikte knop
          console.log(color);
          socketio.emit("F2B_lighting", {"color": color}); // Stuur kleur naar backend
      });
  });
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  socketio.on('B2F_product_change', function (data) {
    console.log('Product change received:', data);
    if (product_history_page) {
      let productData = [data.name, data.category, data.date, data.change];
      // Get the table body
      let tableBody = document.querySelector('.myTable');
      // Check if adding one row will exceed the limit of 10 rows
      if (tableBody.querySelectorAll('tr').length >= 10) {
        // Remove the last row
        tableBody.deleteRow(-1);
      }
      // Insert new row at the top of the table
      let rijHTML=dataRow2HTML(productData,"prodhis");
      tableBody.innerHTML=rijHTML+tableBody.innerHTML;
      //voegRijToe(productData, 'prodhis');
    }
  });

  socketio.on('B2F_lighting', function (object) {
    let lighting_color = object.color; // Ontvangen kleur van backend
    // Verwijder 'active' class van alle knoppen (gebruik buttons hier)
    buttons.forEach(btn => {
        btn.classList.remove('active');
    });
    // Voeg 'active' class toe aan knop met overeenkomende kleur
    const current_color = document.querySelector("." + lighting_color);
    if (current_color) {
        current_color.classList.add('active');
    }
});

  socketio.on('B2F_light_open', function (object) {
    console.log(object)
    const door_icon = document.querySelector(".door");
    let iconHTML;
    iconHTML = `
        <div class="door">
          <img src="Icons/door_open_24dp_FILL0_wght400_GRAD0_opsz24 1.svg" alt="open door icon" class="door__img">
        </div>
      `;
    if (door_icon) {
      door_icon.outerHTML = iconHTML;
    }
  });

  socketio.on('B2F_light_close', function (object) {
    console.log(object)
    const door_icon = document.querySelector(".door");
    let iconHTML;
    iconHTML = `
        <div class="door">
          <img src="Icons/door_front_24dp_FILL0_wght400_GRAD0_opsz24 1.svg" alt="closed door icon" class="door__img">
        </div>
      `;
    if (door_icon) {
      door_icon.outerHTML = iconHTML;
    }
  })
  socketio.on("B2F_xpos_left", function (object) {
    console.log(object)
  })

  socketio.on('B2F_set_switch', function (data) {
    // console.log("B2F_set_switch event received:", data);
    const toggleSwitch = document.querySelector('.toggleSwitch');
    if (toggleSwitch) {
      toggleSwitch.checked = data.status;
      if (data.status) {
        console.log('Switch is set to ON');
      } else {
        console.log('Switch is set to OFF');
      }
    } else {
      console.error("Toggle switch element not found.");
    }
  });
};

function listenToDropdown() {
  document.getElementById('myDropdown').classList.toggle('show');
  window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
      const dropdowns = document.getElementsByClassName('dropdown-content');
      for (let i = 0; i < dropdowns.length; i++) {
        const openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  };
}

function myFunction() {
  const input = document.querySelector('.search-bar');
  const filter = input.value.toUpperCase();
  const table = document.querySelector('.myTable');
  const tr = table.getElementsByTagName('tr');

  for (let i = 0; i < tr.length; i++) {
    tr[i].style.display = 'none';
    const td = tr[i].getElementsByTagName('td');
    for (let j = 0; j < td.length; j++) {
      if (td[j]) {
        const txtValue = td[j].textContent || td[j].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = '';
          break;
        }
      }
    }
  }
}
const listenToSwitch = function() {
  const toggleSwitch = document.querySelector('.toggleSwitch');
  if (toggleSwitch) {
    toggleSwitch.addEventListener('change', function () {
      if (this.checked) {
        console.log('Switch is ON');
        socketio.emit("F2B_buzzer", {"status":1});
      } else {
        console.log('Switch is OFF');
        socketio.emit("F2B_buzzer", {"status":0});
      }
    });
  }
};


const getRowCountFromTable = function (className) {
  tableBody = document.querySelector('.'+className);
  console.log(tableBody.childElementCount)
  return tableBody.childElementCount
}
  
const updateHTML = function (className, htmlcontent) {
  tableBody = document.querySelector('.'+className);
  tableBody.innerHTML=htmlcontent;
}

const voegRijToe = function (data, type) {
  // console.log("data:", data);
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
    console.log("INSERT WORKS")
    tableBody = document.querySelector('.myTable');
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
  } 
  
  else if (type === 'cart') {
    tableBody = document.querySelector('.myTable');
    rijHTML = `<tr>`;
    for (let i of data) {
      rijHTML += `<td>${i}</td>`;
    }
    rijHTML += `</tr>`;
  }

  if (tableBody) {
    // tableBody.insertAdjacentHTML('beforeend', rijHTML);
    return rijHTML
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
        console.log('works2')
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
    storedBarcodeHistory = history;
    let alldata = [];
    console.log('History ontvangen:', history);
    if (history && history.history) {
      for (let record of history.history) {
        let data = [record.waarde, record.tijdstip_waarde, record.opmerking];
        alldata.push(data);
      }
      let contentHTML = '';
      let nrExistingRows = getRowCountFromTable('myTable1');
      let nrRowsInTable = nrExistingRows + rows_to_be_loaded_sensor_barcode;
      for (let i = 0; i < nrRowsInTable; i++) {
        contentHTML += voegRijToe(alldata[i], 'his1');
        // voegRijToe(alldata[i], 'his1');
      }
      updateHTML('myTable1', contentHTML);
    } else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
};

const showSensorHistoryLight = function (history) {
  try {
    storedLightHistory = history;
    let alldata = [];
    console.log('History ontvangen:', history);
    if (history && history.history) {
      for (let record of history.history) {
        let data = [record.waarde, record.tijdstip_waarde, record.opmerking];
        alldata.push(data);
      }
      let contentHTML = '';
      let nrExistingRows = getRowCountFromTable('myTable2');
      let nrRowsInTable = nrExistingRows + rows_to_be_loaded_sensor_light;
      for (let i = 0; i < nrRowsInTable; i++) {
        contentHTML += voegRijToe(alldata[i], 'his2');
      }
      updateHTML('myTable2', contentHTML);
    } else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
};

const showSensorHistoryJoy = function (history) {
  try {
    storedJoyHistory = history;
    let alldata = [];
    console.log('History ontvangen:', history);
    if (history && history.history) {
      for (let record of history.history) {
        let data = [record.waarde, record.tijdstip_waarde, record.opmerking];
        alldata.push(data);
      }
      let contentHTML = '';
      let nrExistingRows = getRowCountFromTable('myTable3');
      let nrRowsInTable = nrExistingRows + rows_to_be_loaded_sensor_barcode;
      for (let i = 0; i < nrRowsInTable; i++) {
        contentHTML += voegRijToe(alldata[i], 'his3');
      }
      updateHTML('myTable3', contentHTML);
    } else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
};

const showProductHistory = function (history) {
  try {
    storedProductHistory = history
    let alldata = []
    console.log('History ontvangen:', history);
    if (history && history.history) {
        for (let record of history.history) {
          let data = [
            record.product_naam,
            record.product_type,
            record.tijdstip,
            record.product_aantal_wijziging
          ];
          alldata.push(data)
        }
        let contentHTML = "";
        let nrExistingRows=getRowCountFromTable("myTable");
        let nrRowsInTable=nrExistingRows+rows_to_be_loaded_product;
        for (let i = 0; i < nrRowsInTable; i++) {
          contentHTML += voegRijToe(alldata[i], "prodhis")
          console.log("date" +i+' '+ alldata[i][2])
          // voegRijToe(alldata[i], "prodhis");
        }
        updateHTML("myTable", contentHTML);
        console.log("UPDATE HTML")
      }
       else {
      console.error('Ongeldige records data ontvangen:', history);
    }
  } catch (e) {
    console.log(e);
  }
}




const showCart = function (cart) {
  try {
    console.log('Cart ontvangen:', cart);
    if (cart && cart.cart) {
      for (let item of cart.cart) {
        let data = [
          item.product_naam,
          item.product_type,
          item.totaal_aantal
        ];
        voegRijToe(data, 'cart');
      }
      // console.log("data= "+ cart.cart)
      // console.log(cart.cart.length)
      if (cart.cart.length == 0) {
        console.log("WORKS")
        data = ["---", "---", "---"]
        voegRijToe(data, "cart")
      }
    } else {
      console.error('Ongeldige records data ontvangen:', cart);
    }
  } catch (e) {
    console.log(e);
  }
}


const getInventory = function () {
  const url = `http://${lanIP}/inventory/`;
  handleData(url, showInventory);
  console.log('works1')
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
const getCart = function () {
  const url = `http://${lanIP}/cart/`;
  handleData(url, showCart); 
}



const init = function () {
  console.info('DOM geladen');
  inventory_page = document.querySelector('.js-inventory');
  settings_page = document.querySelector('.js-settings');
  cart_page = document.querySelector('.js-cart');
  sensor_history_page = document.querySelector('.js-sensor-history');
  product_history_page = document.querySelector('.js-product-history');

  listenToUI();
  listenToSwitch()
  listenToSocket();
  if (inventory_page) {
    getInventory();
    listenToDropdown();
  }
  if (settings_page) {
  }
  if (cart_page) {
    getCart()
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
