function fillBilling(f) {
  if(f.billingCheckbox.checked == true) {
    f.inputCustomerBillAddress1.value = f.inputCustomerAddress1.value;
    f.inputCustomerBillAddress2.value = f.inputCustomerAddress2.value;
    f.inputCustomerBillCity.value = f.inputCustomerCity.value;
    f.inputCustomerBillState.value = f.inputCustomerState.value;
    f.inputCustomerBillZip.value = f.inputCustomerZip.value;
    f.inputCustomerBillCountry.value = f.inputCustomerCountry.value;
  }
  else
  {
  	f.inputCustomerBillAddress1.value = "";
    f.inputCustomerBillAddress2.value = "";
    f.inputCustomerBillCity.value = "";
    f.inputCustomerBillState.value = "";
    f.inputCustomerBillZip.value = "";
    f.inputCustomerBillCountry.value = "";
  }
}