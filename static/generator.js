function vidGen(dataString,element){
    element.style.opacity="0.5";

    source = document.getElementById("source").value;
    if(source == "realtor"){
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/gen/realtor", true);

        // Send the proper header information along with the request
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        xhr.onreadystatechange = () => {

        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            alert("generation done"+" "+xhr.responseText);
            json_ = JSON.parse(xhr.responseText);
            window.open('/'+json_.output)
            element.style.opacity="1";
        }
        };
        xhr.send("data="+dataString);
    }
    else if(source == "zillow"){
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/gen/zillow", true);

        // Send the proper header information along with the request
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        xhr.onreadystatechange = () => {

        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            alert("generation done"+" "+xhr.responseText);
            json_ = JSON.parse(xhr.responseText);
            window.open('/'+json_.output)
            element.style.opacity="1";
        }
        };
        xhr.send("data="+dataString);
    }
    
    
}
function onclickthing(element){
    dstring = element.getAttribute("data")
    vidGen(dstring,element)

}