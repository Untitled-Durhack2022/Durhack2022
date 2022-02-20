//toggle results display

button = document.getElementById("showResults")
results = document.getElementById("results")
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
            message: "PostCode entered not allowed"
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
    let bedrms = document.getElementById("bedrms").value;
    let bthrms = document.getElementById("bthrms").value;
    let pcode = document.getElementById("pcode").value;
    let rcptns = document.getElementById("rcptns").value;

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

    if (error !== undefined){
        let args = ["pcode", "bedrms", "bthrms", "rcptns"];
        alert("Incorrect Input Arguments")
    //     for(var i =0; i <= error.length();i++){
    //         let label = document.querySelectorAll(`[for={args[i]}]`);
    //         label.innerHTML = error[args[0]];
    //         }
    // }

    console.log(error);
    // if err print error

    fetch(`/submitModelData?bedrms={bedrms}&bthrms={bthrms}&pcode={pcode}&rcptns={rcptns}`)
    .then(response => {
      // indicates whether the response is successful (status code 200-299) or not
      if (!response.ok) {
        throw new Error(`Request failed with status ${reponse.status}`)
      }
      return response.text()
    })
    .then(data => {
      console.log(data);
    })
    .catch(error => console.log(error))







    // You must return false to prevent the default form behavior
    return false;
}

var form = document.getElementById('my-form');
if (form.attachEvent) {
    form.attachEvent("submit", processForm);
} else {
    form.addEventListener("submit", processForm);
}

