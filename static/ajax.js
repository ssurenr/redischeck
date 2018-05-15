function getKey() {

      var fd = new FormData();

      txtFetchKey = document.getElementById("fetchkey").value;
      fd.append("fetchkey",txtFetchKey);


      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
            if (response.found) {
                document.getElementById("fetchedvalue").innerHTML = response.value;
                document.getElementById("fetchedtime").innerHTML = response.time;
            } else {
                document.getElementById("fetchedvalue").classList.add("bg-danger");
                document.getElementById("fetchedvalue").innerHTML = "Key not found";
                document.getElementById("fetchedtime").innerHTML = "Not applicable";
            }
        }
      };
      xhttp.open("POST", "/api/fk");
      xhttp.send(fd);
      console.log(xhttp.readyState);
      console.e

  }

function performTest() {
//    var pdata = new FormData();
//
//
//     var perf_xhttp = new XMLHttpRequest();
//      perf_xhttp.onreadystatechange = function() {
//            if (this.readyState == 4 && this.status == 200) {
//            response = JSON.parse(this.responseText);
//            if (response.found) {
//                document.getElementById("perf_result").innerHTML = response.name;
//            } else {
//                document.getElementById("perf_result").innerHTML = "No DATA";
//            }
//        }
//      };
//
//    perf_xhttp.open("POST", /pt);
//    perf_xhttp.send(pdata);
//    console.log(perf_xhttp.readyState);
}
