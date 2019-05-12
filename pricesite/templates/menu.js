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