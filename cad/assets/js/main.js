function toggleConnexion() {
    document.getElementById("ConnexionForm").style.display = "block";
    document.getElementById("InscriptionForm").style.display = "none";
}

function toggleInscription() {
    document.getElementById("ConnexionForm").style.display = "none";
    document.getElementById("InscriptionForm").style.display = "block";
}

function toggleRegisterStudent() {
    document.getElementById("studentRegister").style.display = "block";;
    document.getElementById("coachRegister").style.display = "none";
}

function toggleRegisterCoach() {
    document.getElementById("studentRegister").style.display = "none";
    document.getElementById("coachRegister").style.display = "block";

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
        document.getElementById("errorLab").innerHTML = "Les mots de passe ne sont pas identiques !";
    } else if (pass.length < 8) {
        document.getElementById("errorLab").innerHTML = "Le mot de passe est trop court !";
    } else {
        document.getElementById("errorLab").innerHTML = "";
        return true;
    }
    return false;
}

function checkCoordinates() {
    address = document.getElementById("Address").value != "";
    mail = validateEmail(document.getElementById("mail").value);
    phone = document.getElementById("phoneNumber").value != "";

    if (!mail) {
        document.getElementById("mailError").innerHTML = "Cette addresse mail n'est pas correcte !";
    } else {
        document.getElementById("mailError").innerHTML = "";
    }
    return phone && address && mail;
}

function checkNames() {
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

function checkBirth() {
    birthDate = document.getElementById("birthDate").value != "";
    return birthDate;
}

function checkCourses() {
    math = document.getElementById("checkMath").checked;
    chem = document.getElementById("checkChemistry").checked;
    phys = document.getElementById("checkPhysics").checked;
    fren = document.getElementById("checkFrench").checked;

    if (!math && !chem && !phys && !fren) {
        return false;
    }
    return true;
}

function validate() {
    if (checkPass() && checkNames() && checkBirth() && checkCoordinates() && checkCourses()) {
        document.getElementById("registerErrors").innerHTML = "";
        return true;
    }
    document.getElementById("registerErrors").innerHTML = "Certains champs obligatoires n'ont pas été remplis ou le mot de passe n'est pas correct !";
    return false;
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
    phoneno = /^\(?([0-9]{3,4})\)?[/. ]?([0-9]{2})?[/. ]?([0-9]{2})?[/. ]?([0-9]{2})$/;
    address = document.getElementById("C_Address").value != "";
    mail = validateEmail(document.getElementById("C_mail").value);
    phone = document.getElementById("C_phoneNumber").value.match(phoneno);
    iban = document.getElementById("C_IBAN").value != "";
    natreg_number = document.getElementById("C_IBAN").value != "";
    courses = document.getElementById("C_math").checked
        || document.getElementById("C_chemistry").checked
        || document.getElementById("C_physics").checked
        || document.getElementById("C_french").checked;
    school = document.getElementById("C_School").value != "";
    school = document.getElementById("C_IBAN").value != "";

    document.getElementById("C_mailError").innerHTML = "";
    document.getElementById("C_notGoodNRN").innerHTML = "";
    document.getElementById("C_notGoodAddress").innerHTML = "";
    document.getElementById("C_notGoodPhone").innerHTML = "";
    document.getElementById("C_notGoodCourse").innerHTML = "";
    document.getElementById("C_notGoodSchool").innerHTML = "";
    document.getElementById("C_notGoodIBAN").innerHTML = "";
    if (!mail) document.getElementById("C_mailError").innerHTML = "Cette addresse mail n'est pas correcte !";
    if (!natreg_number) document.getElementById("C_notGoodNRN").innerHTML = "Ce champ est obligatoire !";
    if (!address) document.getElementById("C_notGoodAddress").innerHTML = "Ce champ est obligatoire !";
    if (!phone) document.getElementById("C_notGoodPhone").innerHTML = "Ce numero de telephone n'est pas correct";
    if (!phone) document.getElementById("C_notGoodCourse").innerHTML = "Vous devez choisir au moins un cours !";
    if (!phone) document.getElementById("C_notGoodSchool").innerHTML = "Ce champ est obligatoire !";
    if (!phone) document.getElementById("C_notGoodIBAN").innerHTML = "Ce champ est obligatoire !";

    return phone && address && mail && iban;
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

function checkC_Birth() {
    birthDate = document.getElementById("C_birthDate");
    if (birthDate.value == ""){
        document.getElementById("C_notGoodBirth").innerHTML = "Ce champ est obligatoire !";
        return false
    }
    document.getElementById("C_notGoodBirth").innerHTML = "";

    return true;
}

function C_validate() {
    var checked = checkC_Pass();
    checked = checkC_Names()       && checked;
    checked = checkC_Birth()       && checked;
    checked = checkC_Coordinates() && checked;
    if (checked) {
        return true;
    }
    document.getElementById("C_registerErrors").innerHTML = "Certains champs \
        obligatoires n'ont pas été remplis ou les mots de passe ne \
        correspondent pas !";
    return false;
}
