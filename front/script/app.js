const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

let loadedRecordsCount = 0; // Houd het aantal geladen records bij
const recordsPerPage = 5; // Aantal records per keer laden

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
  const moreBtn = document.querySelector('.load-more-btn');
  if (moreBtn) {
    moreBtn.addEventListener('click', () => {
      getMoreRecords();
    });
  }
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  // Voeg hier meer socket event listeners toe, indien nodig
};

const showRecordsHistoriek = function (records) {
  console.log('Records ontvangen:', records);
  if (records && records.historiek) {
    const startIndex = loadedRecordsCount;
    const endIndex = Math.min(startIndex + recordsPerPage, records.historiek.length);

    for (let i = startIndex; i < endIndex; i++) {
      const record = records.historiek[i];
      voegRijToe(record.device_naam, record.waarde, record.tijdstip_waarde, record.opmerking);
    }
    
    loadedRecordsCount = endIndex; // Update het aantal geladen records
  } else {
    console.error('Ongeldige records data ontvangen:', records);
  }
};

const getRecordsHistoriek = function () {
  const url = `http://${lanIP}/historiek/`;
  handleData(url, showRecordsHistoriek);
};

const getMoreRecords = function () {
  console.log('Meer records laden...');
  const url = `http://${lanIP}/historiek/meer`;
  handleData(url, function(records) {
    if (records && records.historiek) {
      showRecordsHistoriek(records);
    } else {
      console.error('Ongeldige records data ontvangen:', records);
    }
  });
};

const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
  getRecordsHistoriek();
};

document.addEventListener('DOMContentLoaded', init);
