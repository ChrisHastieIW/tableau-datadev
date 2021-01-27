
//(function () {

  var viz;

  $(document).ready(function () {

    // Set up the initial form with default values and dropdowns
    initializeViz();

  })

  function initializeViz() {
      var placeholderDiv = document.getElementById("tableauViz"),
          url = "https://10ax.online.tableau.com/t/chrishastieiwdev598367/views/embeddingLevel2/BasicDashboard?:showAppBanner=false&:display_count=n&:showVizHome=n&:origin=viz_share_link",
          options = {
            width: placeholderDiv.offsetWidth,
            height: placeholderDiv.offsetHeight,
            hideTabs: true,
            hideToolbar: true,
            onFirstInteractive: function () {
                // Add event listener for selection changes
                viz.addEventListener(tableau.TableauEventName.MARKS_SELECTION, retrieveSelectedMarks);
            }
          };

      viz = new tableau.Viz(placeholderDiv, url, options);
      // Create a viz object and embed it in the container div.

  }

  function updateTextBox(text) {
    $("#selectedMarksTextBox").val(text);
  }

  function parseMarks(marks) {
    let parsedMarks = []
    marks.forEach(function(mark){
      let pairs = mark.getPairs()
      marksList = []
      pairs.forEach(function(pair){
        marksList.push(`${pair.fieldName}: ${pair.formattedValue}`)
      })
      parsedMarks.push(marksList)
    })
    return parsedMarks
  }

  function retrieveSelectedMarks(marksEvent) {

    marksEvent.getMarksAsync()
    .then(function(marks) {
      console.log(marks)
      return parseMarks(marks)
    })
    .then(function(parsedMarks) {
      console.log(parsedMarks)
      updateTextBox(JSON.stringify(parsedMarks))
    })

  }
//})();
