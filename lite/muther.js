/**
 * Mini Unit Test Harness
 * Copyright(c) 2011, Google Inc.
 *
 * A really tiny unit test harness.
 */

var muther = muther || {};

muther.assert = function(cond, err) {
  if (!cond) {
    throw err;
  }
};
  
muther.addTest_ = function(testDiv, innerHTML, pass) {
  var theTest = document.createElement('div');
  // Convert all angle brackets into displayable text.
  innerHTML = innerHTML.replace(/&/g, '&amp;').
      replace(/</g, '&lt;').
      replace(/>/g, '&gt;');
  theTest.innerHTML = innerHTML;
  theTest.setAttribute('style', pass ? 'color:#090' : 'color:#900');
  testDiv.appendChild(theTest);
};
  
// Run through all tests and record the results.
muther.test = function(testsToRun) {
  var progress = document.createElement('progress');
  var testDiv = document.createElement('div');
  document.body.insertBefore(testDiv, document.body.firstChild);
  document.body.insertBefore(progress, document.body.firstChild);

  var max = testsToRun.length;
  progress.max = max;
  progress.value = 0;
  testDiv.innerHTML = max + ' Tests';
  for (var t = 0; t < max; ++t) {
    var test = testsToRun[t];
    try {
      test();
      muther.addTest_(testDiv, test.name + ': Pass', true);
    } catch(e) {
      muther.addTest_(testDiv, test.name + ': Fail. ' + e, false);
    }
    progress.value += 1;
  }
};

