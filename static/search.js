// /search?source=realtor&city=Seattle&state=WA

function AddSearchResult(title,image,text){

  html = '\
    <div class="card">\
    <img class="card-img-top" src="'+image+'">\
      <div class="card-body">\
      <h5 class="card-title">'+title+'</h5>\
      <p class="card-text">'+text+'</p>\
      </div>\
    </div>\
  '
  document.getElementById("results").innerHTML =document.getElementById("results").innerHTML+html

}
async function searchIt(){
  var source = document.getElementById("source").value;
  var city = document.getElementById("city").value;
  var state = document.getElementById("state").value;
  const page = await fetch("/search?source="+source+"&city="+city+"&state="+state)
  const pageJson = await page.json()
  document.getElementById("results").innerHTML = ""
  if (source=="zillow") {
    for (var i = 0; i < pageJson.out.length; i++) {
      var current = pageJson.out[i]
      AddSearchResult(current.address,current.imgSrc,current.hdpData.homeInfo.price.toLocaleString())
    }

  }
  if (source=="realtor") {
    for (var i = 0; i < pageJson.out.length; i++) {
      var current = pageJson.out[i]
      console.log(current)
    }

  }
}
