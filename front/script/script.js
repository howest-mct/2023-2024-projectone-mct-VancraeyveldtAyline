function myFunction() {
    // Declare variables
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.querySelector('.search-bar');
    filter = input.value.toUpperCase();
    table = document.querySelector('.myTable');
    tr = table.getElementsByTagName('tr');
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      tr[i].style.display = 'none'; // Hide the row initially
      td = tr[i].getElementsByTagName('td');
      for (j = 0; j < td.length; j++) {
        if (td[j]) {
          txtValue = td[j].textContent || td[j].innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = '';
            break; // Break the loop once a match is found
          }
        }
      }
    }
  }
  
  document.querySelector('.toggleSwitch').addEventListener('change', function () {
    if (this.checked) {
      console.log('Switch is ON');
      // Voeg hier je logica toe voor wanneer de switch aan staat
    } else {
      console.log('Switch is OFF');
      // Voeg hier je logica toe voor wanneer de switch uit staat
    }
  });
  
  /* When the user clicks on the button,
  toggle between hiding and showing the dropdown content */
  function dropdownfunction() {
    document.getElementById('myDropdown').classList.toggle('show');
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName('dropdown-content');
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  };
  