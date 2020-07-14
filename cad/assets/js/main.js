function toggleRegisterStudent() {
    document.getElementById("studentRegister").style.display = "block";;
    document.getElementById("AsStudent").classList.add("active");
    document.getElementById("coachRegister").style.display = "none";
    document.getElementById("AsCoach").classList.remove("active");
}

function toggleRegisterCoach() {
    document.getElementById("studentRegister").style.display = "none";
    document.getElementById("AsStudent").classList.remove("active");
    document.getElementById("coachRegister").style.display = "block";
    document.getElementById("AsCoach").classList.add("active");

    document.getElementById("French_3").checked = true;
    document.getElementById("Dutch_3").checked = true;
    document.getElementById("English_3").checked = true;
}

//Student checks

function checkPass() {
    pass = document.getElementById("passwd").value;
    passConf = document.getElementById("passwdConf").value;
    if (pass == passConf && pass.length >= 8) {
        document.getElementById("passwdM").style.display = "block";
        document.getElementById("passwdNM").style.display = "none";
    } else {
        document.getElementById("passwdM").style.display = "none";
        document.getElementById("passwdNM").style.display = "block";
    }

    if (pass != passConf) {
        document.getElementById("notGoodPass").innerHTML = "Les mots de passe ne sont pas identiques !";
    } else if (pass.length == 0) {
        document.getElementById("notGoodPass").innerHTML = "ce champ est obligatoire !";
    } else if (pass.length < 8) {
        document.getElementById("notGoodPass").innerHTML = "Le mot de passe est trop court !";
    } else {
        document.getElementById("notGoodPass").innerHTML = "";
        return true;
    }
    return false;
}

function checkCoordinates() {
    //phoneno = /^\(?([0-9]{3,4})\)?[/. ]{,1}?([0-9]{2})?[/. ]{,1}?([0-9]{2})?[/. ]{,1}?([0-9]{2})$/;
    //phone = document.getElementById("phoneNumber").value.match(phoneno);
    phone = true; //phone == null ? false : true;

    address = document.getElementById("Address").value != "";
    mail = validateEmail(document.getElementById("mail").value);
    courses = document.getElementById("math").checked
        || document.getElementById("chemistry").checked
        || document.getElementById("physics").checked
        || document.getElementById("french").checked;

    document.getElementById("notGoodPhone").innerHTML = "";
    document.getElementById("notGoodAddress").innerHTML = "";
    document.getElementById("mailError").innerHTML = "";
    document.getElementById("notGoodCourse").innerHTML = "";
    if (!phone) document.getElementById("notGoodPhone").innerHTML = "Ce numero de telephone n'est pas correct";
    if (!address) document.getElementById("notGoodAddress").innerHTML = "Ce champ est obligatoire !";
    if (!mail) document.getElementById("mailError").innerHTML = "Cette adresse mail n'est pas correcte !";
    if (!courses) document.getElementById("notGoodCourse").innerHTML = "Vous devez choisir au moins un cours !";

    return phone
        && address
        && mail
        && courses;
}

