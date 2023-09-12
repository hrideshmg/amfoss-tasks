// Async functions always return promises
async function fetchCoords(place)
{
    let response = await fetch(`http://api.openweathermap.org/geo/1.0/direct?q=${place}&appid=8f66029f46345fe4089e2a3c459bb6c9`);
    let data = await response.json();

    if (data.length != 0) 
    {
        return {"latitude":data[0].lat, "longitude":data[0].lon};
    } 
    else 
    {
        return false;
    }
}

async function fetchWeather(coords)
{
    let response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${coords.latitude}&lon=${coords.longitude}&appid=8f66029f46345fe4089e2a3c459bb6c9&units=metric`);
    let data = await response.json()
    weather = {
        "name": data.name,
        "description": data["weather"][0].main,
        "temperature": data.main.temp,
        "humidity": data.main.humidity,
    }
    return weather;
}

function updateHtml(weather)
{
    document.getElementById("place").textContent = weather.name;
    document.getElementById("temperature").textContent = weather.temperature;
    document.getElementById("description").textContent = weather.description;

    switch (weather.description) {
    case "Rain":
        document.body.style.background = "url(assets/Rain.webp)";
        break;
    case "Clouds":
        document.body.style.background = "url(assets/cloudy.jpg)";
        break;
    case "Mist":
        document.body.style.background = "url(assets/mist.jpg)";
        break;
    case "Clear":
        document.body.style.background = "url(assets/clear.avif)";
        break;
    default:
        document.body.style.background = "url(assets/cloudy.jpg)";
        break;
    }
}

// This function needs to be async in order to resolve the object (using await) from the promise returned by fetchWeather
async function updateWeather() 
{
    weather = await fetchWeather(coords);
    updateHtml(weather);
}

window.onload = () => {
    let date = new Date;
    greeting = document.getElementById("greeting");
    if (date.getHours() < 12) {
        greeting.textContent = "Good Morning";
    }
    else if (date.getHours <15) {
        greeting.textContent = "Good Afternoon";
    }
    else if (date.getHours) {
        greeting.textContent = "Good Evening";
    }

    // Kollam's coordinates are loaded by default
    coords = {"latitude":"8.8879509", "longitude":"76.5955013"};
    updateWeather(coords);
}

document.getElementById("search_form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const search = document.getElementById("place-input");

    coords = await fetchCoords(search.value);
    if (coords)
    {
        updateWeather(coords);
    } else
    {
        document.getElementById("place").textContent = "City not found!";
        document.getElementById("temperature").textContent = "";
        document.getElementById("description").textContent = "";
        document.body.style.background = "url(assets/error.png)";
    }
    
    search.value = "";
})
