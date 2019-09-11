function toggleConnexion() {
  var Part_1 = document.getElementById("ConnexionForm");
  var Part_2 = document.getElementById("InscriptionForm");
  Part_1.style.display = "block";
  Part_2.style.display = "none";
}

function toggleInscription() {
  var Part_1 = document.getElementById("ConnexionForm");
  var Part_2 = document.getElementById("InscriptionForm");
  Part_1.style.display = "none";
  Part_2.style.display = "block";
}

function toggleRegisterStudent() {
  var Part_1 = document.getElementById("studentRegister");
  var Part_2 = document.getElementById("coachRegister");
  Part_1.style.display = "block";
  Part_2.style.display = "none";
}

function toggleRegisterCoach() {
  var Part_1 = document.getElementById("studentRegister");
  var Part_2 = document.getElementById("coachRegister");
  Part_1.style.display = "none";
  Part_2.style.display = "block";

  document.getElementById("French_3").checked = true;
  document.getElementById("Dutch_3").checked = true;
  document.getElementById("English_3").checked = true;
}

function checkPass(){
  pass = document.getElementById("passwd").value;
  passConf = document.getElementById("passwdConf").value;
  if(pass == passConf && pass.length >= 8){
    document.getElementById("passwdM").style.display = "block";
    document.getElementById("passwdNM").style.display = "none";
  }
  else{
    document.getElementById("passwdM").style.display = "none";
    document.getElementById("passwdNM").style.display = "block";
  }

  if(pass != passConf){
    document.getElementById("errorLab").innerHTML = "Les mots de passe ne sont pas identiques !";
  }
  else if(pass.length < 8){
    document.getElementById("errorLab").innerHTML = "Le mot de passe est trop court !";
  }
  else{
    document.getElementById("errorLab").innerHTML = "";
    return true;
  }
  return false;
}

function checkCoordinates(){
  address = document.getElementById("Address"    ).value != "";
  mail    = validateEmail(document.getElementById("mail").value);
  phone    = document.getElementById("phoneNumber").value != "";

  if(!mail){
    document.getElementById("mailError").innerHTML = "Cette addresse mail n'est pas correcte !";
  }else{
    document.getElementById("mailError").innerHTML = "";
  }
  return phone && address && mail;
}

function checkNames(){
  name = document.getElementById("name") != "";
  firstName = document.getElementById("firstName") != "";
  tutorName = document.getElementById("tutorName") != "";
  tutorFirstName = document.getElementById("tutorFirstName") != "";

  return name && firstName && tutorName && tutorFirstName;
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function checkBirth(){
  birthDate = document.getElementById("birthDate").value != "";
  return birthDate;
}

function checkCourses(){
  math = document.getElementById("checkMath"     ).checked;
  chem = document.getElementById("checkChemistry").checked;
  phys = document.getElementById("checkPhysics"  ).checked;
  fren = document.getElementById("checkFrench"   ).checked;

  if(!math && !chem && !phys && !fren){
    return false;
  }
  return true;
}

function validate(){
  if(checkPass() && checkNames() && checkBirth() && checkCoordinates() && checkCourses()){
    document.getElementById("registerErrors").innerHTML = "";
    return true;
  }
  document.getElementById("registerErrors").innerHTML = "Certains champs obligatoires n'ont pas été remplis ou le mot de passe n'est pas correct !";
  return false;
}

//COACH CHECKS

function checkC_Pass(){
  pass = document.getElementById("C_passwd").value;
  passConf = document.getElementById("C_passwdConf").value;
  if(pass == passConf && pass.length >= 8){
    document.getElementById("C_passwdM").style.display = "block";
    document.getElementById("C_passwdNM").style.display = "none";
  }
  else{
    document.getElementById("C_passwdM").style.display = "none";
    document.getElementById("C_passwdNM").style.display = "block";
  }

  if(pass != passConf){
    document.getElementById("C_errorLab").innerHTML = "Les mots de passe ne sont pas identiques !";
  }
  else if(pass.length < 8){
    document.getElementById("C_errorLab").innerHTML = "Le mot de passe est trop court !";
  }
  else{
    document.getElementById("C_errorLab").innerHTML = "";
    return true;
  }
  return false;
}

function checkC_Coordinates(){
  address = document.getElementById("C_Address"    ).value != "";
  mail    = validateEmail(document.getElementById("C_mail").value);
  phone   = document.getElementById("C_phoneNumber").value != "";
  iban    = document.getElementById("C_IBAN").value != "";

  if(!mail){
    document.getElementById("C_mailError").innerHTML = "Cette addresse mail n'est pas correcte !";
  }else{
    document.getElementById("C_mailError").innerHTML = "";
  }
  return phone && address && mail && iban;
}

function checkC_Names(){
  name = document.getElementById("C_name") != "";
  firstName = document.getElementById("C_firstName") != "";

  return name && firstName;
}

function checkC_Birth(){
  birthDate = document.getElementById("C_birthDate");
  console.log(birthDate.value);

  return true;
}

function C_validate(){
  if(checkC_Pass() && checkC_Names() && checkC_Birth() && checkC_Coordinates()){
    document.getElementById("C_registerErrors").innerHTML = "";
    return true;
  }
  document.getElementById("C_registerErrors").innerHTML = "Certains champs obligatoires n'ont pas été remplis ou le mot de passe n'est pas correct !";
  return false;
}
