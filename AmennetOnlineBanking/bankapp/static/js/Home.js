// Theme Toggler
const themeToggler = document.querySelector(".theme-toggler");
themeToggler.addEventListener("click", () => {
  document.body.classList.toggle("dark-theme-variables");
  
  themeToggler.querySelector("span:nth-child(1)").classList.toggle("active");
  themeToggler.querySelector("span:nth-child(2)").classList.toggle("active");
  
  // Store the theme preference in Local Storage
  const isDarkTheme = document.body.classList.contains("dark-theme-variables");
  localStorage.setItem("themePreference", isDarkTheme ? "dark" : "light");
});

// Check for stored theme preference on page load
const storedThemePreference = localStorage.getItem("themePreference");
if (storedThemePreference === "dark") {
  document.body.classList.add("dark-theme-variables");
  themeToggler.querySelector("span:nth-child(1)").classList.add("active");
  themeToggler.querySelector("span:nth-child(2)").classList.remove("active");
}

// Sidebar
const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");

// Show Sidebar
menuBtn.addEventListener("click", () => {
  sideMenu.style.display = "block";
});

// Hide Sidebar
closeBtn.addEventListener("click", () => {
  sideMenu.style.display = "none";
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 768) {
    if (sideMenu.style.display == "none") {
      sideMenu.style.display = "block";
    }
  } else {
    if (sideMenu.style.display == "block") {
      sideMenu.style.display = "none";
    }
  }
});

  //devise convertisseur
// Hardcoded conversion rates
// Hardcoded conversion rates
const conversionRates = {
  TND: 1,
  AED: 0.37,
  CAD: 0.32,
  CHF: 0.29,
  DKK: 1.95,
  EUR: 0.26,
  GBP: 0.23,
  JPY: 32.45,
  KWD: 0.09,
  MAD: 2.77,
  NOK: 2.49,
  QAR: 1.08,
  SAR: 1.09,
  SEK: 2.54,
  USD: 0.30
};
function findValue(obj, searchKey) {
  for (var key in obj) {
    if (obj.hasOwnProperty(key) && key === searchKey) {
      return obj[key];
    }
  }
  return null;
}



// Get the select element
// Get the select element
// Get the select element



// Add event listener for change event

  // Get the monetary value element
  var rows = Array.from(document.querySelectorAll('tr'));
  rows = rows.slice(1, rows.length - 1);
  var initialSoldes = rows.map(function(row) {
    var soldeElement = row.getElementsByTagName('td')[row.getElementsByTagName('td').length - 1];
    return soldeElement.textContent.trim();
  });
  
  console.log(initialSoldes);
  var zippedData = rows.map(function(row, index) {
    return [row, initialSoldes[index]];
  });
  console.log(zippedData);
  function find(x,obj){
    for(i=0;i<obj.length;i++){
      if(obj[i][0]==x){
        return obj[i][1];
      }
    }
    return null
  }
  rows.forEach(function(row) {
    var selectElement = row.querySelector('select[name="devise"]');
    var initialSol = find(row, zippedData);
  
    // Add event listener for change event if selectElement exists
    if (selectElement) {
      selectElement.addEventListener('change', function() {
        // Get the selected value from the select element
        var selectedValue = selectElement.value;
  
        var currencyCode;
        if (selectedValue === 'TND') {
          row.getElementsByTagName('td')[row.getElementsByTagName('td').length - 1].textContent = initialSol;
          return;
        } else {
          currencyCode = findValue(conversionRates, selectedValue);
        }
  
        var soldeElement = row.getElementsByTagName('td')[row.getElementsByTagName('td').length - 1];
        var cleanedSolde = initialSol.replace(/\s/g, '').replace(/,/g, '.');
        var solde = parseFloat(cleanedSolde);
        var convertedsolde = solde / currencyCode;
        console.log(solde);
        console.log(convertedsolde)
        row.getElementsByTagName('td')[row.getElementsByTagName('td').length - 1].textContent = convertedsolde.toFixed(2);
  
        // Handle the value change
  
        // Perform further actions based on the selected value
        // ...
      });
    }
  });


  

  



