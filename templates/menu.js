function setMenu(id)
{
    var select = document.getElementById(id);
    for(var i=0;i<=8;i++){
    var opt = document.createElement("option");
    opt.value=i;
    opt.innerHTML=i;
    select.appendChild(opt);
    }
}


function setProperty()
{
    var select = document.getElementById('property_type');
    var items = ['Detached House', 'Semi-detached House', 'Terraced House', 'Townhouse', 'Bungalow', 'Studio', 'Flat', 'Maisonette']
    for(var i=0;i<items.length;i++){
        var opt = document.createElement("option");
        opt.value=i;
        opt.innerHTML=items[i];
        select.appendChild(opt);
    }
}

function setPreference()
{
    var select = document.getElementById('property_type');
    var items = ['House','Bungalow', 'Studio', 'Flat']
    for(var i=0;i<items.length;i++){
        var opt = document.createElement("option");
        opt.value=i;
        opt.innerHTML=items[i];
        select.appendChild(opt);
    }
}

function setFurniture()
{
    var select = document.getElementById('furniture_state');
    var items = ['Unfurnished', 'Part furnished', 'Furnished']
    for(var i=0;i<items.length;i++){
        var opt = document.createElement("option");
        opt.value=i;
        opt.innerHTML=items[i];
        select.appendChild(opt);
    }
}