function updateAgeInput(val) {
  document.getElementById("ageSlider").value = val;
  document.getElementById("ageText").value = val;
}

function updateWeeksInput(val) {
  document.getElementById("weeksSlider").value = val;
  document.getElementById("weeksText").value = val;
}

function updateYearInput(val) {
  document.getElementById("carYearSlider").value = val;
  document.getElementById("carYearText").value = val;
}
 
function clearSelectData(select) {
  var length = select.options.length;
  for (i = length - 1; i >= 0; i--) {
    select.options[i] = null;
  }
}

function setSelectData(select_id, data) {
  var select = document.getElementById(select_id);

  clearSelectData(select);

  for (i = 0; i < data.length; i++) {
    var opt = document.createElement("option");
    opt.value = i;
    opt.innerHTML = data[i];
    select.appendChild(opt);
  }
}

function changeMaker() {
  var makerSel = document.getElementById("maker-list");

  // select element에서 선택된 option의 text가 저장된다.
  var makerText = makerSel.options[makerSel.selectedIndex].text;

  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/?maker=" + makerText);
  xhr.onload = function () {
    const response = JSON.parse(xhr.responseText);
    setSelectData("model-list", response);
  };
  xhr.send(null);
}

function changeModel() {
  var makerSel = document.getElementById("maker-list");
  var makerText = makerSel.options[makerSel.selectedIndex].text;

  var modelSel = document.getElementById("model-list");
  var modelText = modelSel.options[modelSel.selectedIndex].text;

  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/?maker=" + makerText + "&model=" + modelText);
  xhr.onload = function () {
    const response = JSON.parse(xhr.responseText);
    setSelectData("fuelType-list", response.fuelType);
    setSelectData("transmission-list", response.transmission);
    setSelectData("mpg-list", response.mpg);
    setSelectData("engine-list", response.engineSize);
  };
  xhr.send(null);
}

const submitButton = document.getElementById("submit");
submitButton.addEventListener("click", function (event) {
  const myForm = document.getElementById("myForm");
  var formData = new FormData(myForm);
  if (true) {
    //myForm.checkValidity()) {
    event.preventDefault();

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/predict");
    xhr.onload = function () {
      console.log("recv result");
      const response = xhr.responseText;
      document.getElementById("result").innerHTML = response;
    };
    xhr.send(formData);
  }
});