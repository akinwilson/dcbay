var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');


var form = document.getElementById('payment-form');



// using jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


form.addEventListener('submit', function(ev) {
  ev.preventDefault();

  var custName = document.getElementById("custName").value;
  var custNameLast = document.getElementById("custNameLast").value;
  var custAdd = document.getElementById("custAdd").value;
  var counrty = document.getElementById("country").value;
  var county = document.getElementById("county").value;
  var postCode = document.getElementById("postCode").value;
  var email = document.getElementById("email").value;
  var city = document.getElementById("city").value;
  var csrftoken = getCookie('csrftoken');
  
  

  
  $.ajax({
    type: "POST",
    credentials: "include",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      'X-CSRFToken': csrftoken,
    },
    // this works for local deployment, deploying django server locally 
    url: "http://localhost:1337/orders/add/",
    data: {
      order_key: clientsecret,
      first_name: custName, 
      last_name: custNameLast,
      address_line_1: custAdd, 
      counrty: counrty,
      county: county, 
      postcode: postCode,
      email: email, 
      city: city, 
      csrfmiddlewaretoken: csrftoken,
      action: "post",
    },
    success: function (json) {
      window.location.replace("http://localhost:1337/payment/orderplaced/");

    },
    error: function (xhr, errmsg, err) {
      console.log("error");
      console.log(xhr);
      console.log(errmsg);
    },
  });



});