function checkNames() {
    firstName = document.getElementById("firstName").value != "";
    lastName = document.getElementById("lastName").value != "";
    tutorFirstName = document.getElementById("tutorFirstName").value != "";
    tutorLastName = document.getElementById("tutorLastName").value != "";

    document.getElementById("notGoodFirstName").innerHTML = "";
    document.getElementById("notGoodLastName").innerHTML = "";
    document.getElementById("notGoodTutorFirstName").innerHTML = "";
    document.getElementById("notGoodTutorLastName").innerHTML = "";
    if(!firstName) document.getElementById("notGoodFirstName").innerHTML = "Ce champ est obligatoire !";
    if(!lastName) document.getElementById("notGoodLastName").innerHTML = "Ce champ est obligatoire !";
    if(!lastName) document.getElementById("notGoodTutorFirstName").innerHTML = "Ce champ est obligatoire !";
    if(!lastName) document.getElementById("notGoodTutorLastName").innerHTML = "Ce champ est obligatoire !";

    return lastName && firstName && tutorLastName && tutorFirstName;
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function validate() {
    var checked = checkPass();
    checked = checkNames()       && checked;
    checked = checkCoordinates() && checked;
    document.getElementById("registerErrors").innerHTML = "";
    if (!checked) document.getElementById("registerErrors").innerHTML = "\
        Certains champs obligatoires n'ont pas été correctement remplis ou \
        les mots de passe ne correspondent pas !";
    return checked;
}

//COACH CHECKS

function checkC_Pass() {
    pass = document.getElementById("C_password").value;
    passConf = document.getElementById("C_passConf").value;

    if (pass == passConf && pass.length >= 8) {
        document.getElementById("C_passMatch").style.display = "block";
        document.getElementById("C_passNoMatch").style.display = "none";
    } else {
        document.getElementById("C_passMatch").style.display = "none";
        document.getElementById("C_passNoMatch").style.display = "block";
    }

    if (pass != passConf) {
        document.getElementById("C_notGoodPass").innerHTML = "Les mots de passe ne sont pas identiques !";
    } else if (pass.length == 0) {
        document.getElementById("C_notGoodPass").innerHTML = "ce champ est obligatoire !";
    } else if (pass.length < 8) {
        document.getElementById("C_notGoodPass").innerHTML = "Le mot de passe est trop court !";
    } else {
        document.getElementById("C_notGoodPass").innerHTML = "";
        return true;
    }
    return false;
}

function checkC_Coordinates() {
    //phoneno = /^\(?([0-9]{3,4})\)?[/. ]?([0-9]{2})?[/. ]?([0-9]{2})?[/. ]?([0-9]{2})$/;
    //phone = document.getElementById("C_phoneNumber").value.match(phoneno);
    //phone = phone == null ? false : true;
    phone = true;
    address = document.getElementById("C_Address").value != "";
    mail = validateEmail(document.getElementById("C_mail").value);
    iban = document.getElementById("C_IBAN").value != "";
    natreg_number = document.getElementById("C_IBAN").value != "";
    courses = document.getElementById("C_math").checked
        || document.getElementById("C_chemistry").checked
        || document.getElementById("C_physics").checked
        || document.getElementById("C_french").checked;
    school = document.getElementById("C_School").value != "";

    //document.getElementById("C_notGoodPhone").innerHTML = "";
    document.getElementById("C_notGoodAddress").innerHTML = "";
    document.getElementById("C_mailError").innerHTML = "";
    document.getElementById("C_notGoodIBAN").innerHTML = "";
    document.getElementById("C_notGoodNRN").innerHTML = "";
    document.getElementById("C_notGoodCourse").innerHTML = "";
    document.getElementById("C_notGoodSchool").innerHTML = "";
    //if (!phone) document.getElementById("C_notGoodPhone").innerHTML = "Ce numero de telephone n'est pas correct";
    if (!address) document.getElementById("C_notGoodAddress").innerHTML = "Ce champ est obligatoire !";
    if (!mail) document.getElementById("C_mailError").innerHTML = "Cette addresse mail n'est pas correcte !";
    if (!iban) document.getElementById("C_notGoodIBAN").innerHTML = "Ce champ est obligatoire !";
    if (!natreg_number) document.getElementById("C_notGoodNRN").innerHTML = "Ce champ est obligatoire !";
    if (!courses) document.getElementById("C_notGoodCourse").innerHTML = "Vous devez choisir au moins un cours !";
    if (!school) document.getElementById("C_notGoodSchool").innerHTML = "Ce champ est obligatoire !";

    return phone
        && address
        && mail
        && iban
        && natreg_number
        && courses
        && school;
}

function checkC_Names() {
    var lastName = document.getElementById("C_lastName").value != "";
    var firstName = document.getElementById("C_firstName").value != "";

    if (!lastName) {
        document.getElementById("C_notGoodLastName").innerHTML = "Ce champ est obligatoire !";
    }
    if (!firstName) {
        document.getElementById("C_notGoodFirstName").innerHTML = "Ce champ est obligatoire !";
    }

    return lastName && firstName;
}

function C_validate() {
    var checked = checkC_Pass();
    checked = checkC_Names()       && checked;
    checked = checkC_Coordinates() && checked;
    if (checked) {
        return true;
    }
    document.getElementById("C_registerErrors").innerHTML = "Certains champs \
        obligatoires n'ont pas été remplis correctement ou les mots de passe ne \
        correspondent pas !";
    return false;
}
