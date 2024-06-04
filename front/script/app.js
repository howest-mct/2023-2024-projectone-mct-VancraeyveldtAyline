const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

const voegRijToe = function (sensorNaam, meting, tijdstip, opmerking) {
  const tableBody = document.querySelector('.historiek__table-body');
  const rijHTML = `
    <tr>
      <td>${sensorNaam}</td>
      <td>${meting}</td>
      <td>${tijdstip}</td>
      <td>${opmerking}</td>
    </tr>
  `;
  tableBody.insertAdjacentHTML('beforeend', rijHTML);
};

const listenToUI = function () {
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  // Voeg hier meer socket event listeners toe, indien nodig
};

const showRecordsHistoriek = function (records) {
  try {
    console.log('test')
    console.log('Records ontvangen:', records);
    if (records && records.historiek) {
      for (let record of records.historiek) {
        voegRijToe(record.device_naam, record.waarde, record.tijdstip_waarde, record.opmerking);
      }
    } else {
      console.error('Ongeldige records data ontvangen:', records);
    }}
  catch (e) {
    console.log(e)
  }
};

const getRecordsHistoriek = function () {
  const url = `http://${lanIP}/historiek/`;
  handleData(url, showRecordsHistoriek);
};

const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
  getRecordsHistoriek();
};

document.addEventListener('DOMContentLoaded', init);
