function showspinneresp(){
    document.getElementById('showspinneresp').style.display='';
    document.getElementById('downloadesp').style.display='none';
    setTimeout(function removespinner(){
    document.getElementById('showspinneresp').style.display='none';
    document.getElementById('downloadesp').style.display='';
    },120)
}
function showspinnering(){
    document.getElementById('showspinnering').style.display='';
    document.getElementById('downloadesp').style.display='none';
    setTimeout(function removespinner(){
    document.getElementById('showspinnering').style.display='none';
    document.getElementById('downloadesp').style.display='';
    },120)
}