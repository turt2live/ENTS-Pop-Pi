var member = {
  newCredit: 0,
  credit: 0,
  deposited: 0,
  cost: 0 // Technically not member info, but whatever
};

var toIdleTimer = null; // when not null then a countdown to 'idle' is pending
var timeoutTime = 15000; // ms

// JQUERY INIT
// ===============================

$(document).ready(function(){
  var socket = io.connect('/pop');
  socket.on('connect', onConnect);
  socket.on('member-swipe', function(credit, cost){
    member.credit = credit;
    member.cost = cost;
    member.deposited = 0;
    onSwipe();
  });
  socket.on('deposit', function(amountDeposited){
    member.deposited += amountDeposited;
    onDeposit();
  });
  socket.on('paid', function(newCredit){
    member.newCredit = newCredit;
    onPaid();
  });
  socket.on('not-found', onMemberNotFound);
});

// SOCKET FUNCTIONS
// ===============================

function onPaid(){
  $("#idle").hide();
  $("#paying").hide();
  $("#thanks").show();
  $("#not-a-member").hide();
  $("#new-credit").html(toCurrency(member.newCredit))
  toIdleTimer = setTimeout(toIdle, timeoutTime);
}

function toIdle(){
  $("#idle").show();
  $("#paying").hide();
  $("#thanks").hide();
  $("#not-a-member").hide();
}

function onConnect(){
  $("#idle").show();
  $("#paying").hide();
  $("#thanks").hide();
  $("#not-a-member").hide();
}

function onDeposit(){
  updateDeposited();
  updateAmountDue();
}

function onSwipe(){
  $("#idle").hide();
  $("#paying").show();
  $("#thanks").hide();
  $("#not-a-member").hide();

  $("#paying-credit").html(toCurrency(member.credit));
  updateAmountDue();
  updateDeposited();

  if (toIdleTimer)
    clearTimeout(toIdleTimer);
}

function onMemberNotFound(){
  $("#idle").hide();
  $("#paying").hide();
  $("#thanks").hide();
  $("#not-a-member").show();
  toIdleTimer = setTimeout(toIdle, timeoutTime);
}

// HELPERS
// ===============================

function updateDeposited(){
  $("#paying-deposited").html(toCurrency(member.deposited));
}

function updateAmountDue(){
  var due = member.cost - member.credit - member.deposited;
  if(due < 0) return;
  $("#paying-amount-due").html(toCurrency(due));
}

function toCurrency(amount){
  var dollars = (amount / 100).toFixed(2);
  var sign = dollars >= 0 ? "$" : "-$";
  return sign + dollars;
}
