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
let locations = [[41.729838, -88.3559956], [28.0109254, -82.1564415], [28.570529, -80.803546], [34.031484, -118.2454195], [28.2542709, -81.4815331], [32.5983122, -117.0826517], [41.7624567, -87.800615], [35.6283557, -78.4295114], [34.1462203, -118.7469619], [32.7531176, -117.2035094], [31.1117403, -97.7193638], [34.0081591, -84.6058197], [37.3228883, -121.9753073], [30.85732059999999, -83.9430149], [33.055356, -84.99843249999999], [38.5929979, -95.26847769999999], [42.40013, -88.182482], [34.474161, -117.283314], [37.5911821, -77.50459149999999], [40.2402567, -111.6669342], [40.3245277, -75.6177139], [40.2610136, -76.853853], [30.18978289999999, -93.21810029999999], [14.5945266, -90.5638594], [38.4633234, 27.1285384], [53.41499779999999, -113.4789228], [34.179811, -119.161768], [28.1403311, -81.9386512], [28.7555264, -100.4943083], [39.63344540000001, -78.220372], [35.3687522, -119.0179752], [34.0706966, -117.4368604], [32.6599034, -117.0913836], [20.661489, -103.313798], [33.915876, -118.1577531], [38.411307, -82.371599], [40.5735733, -74.1149848], [25.7996805, -80.314948], [37.2106268, -93.311699], [42.8910761, -71.3276388], [41.2235782, -96.1205209], [-2.1332914, -79.8955983], [13.0832983, -59.5666918], [36.778261, -119.4179324], [30.2376083, -90.91255819999999], [28.5467922, -81.65762289999999], [28.527801, -81.4026009], [34.1728948, -84.7931557], [39.8088828, -75.0932179], [39.999157, -82.03813819999999], [40.052292, -76.360643], [34.0556793, -117.717658], [32.420214, -104.236445], [33.8039938, -117.8634689], [41.0299819, -73.788641], [35.1701391, -89.88092809999999], [33.9525, -118.1830556], [42.9367255, -87.9497318], [42.0139132, -88.1108515], [39.2157699, -84.5856226], [42.3654286, -89.0372921], [29.8931376, -90.1204733], [26.1509427, -80.1948804], [30.26483, -89.75084299999999], [21.3069444, -157.8583333], [4.6156856, -74.10243], [34.1059916, -117.629603], [41.5030148, -74.4098787], [38.05646309999999, -97.9304099], [39.050445, -82.638514], [41.1522041, -81.3861014], [33.6521098, -117.9193393], [28.0569495, -81.81410629999999], [35.12271399999999, -85.237529], [42.0285445, -87.7859829], [39.7565616, -94.8038963], [32.7065472, -117.1364732], [39.0784844, -94.3851074], [41.692682, -87.757393], [39.52535049999999, -119.7893757], [35.4044952, -97.5285497], [9.0160108, -79.5230351], [41.7709558, -87.7221351], [34.23959019999999, -118.577563], [34.2122422, -118.4664307], [40.8624272, -73.0547551], [10.6369373, -61.3912739], [35.9717844, -83.2538416], [40.62032960000001, -122.3711112], [38.4245052, -122.7130732], [40.340174, -76.4151708], [37.6645431, -97.3714675], [27.4566305, -81.4239685], [18.3243955, -66.2421509], [36.2616889, -86.74174900000001], [31.9331867, -106.4386317], [40.8019903, -73.6508836], [34.1089772, -117.9369796], [29.0853574, -110.9709239], [30.5135665, -81.6218749], [17.7308538, -64.7381663], [36.6702863, -121.6529632], [37.920077, -121.684951], [41.558514, -90.630408], [27.8007302, -97.670559], [38.8779634, -90.1062291], [33.940997, -84.530663], [38.93464, -94.7471655], [40.9900071, -75.2157096], [38.8347911, -97.6254088], [37.9797188, -89.05289650000002], [39.938472, -75.075608], [33.8945645, -80.4449113], [40.6953909, -73.91721199999999], [39.0236336, -96.82984019999999], [35.399784, -77.9822147], [41.8520584, -87.7047042], [34.0923519, -117.9071895], [26.6231597, -80.07029039999999], [44.5241287, -89.5486221], [33.9856006, -117.7131168], [32.2396709, -90.16650299999999], [40.2292494, -111.6613121], [33.7477951, -116.9899826], [36.3277465, -119.266468], [21.3866667, -158.0091667], [41.9379706, -88.0949991], [38.5161106, -90.33761439999999], [9.9485686, -84.0987244], [33.8020718, -117.8636897], [35.0880442, -78.9075005], [36.904854, -93.573196], [40.7915058, -96.72630459999999], [41.4183712, -81.7233086], [33.9394329, -117.9449144], [33.7623336, -78.9254827], [41.5061416, -87.8481063], [36.0628681, -87.3756449], [41.4626648, -87.69820849999999], [38.274153, -81.748649], [37.4206314, -121.8883972], [39.2594166, -84.82015249999999], [30.5046294, -92.0720273], [41.9076956, -87.8920002], [28.2449626, -82.187333], [33.9987395, -96.4688812], [37.989178, -100.8815472], [37.841888, -89.0250466], [37.9210794, -91.7798976], [29.7364749, -95.61231989999999], [32.5686443, -96.9733871], [40.727781, -89.57470699999999], [33.7255867, -84.7608721], [29.7962322, -95.5285068], [36.8213043, -76.0651625], [33.9911812, -118.3957729], [36.19926299999999, -86.515199], [34.4361087, -118.5771537], [36.9887994, -119.8930678], [33.9174936, -118.1063702], [34.2357649, -119.1709357], [34.7400125, -86.59600879999999], [34.2545549, -119.235283], [42.3426823, -87.8733165], [-12.0824936, -77.0278763], [34.221595, -118.4850007], [28.539859, -81.4084041], [28.3174456, -81.4007233], [32.8341331, -117.154335], [35.9998001, -83.96232719999999], [35.0804447, -80.6607952], [36.1848698, -94.1335469], [40.9262273, -91.4056737], [36.095654, -86.7620146], [37.1171616, -121.6332566], [36.5718255, -82.1950263], [42.1730052, -87.794449], [26.6558721, -81.8485862], [35.6219091, -120.6913188], [30.7077379, -88.1208127], [27.2992337, -82.525475], [35.1879639, -84.8711165], [39.8009491, -104.9807861], [38.9421872, -95.24227139999999], [29.5731622, -90.6851065], [33.3639696, -111.800856], [38.8681782, -94.6618673], [39.02009169999999, -122.9139474], [33.7537458, -85.7863699], [38.5350354, -89.9613268], [28.9772896, -80.8982101], [38.896685, -99.3163934], [41.6010912, -87.6038983], [], [], [], [], [], []]
let locAddresses
let vendors

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

        //Aunex Logo
        var logo = document.createElement("img");
        logo.src = "static/main/aunex-logo-sml-01.png";
        logo.classList.add('locationPanelLogo')
        locationPanel.appendChild(logo);

        //location phone number
        if (placeResult.formatted_phone_number) {
            let phoneNumber = document.createElement('div');
            let phoneLink = document.createElement('a');
            phoneLink.href = 'tel:' + placeResult.formatted_phone_number;
            phoneLink.innerHTML = 'Phone: ' + placeResult.formatted_phone_number;
            phoneNumber.classList.add('details');
            phoneNumber.appendChild(phoneLink);
            locationPanel.appendChild(phoneNumber);
        }

        //location international phone number
        if (placeResult.international_phone_number) {
            let iPhoneNumber = document.createElement('div');
            iPhoneNumber.classList.add('details');
            iPhoneNumber.textContent = 'International: ' + placeResult.international_phone_number;
            locationPanel.appendChild(iPhoneNumber);
        }

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
