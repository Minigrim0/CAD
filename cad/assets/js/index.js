var currentTime = 0;
$("#Alerts_div").collapse('show');
history.pushState('', 'CAD', '/');

var IntervalID = setInterval(
  function checkAlerts(){
    currentTime += 0.1;
    if(currentTime > 5){
      $("#Alerts_div").collapse('hide');
      clearInterval(IntervalID);
    }
  }
, 100);
