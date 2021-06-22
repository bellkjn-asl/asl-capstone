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

function clearSelectData(select) {
  var length = select.options.length;
  for (i = length - 1; i >= 0; i--) {
    select.options[i] = null;
  }
}

function setSelectData(selectId, data, defaultText) {
  const select = document.getElementById(selectId);

  clearSelectData(select);

  var opt = document.createElement("option");
  opt.value = 0;
  opt.innerHTML = defaultText;
  opt.disabled = true;
  opt.hidden = true;
  opt.selected = true;
  select.appendChild(opt);

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

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/predict/" + path);
  xhr.setRequestHeader('content-type', 'application/json;charset=UTF-8');
  xhr.onload = function () {
    const response = xhr.responseText;
    document.getElementById("resultText").innerHTML = response;
  };

  xhr.send(JSON.stringify(data));

}


function submitUsedcarClick() {
  console.log('submitUsedcarClick');

  var data = {
    tax: document.getElementById("taxText").value,
    mileage: document.getElementById("mileageText").value,
    carYear: document.getElementById("carYearText").value,
    maker: getSelectedText("maker-list"),
    model: getSelectedText("model-list"),
    fuelType: getSelectedText("fuelType-list"),
    transmission: getSelectedText("transmission-list"),
    mpg: document.getElementById("mpgSlider").value,
    engine: document.getElementById("enginesizeSlider").value
  }

  submitClick('usedcar', data);
}

function submitCreditClick(){
  console.log('submitCreditClick');

  var data = {
    gender: document.getElementById("gender-list").value,
    work_phone: document.getElementById("workPhone-list").value,
    phone: document.getElementById("phone-list").value,
    email: document.getElementById("email-list").value,

    income_type: getSelectedText("incomeType-list"),
    edu_type: getSelectedText("eduType-list"),
    family_type: getSelectedText("familyType-list"),
    house_type: getSelectedText("houseType-list"),
    occyp_type: getSelectedText("occypType-list"),
    car: getSelectedText("car-list"),
    reality: getSelectedText("reality-list"),
    mobile: getSelectedText("mobile-list"),

    income_total: document.getElementById("incomeTotalText").value,
    family_size: document.getElementById("familySizeText").value,
    begin_month: document.getElementById("beginMonthText").value,
    child_num: document.getElementById("childNumText").value,
    DAYS_BIRTH: document.getElementById("daysBirthText").value,
    DAYS_EMPLOYED: document.getElementById("daysEmployedText").value,
  }

  submitClick('creditcard', data);

}