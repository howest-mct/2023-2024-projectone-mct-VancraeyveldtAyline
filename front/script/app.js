const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

const voegRijToe = function (data) {
  const tableBody = document.querySelector('.myTable');
  let rijHTML = `<tr>`
  for (let i of data) {
    rijHTML += `<td>${i}</td>`
  }
  rijHTML += `</tr>`;
  console.log("workesssss")
  tableBody.insertAdjacentHTML('beforeend', rijHTML);
};

const listenToUI = function () {
  loadMoreBtn = document.querySelector('load-more-btn')
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  // Voeg hier meer socket event listeners toe, indien nodig
};

const showInventory = function (inventory) {
  try {
    console.log('test')
    console.log('Records ontvangen:', inventory);
    if (inventory && inventory.inventory) {
      for (let product of inventory.inventory) {
        let data = [product.product_naam, product.product_type, product['max(tijdstip)'], product.totaal_aantal, product.minimum_waarde]
        voegRijToe(data);
      }
    } else {
      console.error('Ongeldige records data ontvangen:', records);
    }}
  catch (e) {
    console.log(e)
  }
};

const getInventory = function () {
  const url = `http://${lanIP}/inventory/`;
  handleData(url, showInventory);
};

const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
  getInventory();
};

document.addEventListener('DOMContentLoaded', init);
