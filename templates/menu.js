function setMenu(id)
{
    var select = document.getElementById(id);
    for(var i=0;i<=10;i++){
    var opt = document.createElement("option");
    opt.value=i;
    opt.innerHTML=i;
    select.appendChild(opt);
    }
}

function setProperty()
{
    var select = document.getElementById('property_type');
    var items = ['Flat', 'Studio', 'House']
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
    var items = ['unfurnished', 'part furnished', 'furnished']
    for(var i=0;i<items.length;i++){
        var opt = document.createElement("option");
        opt.value=i;
        opt.innerHTML=items[i];
        select.appendChild(opt);
    }
}