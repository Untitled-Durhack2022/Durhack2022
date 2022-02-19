//toggle results display
button = document.getElementById("showResults")
results = document.getElementById("results")
button.addEventListener('click', () => {

    if (results.style.display == 'block')
    {
        results.style.display = 'none';
    }

    else 
    {
        results.style.display = 'block';
    }

  });

