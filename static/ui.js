//toggle results display

button = document.getElementById("showResults")
results = document.getElementById("results")
compare = document.getElementById("compare")
// button.addEventListener('click', () => {

//     if (results.style.display == 'block')
//     {
//         results.style.display = 'none';
//     }

//     else 
//     {
//         results.style.display = 'block';
//     }

//   });


var validPostcodes = ['DH1', 'DH2', 'DH3', 'DH4', 'DH5', 'DH6', 'DH7', 'DH8', 'DH9', 'DL1', 'DL12', 'DL13', 'DL14', 'DL15', 'DL16', 'DL17', 'DL2', 'DL3', 'DL4', 'DL5', 'Durham', 'EH12', 'NE36', 'NE63', 'SR7', 'SR8', 'TS16', 'TS17', 'TS18', 'TS19', 'TS2', 'TS20', 'TS21', 'TS22', 'TS23', 'TS24', 'TS25', 'TS26', 'TS27', 'TS28', 'TS29', 'TS5'];

// TODO: We need to build some validation
var constraints = {
    postcode: {
        presence: true,
        inclusion: {
            within: validPostcodes,
            message: "entered not allowed"
          }
    },
    // TODO: Add max value for bathrooms, bedrooms, receptions
    bathrooms: {
        presence: true,
        // pattern: "/^\+?(0|[1-9]\d*)$/",
        numericality: {
            lessThanOrEqualTo: 10,
            greaterThanOrEqualTo: 1,
            onlyInteger: true
        }
    },
    bedrooms: {
        presence: true,
        // pattern: "/^\+?(0|[1-9]\d*)$/",
        numericality: {
            lessThanOrEqualTo: 10,
            greaterThanOrEqualTo: 1,
            onlyInteger: true
        }

    },
    receptions: {
        presence: true,
        // pattern: "/^\+?(0|[1-9]\d*)$/",7
        numericality: {
            lessThanOrEqualTo: 10,
            greaterThanOrEqualTo: 0,
            onlyInteger: true
        }
    }

};

function processForm(e) {
    if (e.preventDefault) e.preventDefault();


    /* do what you want with the form */
    var bedrms = document.getElementById("bedrms").value;
    var bthrms = document.getElementById("bthrms").value;
    var pcode = document.getElementById("pcode").value;
    var rcptns = document.getElementById("rcptns").value;

    console.log(pcode);
    console.log(bthrms);
    console.log(bedrms);
    console.log(rcptns);

    let error = validate({
        bedrooms: bedrms,
        bathrooms: bthrms,
        postcode: pcode,
        receptions: rcptns
        }, constraints)

    var ids = ["pcode", "bedrms", "bthrms", "rcptns"];
    var args = ["postcode", "bedrooms", "bathrooms", "receptions"];

    // Data validation
    var bIsInvalid = false;
    console.log(error);
    if (error !== undefined){
        for(var i = 0; i < ids.length; i++){
            let label = document.getElementById(`${ids[i]}-label`);
            console.log(i);
            console.log(label);

            if (error[args[i]] !== undefined) {
                label.innerHTML = error[args[i]][0];
                bIsInvalid = true;
            } else {
                label.innerHTML = "";
            }
        }
        if (bIsInvalid == true){
            return false;
        }
    }

    // resetting labels after successful validation
    for (var i = 0; i < args.length; i++){
        let label = document.getElementById(`${ids[i]}-label`);
        label.innerHTML = "";
    }

    console.log(error);
    // if err print error

    fetch("/submitModelData?bedrms=" + bedrms + "&bthrms=" + bthrms + "&pcode=" + pcode + "&rcptns=" + rcptns)
    .then(response => {
      // indicates whether the response is successful (status code 200-299) or not
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }
      console.log(response);
      return response.text()
    })
    .then(data => {
      const arr = data.split(",");
      document.getElementById("result-value").innerText = "Estimated valuation: " + arr[0];
      document.getElementById("postcodehere").innerText = "Comparison with other properties in " + arr[1];
      document.getElementById("medPrice").innerText = "Median Price £" + arr[5];
      document.getElementById("medBedrooms").innerText = "Median no Bedrooms " + arr[2];
      document.getElementById("medBathrooms").innerText = "Median no Bathrooms " + arr[3];
      document.getElementById("medReceptions").innerText = "Median no Receptions " + arr[4];
      document.getElementById("results").style.display = "block";
      document.getElementById("compare").style.display = "block";
      //google maps manipulation
      document.getElementById("googlemaps")["src"] = `https://www.google.com/maps/embed/v1/place?key=AIzaSyAUT8HAbNhczkJs5Ib1HcX1vOkX0_Xcsdo
      &q=${pcode}`;

      console.log(data);
    })
    .catch(error => console.log(error));


    // You must return false to prevent the default form behavior
    return false;
}

var form = document.getElementById('my-form');
if (form.attachEvent) {
    form.attachEvent("submit", processForm);
} else {
    form.addEventListener("submit", processForm);
}

