// Ensure to include the AWS SDK in your HTML file
// <script src="https://sdk.amazonaws.com/js/aws-sdk-2.1.12.min.js"></script>

// Fetch weather data from the local JSON file
async function fetchWeatherData() {
    try {
        const response = await fetch('weather_data.json');
        const weatherData = await response.json();

        // Display the data for each city
        for (const city in weatherData) {
            const data = weatherData[city];

            // Define image URLs for each city
            let imageUrl;
            switch (city) {
                case 'Nairobi':
                    imageUrl = 'images/nairobi.jpg'; // Path to Nairobi's image
                    break;
                case 'Arusha':
                    imageUrl = 'images/arusha.jpg'; // Path to Arusha's image
                    break;
                case 'Kampala':
                    imageUrl = 'images/kampala.jpg'; // Path to Kampala's image
                    break;
                default:
                    imageUrl = 'images/default.jpg'; // Default image
            }

            document.getElementById(city.toLowerCase()).innerHTML = `
                <img src="${imageUrl}" alt="${data.weather[0].description}">
                <h2>${data.name}</h2>
                <p>Temperature: ${data.main.temp}°C</p>
                <p>Condition: ${data.weather[0].description}</p>
            `;
        }
    } catch (error) {
        console.error('Error fetching weather data:', error);
    }
}

// Call the function to fetch and display weather data
fetchWeatherData();
