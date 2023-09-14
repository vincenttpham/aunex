//setup google maps address auto complete
function initialize() {
    var input = document.getElementById('searchLocation');
    new google.maps.places.Autocomplete(input);
    initMap();
}

google.maps.event.addDomListener(window, 'load', initialize);

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("searchLocation").addEventListener("keyup", event => {submitCheck(event)});
    document.getElementById("distance").addEventListener("keyup", event => {submitCheck(event)});

});

function submitCheck(event){
    if(event.key !== "Enter") return;
    document.getElementById("findDealers").click();
    event.preventDefault();
}

//global scope variables
const GM_QUERY_CAP = 7; //prevent query limit and abuse
let pos;
let map;
let bounds;
let markers = [];
let infoWindow;
let currentInfoWindow;
let service;
let infoPane;
let locations = []
let locAddresses
let vendors

let musway
let elite
let phone

var cArray = document.getElementById('coordinates').value;
var coordinates = cArray.split(',');
for(var i = 0; i < coordinates.length; i++) {
    var coordinate = coordinates[i].split('/');
    var dealerCoordinate = [];
    var c0 = coordinate[0].replace(/[\[\]']+/g, '');
    var c1 = coordinate[1].replace(/[\[\]']+/g, '');
    dealerCoordinate.push(parseFloat(c0));
    dealerCoordinate.push(parseFloat(c1));
    locations.push(dealerCoordinate);
}

function initMap() {
    //initialize variables
    bounds = new google.maps.LatLngBounds();
    infoWindow = new google.maps.InfoWindow;
    currentInfoWindow = infoWindow;
    infoPane = document.getElementById('location-info');
    //set default location to Chino, CA
    pos = { lat: 34.42, lng: -117.69 };
    //create map
    map = new google.maps.Map(document.getElementById('map-canvas'), {
        center: pos,
        zoom: 8
    });
    //update the locAddresses and vendors
    fetch('dealer-locations')
    .then(response => response.json())
    .then(locations => {

        vendors = locations.locations
        locAddresses = locations.addresses
        musway = locations.musway
        elite = locations.elite
        phone = locations.phone
        
    });
}

function getLocation(){
    //try HTML5 geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
        pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        map = new google.maps.Map(document.getElementById('map-canvas'), {
            center: pos,
            zoom: 15
        });
        bounds.extend(pos);

        infoWindow.setPosition(pos);
        infoWindow.setContent('Location found.');
        infoWindow.open(map);
        map.setCenter(pos);

        //check for nearby dealers using the user's location
        getNearbyDealers(pos);
        }, () => {
            //browser supports geolocation, but user has denied permission
            handleLocationError(true, infoWindow);
        });
    } else {
        //browser doesn't support geolocation
        handleLocationError(false, infoWindow);
    }
}

//handle a geolocation error
function handleLocationError(browserHasGeolocation, infoWindow) {

    //display an InfoWindow at the map center
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Geolocation permissions denied. Using default location.' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
    currentInfoWindow = infoWindow;

    //call Places Nearby Search on the default location
    getNearbyDealers(pos);
}

//displays nearby Aunex dealers
// ~~~ split into several functions if reusable later...
function getNearbyDealers(loc = null){

    //clamp search distance
    clampSearchDistance()

    //remove any pre-existing markers
    removeMarkers()

    var nearby = []; //list of indexes of dealers within dist of user
    var nearbyCoords = []; //list of coords for the dealers
    var distances = []; //array of distances used to sort nearby
    var dist = document.getElementById('distance').value; //distance from user 
    if(loc == null){ //check if using search bar location or geolocation
        loc = document.getElementById('searchLocation').value; 
    }

    //unit conversion, mi -> meters
    dist *= 1609.34

    //get the location the user is requesting nearby sellers from
    fetch('https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '&key=AIzaSyC0uC2V-60qNc3TeAyTtemqebljrdni97A')
    .then(response => response.json())
    .then(data => {

        //get location coordinates
        var locCoords = data.results[0]["geometry"]["location"];

        //move the map to the location
        map.panTo(locCoords);

        //check distances from location
        for(var x = 0; x < locations.length; x++){
            
            //get the xth coordinate pair
            var coordLatLng = new google.maps.LatLng(locations[x][0], locations[x][1]);
            
            //check the distance
            var d = google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(locCoords), coordLatLng)
            if (d < dist){ 
                //sort by distance
                let j = distances.length; //where the location is being inserted
                for(var i = 0; i < distances.length; i++){
                    if(distances[i] > d){
                        j = i;
                        break;
                    }
                }
                distances.splice(j, 0, d);
                nearby.splice(j, 0, x);
                nearbyCoords.splice(j, 0, coordLatLng);

                //check limit
                if(nearby.length >= GM_QUERY_CAP){
                    break;
                }
            }
        };

        //clear the information in the current side panel and previous markers
        clearPanel()
        markers = [];

        //create service object to get place information
        service = new google.maps.places.PlacesService(map);

        //create a list of promises from the fetch function to keep the places in order
        let promises = [];

        //make the promises from each of the fetch requests for location information
        for(let i = 0; i < nearby.length; i++){
            promises.push(new Promise((resolve, reject) => {
                fetch('https://maps.googleapis.com/maps/api/geocode/json?address=' + encodeURIComponent(vendors[nearby[i]] + locAddresses[nearby[i]]) + '&key=AIzaSyC0uC2V-60qNc3TeAyTtemqebljrdni97A')
                .then(response => response.json())
                .then(data => {

                    //get the place from the returned json data
                    var place = data.results[0];

                    //create request
                    let request = {
                        placeId: place.place_id,
                        fields: ['name', 'formatted_address', 'geometry', 'rating',
                            'website', 'photos', 'formatted_phone_number',
                            'international_phone_number', 'business_status']
                    };

                    //get the details for the location then return an info div
                    service.getDetails(request, (placeResult, status) => {
                        console.log("Query for Place Details Status: " + status);
                        let r = createPanel(placeResult, i+1, distances[i], nearby[i]);
                        resolve(r); //this promise resolves when it successfully generates an info div
                    });

                })

            }));

            //adds marker for each i

            //create the marker
            let mark = new google.maps.Marker({
                position: nearbyCoords[i],
                map: map,
                label: {text: (i+1).toString(), color: "black", fontWeight: "900", fontSize: "15px"},
                icon: "static/main/favicon.png"
            });

            //add a listener -> when clicked scroll the side panel
            mark.addListener('click', () => {
                location.href = '#locationPanel' + (i+1);
                let p = document.getElementById('locationPanel' + (i+1));
                //show info above marker
                let placeInfowindow = new google.maps.InfoWindow();
                placeInfowindow.setContent(infoboxify(p.cloneNode(true)));
                placeInfowindow.open(mark.map, mark);
                currentInfoWindow.close();
                currentInfoWindow = placeInfowindow;
                //play highlight animation
                p.preventDefault;
                p.classList.remove("highlightAnimation");
                void p.offsetWidth;
                p.classList.add("highlightAnimation");
            });

            //add the mark to current list of markers
            markers.push(mark);
        }
        
        //wait for all promises to complete
        Promise.all(promises)
        .then((returnedPromises) => {
            //add the info panes
            returnedPromises.forEach(p => {
                infoPane.appendChild(p);
            });
        });

        //resize visible map bounds
        if(nearby.length > 0){
            var bounds = new google.maps.LatLngBounds();
            for (var i = 0; i < nearby.length; i++) {
                bounds.extend(nearbyCoords[i]);
            }
            map.fitBounds(bounds);
            //infoPane.innerHTML = "Select a dealer location for information.";
        }else { //no locations found given address
            infoPane.innerHTML = "No dealers within " + document.getElementById('distance').value + " miles of this location.";
            //contact info
            infoPane.innerHTML += '<hr><div>Please try a different address or contact us.</div><div>Email: <a href="mailto:sales@aunexusa.com">sales@aunexusa.com</a></div><div>Phone: <a href="tel:9095892010">(909) 589-2010</a></div>'
        }

        //show sidebar
        showPanel();

    }).catch(error => {
        infoPane.innerHTML = "Location invalid.";
        //contact info
        infoPane.innerHTML += '<hr><div>Please try a different address or contact us.</div><div>Email: <a href="mailto:sales@aunexusa.com">sales@aunexusa.com</a></div><div>Phone: <a href="tel:9095892010">(909) 589-2010</a></div>'
        showPanel();
    });


}

//clears and closes the sidebar
function clearPanel() {

    //if infoPane is already open, close it
    if (infoPane.classList.contains("open")) {
        infoPane.classList.remove("open");
    }

    //clear the previous details
    while (infoPane.lastChild) {
        infoPane.removeChild(infoPane.lastChild);
    }
}

//opens the info pane
function showPanel(placeResult) {
    infoPane.classList.add("open");
    document.getElementById("map-side-panel").style.animationPlayState = "running";
    document.getElementById("map-side-panel").style.display = "block";
}

//creates an info panel for a google place result then returns it
//@param placeResult returned place information from the Google Maps API
//@param number the number of the panel card
//@param dist distance to display
//@param locInd index of the location in the dealer array
function createPanel(placeResult, number=0, dist=0, locInd=0) {

    let locationPanel = document.createElement('div');
    locationPanel.classList.add('locationPanel');
    locationPanel.classList.add('locationUnderBar');
    //add id for scrolling
    locationPanel.id = 'locationPanel' + number;

    /*location primary photo
    if (placeResult.photos != null) {
        let firstPhoto = placeResult.photos[0];
        let photo = document.createElement('img');
        photo.classList.add('hero');
        photo.src = firstPhoto.getUrl();
        locationPanel.appendChild(photo);
    }
    */
    
    //show the number of the location
    let locationNumber = document.createElement('strong');
    locationNumber.innerHTML = number + " - " + (dist/1609.34).toFixed(2) + "mi";
    locationNumber.classList.add('locationNumber');
    locationPanel.appendChild(locationNumber);

    if (placeResult){

        //location Name and Website
        //location Website
        if (placeResult.website && "business_status" in placeResult) {
            let websitePara = document.createElement('strong');
            let websiteLink = document.createElement('a');
            websiteLink.classList.add('place');
            websiteLink.innerHTML = placeResult.name;
            websiteLink.title = placeResult.website;
            websiteLink.href = placeResult.website;
            websitePara.appendChild(websiteLink);
            locationPanel.appendChild(websitePara);
        }else  { 
            let name = document.createElement('strong');
            name.classList.add('place');
            if("business_status" in placeResult){ //location found
                name.textContent = placeResult.name;
            }else{ //location not found
                name.textContent = vendors[locInd];
            }
            locationPanel.appendChild(name);
        }
        

        //location Address
        let address = document.createElement('div');
        address.classList.add('details');
        address.textContent = placeResult.formatted_address;
        locationPanel.appendChild(address);

        //location phone number
        let p = phone[locInd];
        if (placeResult.formatted_phone_number) {
            let phoneNumber = document.createElement('div');
            let phoneLink = document.createElement('a');
            phoneLink.href = 'tel:' + placeResult.formatted_phone_number;
            phoneLink.innerHTML = 'Phone: ' + placeResult.formatted_phone_number;
            phoneNumber.classList.add('details');
            phoneNumber.appendChild(phoneLink);
            locationPanel.appendChild(phoneNumber);
        } else {
            let phoneNumber = document.createElement('div');
            let phoneLink = document.createElement('a');
            phoneLink.href = 'tel:' + p;
            phoneLink.innerHTML = 'Phone: ' + p;
            phoneNumber.classList.add('details');
            phoneNumber.appendChild(phoneLink);
            locationPanel.appendChild(phoneNumber);
        }

        //Aunex Logo
        var logo = document.createElement("img");
        logo.src = "static/main/aunex-logo-sml-01.png";
        logo.classList.add('locationPanelLogo')
        locationPanel.appendChild(logo);


        //Logo variables
        let v = vendors[locInd];

        //Musway Logo
        for (let i = 0; i < musway.length; i++) {
            let m = musway[i];
            if (m == v) {
                var muswayLogo = document.createElement("img");
                muswayLogo.src = "static/main/musway-logo.png";
                muswayLogo.classList.add('locationPanelMuswayLogo')
                locationPanel.appendChild(muswayLogo);
            }
        }

        //Elite Dealer Logo
        for (let i = 0; i < elite.length; i++) {
            let e = elite[i];
            if (e == v) {
                var eliteLogo = document.createElement("img");
                eliteLogo.src = "static/main/elite-dealer-logo-01.png";
                eliteLogo.classList.add('locationPanelEliteLogo')
                locationPanel.appendChild(eliteLogo);
            }
        }

        /* location international phone number
        if (placeResult.international_phone_number) {
            let iPhoneNumber = document.createElement('div');
            iPhoneNumber.classList.add('details');
            iPhoneNumber.textContent = 'International: ' + placeResult.international_phone_number;
            locationPanel.appendChild(iPhoneNumber);
        }
        */

        /* location Rating
        if (placeResult.rating != null) {
            let rating = document.createElement('div');
            rating.classList.add('details');
            rating.textContent = `Rating: ${placeResult.rating} \u272e`;
            locationPanel.appendChild(rating);
        }
        */

    }

    //return the location panel
    return locationPanel;
}


//takes a panel returned from createPanel, and converts to a inbox version to display on the map
function infoboxify(panel){
    panel.classList.remove("locationUnderBar");
    panel.classList.remove("highlightAnimation");
    panel.id += 'InfoBox';
    return panel;
}

//remove active markers from the map
function removeMarkers(){
    for(i=0; i<markers.length; i++){
        markers[i].setMap(null);
    }
}

//keeps the value of the distance input within min and max
function clampSearchDistance(){
    clampValue(document.getElementById('distance'));
}

//clamp a value of an input within its min and max
function clampValue(e){
    if(e.value != ""){
        if(parseInt(e.value) < parseInt(e.min)){
            e.value = e.min;
        }
        if(parseInt(e.value) > parseInt(e.max)){
            e.value = e.max;
        }
    }
}
