function updateYearInput(val) {
  document.getElementById("carYearSlider").value = val;
  document.getElementById("carYearText").value = val;
}

function updateMpgInput(val) {
  document.getElementById("mpgSlider").value = val;
  document.getElementById("mpgText").value = val;
}

function updateEngineSizeInput(val) {
  document.getElementById("enginesizeSlider").value = val;
  document.getElementById("enginesizeText").value = val;
}

function updateFamilySizeInput(val){
  document.getElementById("familySizeSlider").value = val;
  document.getElementById("familySizeText").value = val;
}

function updateBeginMonthInput(val){
  document.getElementById("beginMonthSlider").value = val;
  document.getElementById("beginMonthText").value = val;
}

function updateChildNumInput(val){
  document.getElementById("childNumSlider").value = val;
  document.getElementById("childNumText").value = val;
}

function updateDaysBirthInput(val){
  document.getElementById("daysBirthSlider").value = val;
  document.getElementById("daysBirthText").value = val;
}

function updateDaysEmployedInput(val){
  document.getElementById("daysEmployedSlider").value = val;
  document.getElementById("daysEmployedText").value = val;
}

function updateMileageInput(val){
  document.getElementById("mileageSlider").value = val;
  document.getElementById("mileageText").value = val;
}

function updateTaxInput(val){
  document.getElementById("taxSlider").value = val;
  document.getElementById("taxText").value = val;
}

function updateIncomeTotalTextInput(val){
  document.getElementById("incomeTotalSlider").value = val;
  document.getElementById("incomeTotalText").value = val;
}


function clearSelectData(select) {
  var length = select.options.length;
  for (i = length - 1; i >= 0; i--) {
    select.options[i] = null;
  }
}

function setSelectData(selectId, data, defaultText) {
  const select = document.getElementById(selectId);

  clearSelectData(select);

  // var opt = document.createElement("option");
  // opt.value = 0;
  // opt.innerHTML = defaultText;
  // opt.disabled = true;
  // opt.hidden = true;
  // opt.selected = true;
  // select.appendChild(opt);

  for (i = 0; i < data.length; i++) {
    var opt = document.createElement("option");
    opt.value = i+1;
    opt.innerHTML = data[i];
    select.appendChild(opt);
  }
}

function getSelectedText(selectId) {
  const select = document.getElementById(selectId);
  return select.options[select.selectedIndex].text;
}

function changeMaker() {
  var makerSel = document.getElementById("maker-list");
  var makerText = makerSel.options[makerSel.selectedIndex].text;

  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/?maker=" + makerText);
  xhr.onload = function () {
    const response = JSON.parse(xhr.responseText);
    setSelectData("model-list", response, 'Choose model');
  };
  xhr.send(null);
}

function changeModel() {
  // var makerSel = document.getElementById("maker-list");
  // var makerText = makerSel.options[makerSel.selectedIndex].text;

  // var modelSel = document.getElementById("model-list");
  // var modelText = modelSel.options[modelSel.selectedIndex].text;

  // var xhr = new XMLHttpRequest();
  // xhr.open("GET", "/?maker=" + makerText + "&model=" + modelText);
  // xhr.onload = function () {
  //   const response = JSON.parse(xhr.responseText);
  //   setSelectData("fuelType-list", response.fuelType, 'Choose fuel type');
  //   setSelectData("transmission-list", response.transmission, 'Choose transmission');
  //   setSelectData("mpg-list", response.mpg, 'Choose mpg');
  //   setSelectData("engine-list", response.engineSize, 'Choose engine size');
  // };
  // xhr.send(null);
}

function submitClick(path, data) {
  console.log('submitClick');

  document.getElementById("resultText").innerHTML = "<div class=\"loader\"></div>";

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/predict/" + path);
  xhr.setRequestHeader('content-type', 'application/json;charset=UTF-8');
  xhr.onload = function () {
    const response = xhr.responseText;
    document.getElementById("resultText").innerHTML = response;
  };

  document.getElementById("jsondata").innerHTML = JSON.stringify(data, null, 2);

  xhr.send(JSON.stringify(data));

}

function getFloatElement(id){
  return parseFloat(document.getElementById(id).value)
}

function getIntElement(id){
  return parseInt(document.getElementById(id).value)
}

function getMinusFloatElement(id){
  return getFloatElement(id) * -1
}


function submitUsedcarClick() {
  console.log('submitUsedcarClick');

  maker = getSelectedText("maker-list");

  var data = {
    year: getFloatElement("carYearText"),
    manufacturer: maker,
    engineSize: getFloatElement("enginesizeSlider"),
    mileage: getFloatElement("mileageText"),
    tax: getFloatElement("taxText"),
    mpg: getFloatElement("mpgSlider"),
    model: maker+' '+getSelectedText("model-list"),
    fuelType: getSelectedText("fuelType-list"),
    transmission: getSelectedText("transmission-list"),
  }

  submitClick('usedcar', data);
}

function getDaysEmployed() {
  var ret = getMinusFloatElement('daysEmployedText')
  if( ret == -365243){
    return 0
  } 
  
  return ret
}

function submitCreditClick(){
  console.log('submitCreditClick');

  var data = {
    car: document.getElementById("car-list").value,
    reality: document.getElementById("reality-list").value,
    // mobile: document.getElementById("mobile-list").value,
    gender: document.getElementById("gender-list").value,
    income_total: getFloatElement("incomeTotalText"),
    income_type: getSelectedText("incomeType-list"),
    edu_type: getSelectedText("eduType-list"),
    family_type: getSelectedText("familyType-list"),
    house_type: getSelectedText("houseType-list"),
    work_phone: getIntElement("workPhone-list"),
    phone: getIntElement("phone-list"),
    email: getIntElement("email-list"),
    occyp_type: getSelectedText("occypType-list"),
    family_size: getFloatElement("familySizeText"),
    begin_month: getMinusFloatElement("beginMonthText"),

    child_num: getIntElement("childNumText"),
    DAYS_BIRTH: getMinusFloatElement("daysBirthText"),
    DAYS_EMPLOYED: getDaysEmployed(),
  }

  if(data['DAYS_EMPLOYED'] >= 0){
    data['occyp_type'] = 'Unemployed'
    data['DAYS_EMPLOYED'] = 0
  }

  data['MONTHS_BIRTH'] = Math.floor(data['DAYS_BIRTH'] / 30) 
  data['MONTHS_EMPLOYED'] = Math.floor(data['DAYS_EMPLOYED'] / 30)

  data['ability'] = data['income_total'] / (data['DAYS_BIRTH'] + data['DAYS_EMPLOYED'])
  data['income_mean'] = data['income_total'] / data['family_size']

  data['ID_categorical'] = String(data['DAYS_EMPLOYED']) + '_' 
    + String(data['DAYS_BIRTH']) + '_' 
    + String(data['income_total']) + '_' 
    + String(data['child_num']) + '_' 
    + String(data['work_phone']) + '_' 
    + String(data['phone']) + '_' 
    + String(data['email']) + '_' 
    + String(data['family_size']) + '_' 
    + String(data['gender']) + '_' 
    + String(data['car']) + '_' 
    + String(data['reality']) + '_' 
    + String(data['income_type']) + '_' 
    + String(data['edu_type']) + '_' 
    + String(data['family_type']) + '_' 
    + String(data['house_type']) + '_' 
    + String(data['occyp_type']);


  delete data['child_num'];
  delete data['DAYS_BIRTH'];
  delete data['DAYS_EMPLOYED'];

  submitClick('creditcard', data);

}